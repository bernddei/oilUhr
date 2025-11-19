ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

WORKDIR /app

COPY run.sh /app/run.sh
COPY main.py /app/main.py
RUN chmod +x /app/run.sh

CMD [ "/app/run.sh" ]
