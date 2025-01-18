from __future__ import absolute_import, unicode_literals
# Celery 앱을 import하여 Django가 항상 import하도록 만듦
from celery import app as celery_app

__all__ = ('celery_app',)