# backend

# 프로젝트명

## 요구사항
- Docker
- Docker Compose
- Git
- .env 루트 디렉토리에 생성 및 노션 참고 복붙
   -  ( secretkey의 경우 settings.py 본인 키값 사용 )

## 설치 및 실행

1. 깃헙 저장소에서 프로젝트를 클론하세요:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. `.env` 파일을 작성하세요:
   `.env.example` 파일을 참고하여 `.env` 파일을 생성합니다.
       .env 루트 디렉토리에 생성 및 노션 참고 복붙
        secretkey의 경우 settings.py 본인 키값 사용 )

4. Docker Compose를 실행하세요:
   ```bash
   docker-compose up -d --build
   ```

5. Django에 필요한 마이그레이션을 실행하세요:
   ```bash
   docker exec -it django_web
   python manage.py migrate
   ```

6. 애플리케이션에 접속하세요:
   브라우저에서 [http://localhost:8000](http://localhost:8000)를 열어 프로젝트를 확인하세요.
