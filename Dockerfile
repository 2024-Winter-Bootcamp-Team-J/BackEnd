# Python 이미지 사용
FROM python:3.9-slim

# .pyc 파일 생성 억제
ENV PYTHONDONTWRITEBYTECODE=1

# 실시간 로그 출력을 위해 버퍼 최소화
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /code

# requirements.txt 복사 및 설치
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# 프로젝트 복사
COPY . /code/