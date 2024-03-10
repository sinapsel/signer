#!/bin/bash

echo "start uvicron server"

uvicorn main:app --reload --reload-dir app --host 0.0.0.0 --port ${APP_EXPOSING_PORT} --proxy-headers
