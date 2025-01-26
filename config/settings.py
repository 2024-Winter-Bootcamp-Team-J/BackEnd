"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
from celery.schedules import crontab

load_dotenv()

# Prometheus URL 설정
PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')  # 기본값 설정

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt', # 회원 기능 jwt
    'rest_framework_simplejwt.token_blacklist', # 블랙리스트
    'drf_yasg', # swagger 관련 앱
    'api', #API 앱 추가
    'memo', #memo(api) 앱 추가
    'users',
    'node', # node 앱 추가
    'relation', # relation 앱 추가
    'search',  # 'search' 앱 추가
    'controller',  # 'controller' 앱 추가
    "django_opensearch_dsl",  # django_opensearch_dsl 앱 추가
    'django_celery_beat', # Celery Beat 앱 추가
    'django_celery_results', # Celery Results 앱 추가

]
CORS_ALLOW_ALL_ORIGINS = True

OPENSEARCH_DSL = {
    'default': {
        'HOST': 'https://opensearch:9200',
        'PORT': 9200,
        'USE_SSL': True,
        'TIMEOUT': 30,
        'http_auth': ('admin', 'Link-in1234'),
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', # corsheaders 미들웨어 추가
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {  # jsno 포맷터
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/code/django_logs/django.log',  # 로그 파일 경로
            'formatter': 'json',  # JSON 포맷터를 사용
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.contrib.admin': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.core.cache': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.middleware': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}




CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # 프론트엔드 도메인
    "http://www.link-in.o-r.kr",  # 요청이 발생하는 출처
    "https://www.link-in.o-r.kr",  # HTTPS 요청 처리 시
]

CSRF_TRUSTED_ORIGINS = [
    "http://www.link-in.o-r.kr",  # 요청이 발생하는 출처
    "https://www.link-in.o-r.kr",  # HTTPS 요청 처리 시
]

CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'users.User'
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "postgres"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # 도커 컴포즈 설정의 Redis 호스트
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# 세션 백엔드 설정 (Redis 사용)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# S3 setting
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')


# 파일 업로드와 관련된 기본 설정
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')

# S3에 저장될 파일의 경로를 지정 (선택 사항)
AWS_LOCATION =os.environ.get('AWS_LOCATION')

# S3에서 제공하는 미디어 파일의 URL
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{AWS_LOCATION}/'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', # jwt 관련
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),  # Access Token 유효기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh Token 유효기간
    'ROTATE_REFRESH_TOKENS': True,                  # Refresh Token 재발급 시 새로 발급
    'BLACKLIST_AFTER_ROTATION': True,               # 이전 Refresh Token 블랙리스트 처리
    'AUTH_HEADER_TYPES': ('Bearer',),               # Authorization 헤더 유형 설정
    'ALGORITHM': 'HS256',                           # 암호화 알고리즘
    'SIGNING_KEY': SECRET_KEY,                      # 토큰 서명 키
    'VERIFYING_KEY': None,                          # RSA를 사용할 경우 공개 키 설정
    'USER_ID_FIELD': 'user_id',                     # 사용자 모델의 ID 필드
    'USER_ID_CLAIM': 'user_id',                     # 토큰에 포함될 사용자 ID 필드 이름
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'USE_SESSION_AUTH': False,
}

# Celery setttings  
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
'''
CELERY_BEAT_SCHEDULE = {
    'example-task': {
        'task': 'myapp.tasks.example_task',
        'schedule': crontab(minute='*/1'),  # 매 1분마다 실행
    },
}
'''


# 정적 파일 설정
STATIC_URL = '/static/'  # URL 경로
# collectstatic으로 모을 정적 파일들이 위치할 디렉토리
STATIC_ROOT = '/app/static/' # static 디렉토리로 설정


# 미디어 파일 설정
MEDIA_URL = '/media/'  # URL 경로
# 미디어 파일들이 저장될 디렉토리
MEDIA_ROOT = '/app/media'
