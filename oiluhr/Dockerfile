# Für 64bit RPi: FROM ghcr.io/home-assistant/aarch64-base:latest
# Für Intel/AMD:  FROM ghcr.io/home-assistant/amd64-base:latest
FROM ghcr.io/home-assistant/aarch64-base:latest

RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-deu \
    ffmpeg \
    py3-opencv \
    && pip3 install \
    requests \
    numpy

COPY run.sh /
COPY ocr.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]