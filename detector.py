"""Pluggable detector. Uses Ultralytics YOLO if weights exist, otherwise a demo stub."""
import os
import random
from pathlib import Path

import cv2
import numpy as np

from bins import resolve

WEIGHTS = Path(os.getenv("WEIGHTS", Path(__file__).parent / "weights" / "best.pt"))
CONF = float(os.getenv("CONF", "0.4"))


class Detector:
    def __init__(self):
        self.model = None
        self.mode = "demo"
        if WEIGHTS.exists():
            from ultralytics import YOLO  # imported lazily so demo mode needs no torch
            self.model = YOLO(str(WEIGHTS))
            self.mode = "yolo"

    def detect(self, jpeg: bytes) -> list[dict]:
        img = cv2.imdecode(np.frombuffer(jpeg, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return []
        h, w = img.shape[:2]
        if self.model is None:
            return self._demo()
        out = []
        res = self.model.predict(img, conf=CONF, verbose=False)[0]
        for b in res.boxes:
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            label = res.names[int(b.cls)]
            out.append({
                "label": label,
                "confidence": round(float(b.conf), 3),
                "box": [x1 / w, y1 / h, x2 / w, y2 / h],  # normalised 0..1
                **resolve(label),
            })
        return out

    @staticmethod
    def _demo() -> list[dict]:
        """Fake detections so the UI can be developed without a trained model."""
        label = random.choice(["plastic", "paper", "glass", "metal", "organic"])
        x, y = random.uniform(0.2, 0.5), random.uniform(0.2, 0.5)
        return [{"label": label, "confidence": round(random.uniform(0.6, 0.95), 3),
                 "box": [x, y, x + 0.25, y + 0.3], **resolve(label)}]
