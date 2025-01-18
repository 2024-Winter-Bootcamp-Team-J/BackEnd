from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import example_task

class ExampleView(APIView):
    def get(self, request):
        # Celery 비동기 작업 호출
        result = example_task.delay(5, 7)
        return Response({'task_id': result.id})
