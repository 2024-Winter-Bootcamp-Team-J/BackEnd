# Python 이미지 사용
FROM python:3.9-slim

# .pyc 파일 생성 억제 및 실시간 로그 출력
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /code

# requirements.txt 복사 및 설치 (캐싱 활용)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

# 프로젝트 복사
COPY . /code/

# Nginx 설치는 Docker Compose 파일에서 분리하여 관리하는 것이 좋음
# Django는 Gunicorn을 사용하여 실행하고, Nginx는 별도의 서비스로 관리

EXPOSE 8000

# entrypoint.sh 복사 및 실행 권한 추가
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# entrypoint.sh를 엔트리포인트로 설정
ENTRYPOINT ["/entrypoint.sh"]