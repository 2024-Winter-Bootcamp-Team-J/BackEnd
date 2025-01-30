# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .category_extract_API import category_extract

@shared_task
def category_extract_task(text):
    message = category_extract(text)
    return message

