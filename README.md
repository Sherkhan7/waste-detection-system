# Intelligent Waste Detection System

FastAPI backend + two vanilla-JS frontends (gamified and informational) sharing one detector.

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000 (camera needs localhost or HTTPS).
Without `backend/weights/best.pt` the API runs in **demo mode** (fake detections) so you can build the UI first.
`GET /api/health` reports `"mode": "demo"` or `"yolo"`.

## Train

See `train/train.py`. Put the resulting `best.pt` in `backend/weights/`.

## Layout

- `backend/` – FastAPI (`/api/detect`, `/ws/detect`, `/api/bins`), detector, class → bin mapping
- `static/common.js` – camera capture, WebSocket client, bounding-box overlay
- `static/gamified/` – score, streak, bin highlighting (awareness for kids)
- `static/informational/` – clean view with bin guidance and facts
- `train/` – YOLO fine-tuning script
