# ----------------------------------------------------------------------
# SCHRITT 3: Installation der Python-Abhängigkeiten
# Wir erzwingen die Installation einer neueren Version von scikit-build, 
# um den Fehler im internen Build-Backend von OpenCV zu umgehen.
# ----------------------------------------------------------------------
RUN pip3 install --no-cache-dir --break-system-packages \
        setuptools wheel pip \
        'scikit-build>=0.17.6' \
        && pip3 install --no-cache-dir --break-system-packages \
        requests \
        numpy \
        pytesseract \
        opencv-python-headless==4.9.0.80
