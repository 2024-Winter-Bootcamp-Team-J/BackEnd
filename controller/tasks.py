# myapp/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
'''
example 
@shared_task
def example_task(x, y):
    return x + y
'''