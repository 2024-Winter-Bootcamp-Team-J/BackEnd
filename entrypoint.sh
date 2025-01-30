#!/bin/bash

# 로그 출력을 위해 스크립트 시작 시 메시지 출력
echo "Starting entrypoint script..."

#python manage.py makemigrations
# Django migration 자동화
echo "Running migrations..."
python manage.py migrate || { echo "Migration failed"; exit 1; }

# 정적 파일 모으기 (collectstatic)
echo "Collecting static files..."
mkdir -p /code/static
chown -R www-data:www-data /code/static
chmod -R 775 /code/static
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# Gunicorn 포그라운드에서 실행
echo "Starting Gunicorn..."
exec gunicorn --workers=4 --timeout=30 --worker-class=gevent  config.wsgi:application --bind 0.0.0.0:8000