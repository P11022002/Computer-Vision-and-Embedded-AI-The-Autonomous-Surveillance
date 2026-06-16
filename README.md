# Autonomous AI Surveillance Rover 🤖🔒
### Computer Vision & Embedded AI Final Year Project (MCA)

An intelligent, low-cost autonomous security vehicle built using a hybrid Edge-Cloud computing architecture. The system utilizes an **ESP32-CAM** to stream live video feeds and execute low-level obstacle avoidance, while a high-performance **Django Backend Engine** processes deep learning computer vision algorithms (**YOLOv8** & **Face Recognition**) in real-time. System controls, analytical sensor logs, and live feeds are served beautifully on a **React-based Web Dashboard**.

---

## 📌 Features

- **Hybrid Edge-AI Processing:** Offloads heavy deep-learning inference from the constrained ESP32 microcontroller to a centralized Python web-server backend.
- **Real-Time Object Detection:** Integration with `Ultralytics YOLOv8` to detect humans, suspicious items, and hazards with localized bounding boxes.
- **Intruder vs. Personnel Identification:** Custom Face Recognition layer using `dlib` embeddings to distinguish between authorized users and potential threats.
- **Dual-Mode Control Interface:** - *Autonomous Mode:* Rover uses hardware-level ultrasonic tracking to navigate spaces independently.
  - *Manual Mode:* Low-latency digital joystick control via WebSockets over the web panel.
- **Sensor Telemetry Dashboard:** Live analytics tracking system health, classification logs, and connection latency indicators.

---

## 🏗️ System Architecture

The project is split into three decoupled components interacting synchronously:

```text
                  +--------------------------------+
                  |  Frontend Dashboard (React)    |
                  +--------------------------------+
                             ▲          │
            WebSocket Stream │          │ HTTP API Controls
             & Threat Alerts │          ▼
                  +--------------------------------+
                  |  Backend Core Engine (Django)  |
                  +--------------------------------+
                             ▲          │
               Live MJPEG    │          │ Driving
               Video Stream  │          ▼ Commands (Forward/Turn)
                  +--------------------------------+
                  | Embedded Hardware (ESP32-CAM)  |
                  +--------------------------------+