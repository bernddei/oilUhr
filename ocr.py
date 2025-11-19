#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import requests
import time
import os
import re
import json

options_path = "/data/options.json"

with open(options_path, "r") as f:
    opts = json.load(f)

ESP_IP = opts["esp_ip"]
POLL_INTERVAL = opts["poll_interval"]
SNAPSHOT_URL = f"http://{ESP_IP}/capture"

# ROI aus deinem Beispielbild (Original 883x783, wird dynamisch skaliert)
ROI_X = 180
ROI_Y = 362
ROI_W = 293
ROI_H = 73

def fetch_image():
    try:
        r = requests.get(SNAPSHOT_URL, timeout=5)
        r.raise_for_status()
        img_arr = np.frombuffer(r.content, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        return img
    except:
        return None

def preprocess_and_ocr(img):
    h, w = img.shape[:2]
    # proportional skalieren
    x1 = int(ROI_X * (w/883))
    y1 = int(ROI_Y * (h/783))
    x2 = int(x1 + ROI_W * (w/883))
    y2 = int(y1 + ROI_H * (h/783))
    crop = img[y1:y2, x1:x2]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    kernel = np.ones((2, 2), np.uint8)
    th = cv2.dilate(th, kernel, iterations=1)
    config = r'-c tessedit_char_whitelist=0123456789,\. --psm 7'
    text = pytesseract.image_to_string(th, config=config)
    text = text.strip().replace(" ", "").replace("\n", "")
    text = text.replace("O", "0").replace("o", "0").replace("I", "1")
    m = re.search(r'(\d+[\.,]?\d*)', text)
    if m:
        val = m.group(1).replace(",", ".")
        try:
            return float(val)
        except:
            return None
    return None

def publish_to_ha(value):
    url = "http://supervisor/core/api/states/sensor.oilmeter"
    headers = {
        "Authorization": f"Bearer {os.environ.get('SUPERVISOR_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "state": value,
        "attributes": {
            "unit_of_measurement": "L",
            "friendly_name": "Ölzählerstand"
        }
    }
    requests.post(url, headers=headers, json=data, timeout=5)

def main():
    while True:
        img = fetch_image()
        if img is None:
            time.sleep(POLL_INTERVAL)
            continue
        val = preprocess_and_ocr(img)
        if val is not None:
            print("Erkannter Wert:", val)
            publish_to_ha(val)
        else:
            print("Keine Zahl erkannt")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()