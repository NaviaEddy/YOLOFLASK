import os
import cv2
from ultralytics import YOLO

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '../models/yolo11m.pt')
    return YOLO(model_path)

model = load_model()

def detect_humans(image_path):
    results = model(image_path)
    humans = []

    for r in results:
        boxes = r.boxes
        for box, cls, conf in zip(boxes.xyxy, boxes.cls, boxes.conf):
            label = model.names[int(cls)]
            if label == 'person':
                humans.append({
                    'box': [float(x) for x in box.tolist()],
                    'confidence': float(conf),
                })

    annotated = results[0].plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    out_name = os.path.basename(image_path)
    out_path = os.path.join(os.path.dirname(image_path), 'out_' + out_name)
    print(out_path)
    cv2.imwrite(out_path, annotated)
    return humans, out_path
    
        