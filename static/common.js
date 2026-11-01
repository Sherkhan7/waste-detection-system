// Shared camera + WebSocket client used by both UI versions.
export class WasteClient {
  constructor({ video, overlay, onDetections, fps = 4 }) {
    this.video = video;
    this.overlay = overlay;
    this.onDetections = onDetections;
    this.interval = 1000 / fps;
    this.capture = document.createElement("canvas");
    this.busy = false;
    this.last = [];
  }

  async start() {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment", width: 640, height: 480 },
    });
    this.video.srcObject = stream;
    await this.video.play();
    const proto = location.protocol === "https:" ? "wss" : "ws";
    this.ws = new WebSocket(`${proto}://${location.host}/ws/detect`);
    this.ws.onmessage = (e) => {
      this.busy = false;
      this.last = JSON.parse(e.data).detections;
      this.draw();
      this.onDetections(this.last);
    };
    this.ws.onopen = () => (this.timer = setInterval(() => this.sendFrame(), this.interval));
  }

  stop() {
    clearInterval(this.timer);
    this.ws?.close();
    this.video.srcObject?.getTracks().forEach((t) => t.stop());
  }

  sendFrame() {
    if (this.busy || this.ws.readyState !== 1 || !this.video.videoWidth) return;
    this.busy = true; // one frame in flight at a time -> no latency build-up
    this.capture.width = this.video.videoWidth;
    this.capture.height = this.video.videoHeight;
    this.capture.getContext("2d").drawImage(this.video, 0, 0);
    this.capture.toBlob((b) => b && this.ws.send(b), "image/jpeg", 0.7);
  }

  draw() {
    const c = this.overlay;
    c.width = this.video.clientWidth;
    c.height = this.video.clientHeight;
    const ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.lineWidth = 3;
    ctx.font = "bold 14px system-ui";
    for (const d of this.last) {
      const [x1, y1, x2, y2] = d.box;
      const x = x1 * c.width, y = y1 * c.height;
      ctx.strokeStyle = d.bin.color;
      ctx.strokeRect(x, y, (x2 - x1) * c.width, (y2 - y1) * c.height);
      const text = `${d.label} ${(d.confidence * 100) | 0}%`;
      ctx.fillStyle = d.bin.color;
      ctx.fillRect(x, y - 20, ctx.measureText(text).width + 10, 20);
      ctx.fillStyle = "#000";
      ctx.fillText(text, x + 5, y - 5);
    }
  }
}
