from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django 설정을 Celery에 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('backend')

# Django의 설정을 Celery 설정으로 가져옴
app.config_from_object('django.conf:settings', namespace='CELERY')

# 모든 Django 앱에서 비동기 태스크를 로드
app.autodiscover_tasks(['controller'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')