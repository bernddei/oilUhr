# ----------------------------------------------------------------------
# Basis-Image-Definition
# Pinned Base Image (Python 3.11) zur Umgehung des numpy/pkgutil-Fehlers in Python 3.12.
# ----------------------------------------------------------------------
FROM ghcr.io/home-assistant/aarch64-base:2024.05.0

# ----------------------------------------------------------------------
# SCHRITT 1: Systemabhängigkeiten installieren
# Erforderlich für Tesseract, OpenCV-Kompilierung (build-base, cmake, git etc.)
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
    linux-headers

# ----------------------------------------------------------------------
# SCHRITT 2: Python-Pakete installieren (Hauptfix für den Build)
# Die Installation ist in einem Befehl verkettet:
# 1. Installation des "scikit-build" Fixes (>0.17.6).
# 2. Installation der Hauptpakete (requests, numpy, pytesseract) und
#    der gepinnten OpenCV-Version (4.9.0.80).
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
