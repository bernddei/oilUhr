ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

# Installiere Systemabhängigkeiten: OCR, JPEG und die notwendigen Build-Tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-data-deu \
    jpeg-dev \
    zlib-dev \
    # Diese Pakete sind entscheidend, um OpenCV erfolgreich zu kompilieren:
    build-base \
    cmake \
    git \
    linux-headers

# Installiere Python-Abhängigkeiten. 
# Wichtig: Zuerst setuptools/wheel aktualisieren, um den 'bdist_wheel' Fehler zu vermeiden.
RUN pip3 install --no-cache-dir --break-system-packages \
        setuptools wheel pip \
        && pip3 install --no-cache-dir --break-system-packages \
        requests \
        numpy \
        pytesseract \
        opencv-python-headless

WORKDIR /app
COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod a+x /app/run.sh
CMD [ "/app/run.sh" ]
