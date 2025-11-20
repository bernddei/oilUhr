ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

# Installiere Systemabhängigkeiten, die für OpenCV/Tesseract benötigt werden
RUN apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-data-deu \
    jpeg-dev \
    zlib-dev \
    # Zusätzliche Build-Abhängigkeiten zur Fehlerbehebung
    build-base \
    cmake \
    git \
    linux-headers

# Installiere Python-Abhängigkeiten. WICHTIG:
# 1. setuptools wird zuerst aktualisiert, um den 'bdist_wheel' Fehler zu beheben.
# 2. opencv-python-headless ist der Hauptverursacher und wird als letztes installiert.
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
