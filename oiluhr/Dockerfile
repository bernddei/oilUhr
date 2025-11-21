# ----------------------------------------------------------------------
# Multi-Arch Base Image mit Python Support
# ----------------------------------------------------------------------
ARG BUILD_FROM
FROM $BUILD_FROM

# ----------------------------------------------------------------------
# SCHRITT 1: Systemabhängigkeiten installieren
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
    bash

# ----------------------------------------------------------------------
# SCHRITT 2: Python-Pakete installieren
# ----------------------------------------------------------------------
RUN pip3 install --no-cache-dir --break-system-packages \
    setuptools wheel pip 'scikit-build>=0.17.6' \
    && pip3 install --no-cache-dir --break-system-packages \
    requests numpy pytesseract 'opencv-python-headless==4.9.0.80'

# ----------------------------------------------------------------------
# SCHRITT 3: Add-on-Konfiguration und Start
# ----------------------------------------------------------------------
WORKDIR /app
COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
