#!/usr/bin/env python3
import os
import time
import json
import re
import requests
import numpy as np
import cv2
import pytesseract

OPTIONS_PATH = "/data/options.json"

def load_options():
    try:
        with open(OPTIONS_PATH, "r") as f:
            return json.load(f)
    except:
        return {
            "esp_ip": "192.168.1.45",
            "poll_interval": 10,
            "roi_x": 180,
            "roi_y": 362,
            "roi_w": 293,
            "roi_h": 73,
            "debug": False
        }

opts = load_options()

ESP_IP = opts["esp_ip"]
POLL_INTERVAL = int(opts["poll_interval"])
ROI_X = int(opts["roi_x"])
ROI_Y = int(opts["roi_y"])
ROI_W = int(opts["roi_w"])
ROI_H = int(opts["roi_h"])
DEBUG = bool(opts.get("debug", False))

CAPTURE_URL = f"http://{ESP_IP}/capture"

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")

def fetch_image():
    try:
        r = requests.get(CAPTURE_URL, timeout=8)
        r.raise_for_status()
        arr = np.frombuffer(r.content, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if DEBUG:
            log(f"Bild empfangen: {img.shape if img is not None else 'None'}")
        return img
    except Exception as e:
        log(f"Fehler beim Bildabruf: {e}", "ERROR")
        return None

def preprocess_and_ocr(img):
    try:
        h, w = img.shape[:2]
        
        base_w, base_h = 883.0, 783.0
        x1 = int(ROI_X * (w / base_w))
        y1 = int(ROI_Y * (h / base_h))
        x2 = int(x1 + ROI_W * (w / base_w))
        y2 = int(y1 + ROI_H * (h / base_h))
        
        x1 = max(0, min(w-1, x1))
        x2 = max(1, min(w, x2))
        y1 = max(0, min(h-1, y1))
        y2 = max(1, min(h, y2))
        
        crop = img[y1:y2, x1:x2]
        
        if crop.size == 0:
            log("ROI ist leer!", "ERROR")
            return None, None
        
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        
        config = r'-c tessedit_char_whitelist=0123456789., --psm 7'
        text = pytesseract.image_to_string(thresh, config=config, lang='deu')
        
        text = text.strip().replace(" ", "").replace("\n", "")
        text = text.replace("O", "0").replace("o", "0")
        text = text.replace("I", "1").replace("|", "1").replace("l", "1")
        
        if DEBUG:
            log(f"OCR Rohtext: '{text}'")
        
        match = re.search(r'(\d+[\.,]?\d*)', text)
        if match:
            value_str = match.group(1).replace(",", ".")
            try:
                value = float(value_str)
                log(f"Erkannter Wert: {value} L")
                return value, text
            except:
                log(f"Konnte '{value_str}' nicht umwandeln", "WARN")
                return None, text
        else:
            log(f"Keine Zahl gefunden in: '{text}'", "WARN")
            return None, text
            
    except Exception as e:
        log(f"Fehler bei OCR: {e}", "ERROR")
        return None, None

def publish_to_ha(value):
    try:
        url = "http://supervisor/core/api/states/sensor.oilmeter"
        token = os.environ.get("SUPERVISOR_TOKEN", "")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "state": str(value),
            "attributes": {
                "unit_of_measurement": "L",
                "friendly_name": "Ölzählerstand",
                "device_class": "volume",
                "state_class": "total_increasing",
                "icon": "mdi:oil"
            }
        }
        
        r = requests.post(url, headers=headers, json=data, timeout=5)
        
        if r.status_code in (200, 201):
            log(f"Wert {value} L an HA gesendet")
        else:
            log(f"HA-Update fehlgeschlagen: {r.status_code}", "ERROR")
            
    except Exception as e:
        log(f"Fehler beim Senden an HA: {e}", "ERROR")

def main():
    log("=== OilUhr OCR Add-on gestartet ===")
    log(f"ESP32-CAM: {ESP_IP}")
    log(f"Poll-Intervall: {POLL_INTERVAL}s")
    log(f"ROI: x={ROI_X}, y={ROI_Y}, w={ROI_W}, h={ROI_H}")
    log(f"Debug: {DEBUG}")
    
    while True:
        try:
            img = fetch_image()
            
            if img is None:
                log("Kein Bild empfangen", "WARN")
            else:
                value, raw = preprocess_and_ocr(img)
                
                if value is not None:
                    publish_to_ha(value)
                else:
                    log("Keine gültige Zahl erkannt", "WARN")
                    
        except Exception as e:
            log(f"Fehler in Hauptschleife: {e}", "ERROR")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
