"""YOLOv8 handler for the Autonomous Surveillance Rover backend.

This module provides a production-ready interface for loading YOLOv8 weights,
reading an MJPEG stream from an ESP32-CAM, running inference, and annotating
frames for a Django/Channels video pipeline.

Dependencies:
    - Python 3.10+
    - opencv-python
    - ultralytics
    - numpy

Optional compatibility:
    - face_recognition (for later face authorization pipelines)
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

logger = logging.getLogger(__name__)

DEFAULT_CONFIDENCE_THRESHOLD = 0.25
DEFAULT_IOU_THRESHOLD = 0.45
DEFAULT_STREAM_TIMEOUT_SECONDS = 10.0
DEFAULT_FRAME_TIMEOUT_SECONDS = 5.0
MAX_CONSECUTIVE_DROPPED_FRAMES = 5


class YOLOv8Handler:
    """Encapsulates YOLOv8 loading, inference, and frame annotation."""

    def __init__(
        self,
        weights_path: str,
        device: str = "cpu",
        conf_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        iou_threshold: float = DEFAULT_IOU_THRESHOLD,
    ) -> None:
        self.weights_path = weights_path
        self.device = device
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.model: Optional[YOLO] = None
        self._validate_weight_path()
        self.load_model()

    def _validate_weight_path(self) -> None:
        if not os.path.isfile(self.weights_path):
            logger.error("YOLO weights file not found at %s", self.weights_path)
            raise FileNotFoundError(
                f"YOLO weights not found: {self.weights_path}. "
                "Verify the path and that the file is accessible."
            )

    def load_model(self) -> None:
        try:
            self.model = YOLO(self.weights_path)
            self.model.fuse()  # fuse conv+bias for faster inference if supported
            self.model.model.to(self.device)
            logger.info("Loaded YOLOv8 model from %s on device %s", self.weights_path, self.device)
        except FileNotFoundError:
            raise
        except Exception as exc:
            logger.exception("Failed to initialize YOLO model: %s", exc)
            raise RuntimeError("Unable to load YOLOv8 model; check model weights and dependencies.") from exc

    def open_stream(self, source_url: str, timeout_seconds: float = DEFAULT_STREAM_TIMEOUT_SECONDS) -> cv2.VideoCapture:
        capture = cv2.VideoCapture(source_url)
        start_time = time.time()

        while not capture.isOpened():
            if time.time() - start_time > timeout_seconds:
                capture.release()
                logger.error("Unable to open video stream within %.1fs: %s", timeout_seconds, source_url)
                raise TimeoutError(f"Video stream open timed out after {timeout_seconds}s for {source_url}")
            time.sleep(0.25)

        logger.info("Opened video stream: %s", source_url)
        return capture

    def read_frame(self, capture: cv2.VideoCapture, timeout_seconds: float = DEFAULT_FRAME_TIMEOUT_SECONDS) -> Optional[np.ndarray]:
        start_time = time.time()
        dropped_frames = 0

        while time.time() - start_time < timeout_seconds:
            success, frame = capture.read()
            if success and frame is not None:
                if dropped_frames:
                    logger.warning("Recovered after %d dropped frames", dropped_frames)
                return frame

            dropped_frames += 1
            logger.debug("Dropped frame %d while reading stream", dropped_frames)
            if dropped_frames >= MAX_CONSECUTIVE_DROPPED_FRAMES:
                logger.warning("Too many consecutive dropped frames (%d)", dropped_frames)
            time.sleep(0.05)

        logger.error("Timeout waiting for a valid frame after %.1fs", timeout_seconds)
        return None

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        if frame is None:
            raise ValueError("Received empty frame for preprocessing")

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_frame

    def perform_inference(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        if self.model is None:
            raise RuntimeError("YOLO model instance is not loaded")

        try:
            results = self.model(
                frame,
                imgsz=640,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                device=self.device,
            )
        except Exception as exc:
            logger.exception("YOLO inference failed: %s", exc)
            raise RuntimeError("YOLOv8 inference execution failed") from exc

        if not results:
            return []

        detections = []
        for result in results:
            boxes = result.boxes if hasattr(result, "boxes") else []
            for box in boxes:
                try:
                    xyxy = box.xyxy.tolist()[0]
                    score = float(box.conf[0])
                    class_id = int(box.cls[0])
                    label = self.model.names[class_id] if self.model.names else str(class_id)
                    detections.append(
                        {
                            "xyxy": xyxy,
                            "confidence": score,
                            "class_id": class_id,
                            "label": label,
                        }
                    )
                except Exception as frame_exc:
                    logger.warning("Skipped malformed detection result: %s", frame_exc)
        return detections

    def draw_annotations(
        self,
        frame: np.ndarray,
        detections: List[Dict[str, Any]],
        additional_labels: Optional[List[str]] = None,
    ) -> np.ndarray:
        annotated = frame.copy()
        additional_labels = additional_labels or []

        for detection in detections:
            xyxy = detection.get("xyxy")
            conf = detection.get("confidence", 0.0)
            label = detection.get("label", "unknown")
            if not xyxy or len(xyxy) != 4:
                logger.debug("Skipping invalid annotation data: %s", detection)
                continue

            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            caption = f"{label} {conf:.2f}"
            if additional_labels:
                caption = f"{caption} | {' | '.join(additional_labels)}"
            cv2.putText(
                annotated,
                caption,
                (x1, max(y1 - 8, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        return annotated

    def process_stream(
        self,
        source_url: str,
        frame_callback: Callable[[np.ndarray, List[Dict[str, Any]]], Any],
        max_frames: int = 0,
    ) -> None:
        capture = self.open_stream(source_url)
        frame_count = 0

        try:
            while True:
                frame = self.read_frame(capture)
                if frame is None:
                    raise RuntimeError("Stream stopped returning valid frames")

                rgb_frame = self.preprocess_frame(frame)
                detections = self.perform_inference(rgb_frame)
                annotated_frame = self.draw_annotations(frame, detections)
                frame_callback(annotated_frame, detections)

                frame_count += 1
                if max_frames and frame_count >= max_frames:
                    logger.info("Reached max_frames limit: %d", max_frames)
                    break

        finally:
            capture.release()
            logger.info("Released video capture for %s", source_url)


def default_frame_callback(frame: np.ndarray, detections: List[Dict[str, Any]]) -> None:
    logger.debug("Processed frame with %d detections", len(detections))
