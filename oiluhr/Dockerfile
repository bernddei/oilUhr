ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

# ----------------------------------------------------------------------
# SCHRITT 1: Systemabhängigkeiten installieren (Basis-Tools, Tesseract, Build-Tools)
# Ein temporärer Cache-Brecher (nano) wurde hinzugefügt, 
# um den fehlerhaften Zwischen-Cache zu umgehen.
# ----------------------------------------------------------------------
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
    linux-headers \
    nano

# ----------------------------------------------------------------------
# SCHRITT 2: Python-Pakete installieren (Workaround für OpenCV Build-Fehler)
# Die Installation ist in zwei Teilschritte in einer RUN-Zeile verkettet:
# 1. Installation des "scikit-build" Fixes (>=0.17.6)
# 2. Installation der Hauptpakete mit gepinntem opencv-python-headless (4.9.0.80)
# ----------------------------------------------------------------------
RUN pip3 install --no-cache-dir --break-system-packages \
    setuptools wheel pip 'scikit-build>=0.17.6' \
    && pip3 install --no-cache-dir --break-system-packages \
    requests numpy pytesseract 'opencv-python-headless==4.9.0.80'

# ----------------------------------------------------------------------
# SCHRITT 3: Add-on-Konfiguration
# ----------------------------------------------------------------------
WORKDIR /app
COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod a+x /app/run.sh
CMD [ "/app/run.sh" ]
