# Basis-Image auf eine stabile Version gepinnt, die Python 3.11 verwendet, 
# um Inkompatibilität mit numpy/Python 3.12 zu umgehen.
ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:2024.05.0 
FROM ${BUILD_FROM}

# ----------------------------------------------------------------------
# SCHRITT 1: Systemabhängigkeiten installieren (Cache-Brecher nano ist noch aktiv)
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
# SCHRITT 2: Python-Pakete installieren (Fixes beibehalten)
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
