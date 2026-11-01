from pathlib import Path

from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from bins import BINS
from detector import Detector

app = FastAPI(title="Waste Detection API")
detector = Detector()
STATIC = Path(__file__).parent.parent / "static"


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": detector.mode}


@app.get("/api/bins")
def bins():
    return BINS


@app.post("/api/detect")
async def detect(file: UploadFile = File(...)):
    return {"detections": detector.detect(await file.read())}


@app.websocket("/ws/detect")
async def ws_detect(ws: WebSocket):
    """Client sends binary JPEG frames; server replies with JSON detections per frame."""
    await ws.accept()
    try:
        while True:
            frame = await ws.receive_bytes()
            await ws.send_json({"detections": detector.detect(frame)})
    except WebSocketDisconnect:
        pass


@app.get("/")
def root():
    return RedirectResponse("/static/gamified/index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
