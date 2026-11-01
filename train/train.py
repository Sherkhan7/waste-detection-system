"""Fine-tune a small YOLO model on a waste dataset. Run on a GPU machine (e.g. Colab).

Dataset: export a waste-detection set in YOLO format (Roboflow Universe has many, or
convert TACO from COCO). Remap its classes to: paper, plastic, glass, metal, organic, general
(see backend/bins.py) so the app's bin logic works without changes.

    pip install ultralytics
    python train.py --data /path/to/data.yaml --epochs 50
    # then copy runs/detect/waste/weights/best.pt -> backend/weights/best.pt
"""
import argparse

from ultralytics import YOLO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to YOLO data.yaml")
    ap.add_argument("--base", default="yolo11n.pt", help="pretrained checkpoint (small = fast on CPU)")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    a = ap.parse_args()

    model = YOLO(a.base)
    model.train(data=a.data, epochs=a.epochs, imgsz=a.imgsz, name="waste", patience=15)
    metrics = model.val()  # mAP50 / mAP50-95 + per-class results: put these in your report
    print("mAP50:", metrics.box.map50, "mAP50-95:", metrics.box.map)


if __name__ == "__main__":
    main()
