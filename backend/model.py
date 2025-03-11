import torch
from PIL import Image
from ultralytics import YOLO
from transformers import ViTForImageClassification, ViTFeatureExtractor

import os
print("Files in models/:", os.listdir("../models/"))

yolo_model = YOLO(r"../models/best.pt")
vit_model = ViTForImageClassification.from_pretrained("../models/vit_best/")
feature_extractor = ViTFeatureExtractor.from_pretrained("../models/vit_best/")

def detect_disease(image_path):
    image = Image.open(image_path).convert("RGB")
    results = yolo_model(image_path)
    boxes = results[0].boxes if results else []

    diseases = []
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cropped = image.crop((x1, y1, x2, y2))

        inputs = feature_extractor(images=cropped, return_tensors="pt")
        with torch.no_grad():
            outputs = vit_model(**inputs)
        pred_class = outputs.logits.argmax(-1).item()
        disease_name = vit_model.config.id2label[pred_class]

        diseases.append({
            "disease": disease_name,
            "confidence": round(float(box.conf[0]), 4),
            "bbox": [x1, y1, x2, y2]
        })

    return {"detections": diseases}
