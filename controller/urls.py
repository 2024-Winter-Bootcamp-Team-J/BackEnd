from django.urls import path
from .views import ControllerView

urlpatterns = [
    path('', ControllerView.as_view(), name='write-create'),
]