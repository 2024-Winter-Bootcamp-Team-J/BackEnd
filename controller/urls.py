from django.urls import path
from .views import WriteCreateView

urlpatterns = [
    path('writes/', WriteCreateView.as_view(), name='write-create'),
]
