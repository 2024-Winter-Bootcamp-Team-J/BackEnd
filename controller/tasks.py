# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def example_task(x, y):
    return x + y

@shared_task
def periodic_task():
    print("This is a periodic task.")