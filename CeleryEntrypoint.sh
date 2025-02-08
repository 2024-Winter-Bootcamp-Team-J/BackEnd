#!/bin/bash

# 로그 출력을 위해 스크립트 시작 시 메시지 출력
echo "Starting Celery Worker entrypoint script..."

# Django migration 자동화
echo "Running migrations..."
python manage.py migrate || { echo "Migration failed"; exit 1; }

# Celery 워커 실행
echo "Starting Celery Worker..."
exec celery -A config worker --loglevel=info