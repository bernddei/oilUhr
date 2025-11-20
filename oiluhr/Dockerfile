# ...
# [1/7] FROM ghcr.io/home-assistant/aarch64-base:latest
# ...

# [2/7] RUN apk add ...
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
    linux-headers # <<< NEU: Kommentar hier einfügen, um Cache zu brechen.

# [3/7] RUN pip3 install setuptools wheel pip
RUN pip3 install --no-cache-dir --break-system-packages \
        setuptools wheel pip

# [4/7] RUN pip3 install requests numpy pytesseract opencv-python-headless==4.9.0.80
RUN pip3 install --no-cache-dir --break-system-packages \
        requests \
        numpy \
        pytesseract \
        opencv-python-headless==4.9.0.80
# ...
