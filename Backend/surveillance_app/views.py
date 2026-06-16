from __future__ import annotations

import logging
from typing import Any

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

logger = logging.getLogger(__name__)


@require_GET
def health_check(request: Any) -> JsonResponse:
    return JsonResponse({"status": "ok", "service": "autonomous-surveillance-rover"})


@require_POST
def control_command(request: Any) -> JsonResponse:
    payload = request.POST.dict()
    action = payload.get("action")
    if action not in {"forward", "backward", "left", "right", "stop", "autonomous"}:
        logger.warning("Received invalid control action: %s", action)
        return JsonResponse({"error": "invalid action"}, status=400)

    logger.info("Received control action: %s", action)
    return JsonResponse({"status": "queued", "action": action})
