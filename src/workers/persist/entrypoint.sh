#!/bin/bash

nginx -g "daemon off;" &

cd /app

uvicorn main:app --host 0.0.0.0 --port 8000
