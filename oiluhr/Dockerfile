ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-data-deu \
    jpeg-dev \
    zlib-dev \
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
