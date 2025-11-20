#!/usr/bin/with-contenv bashio
set -e

bashio::log.info "OilUhr OCR Add-on wird gestartet..."

ESP_IP=$(bashio::config 'esp_ip')
POLL_INTERVAL=$(bashio::config 'poll_interval')
DEBUG=$(bashio::config 'debug')

bashio::log.info "ESP32-CAM IP: ${ESP_IP}"
bashio::log.info "Poll-Intervall: ${POLL_INTERVAL} Sekunden"

python3 /app/main.py
