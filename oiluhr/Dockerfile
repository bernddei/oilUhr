ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

# Installiere Systemabhängigkeiten: OCR, JPEG und die notwendigen Build-Tools
# (Dieser Schritt ist im Cache)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-data-deu \
    jpeg-dev \
    zlib-dev \
    build-base \
    cmake \
    git \
    linux-headers

# Installiere Python-Build-Abhängigkeiten
RUN pip3 install --no-cache-dir --break-system-packages \
        setuptools wheel pip

# Installiere OCR/CV Abhängigkeiten mit Versions-Pinning für OpenCV
RUN pip3 install --no-cache-dir --break-system-packages \
        requests \
        numpy \
        pytesseract \
        opencv-python-headless==4.9.0.80

WORKDIR /app
COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod a+x /app/run.sh
CMD [ "/app/run.sh" ]
