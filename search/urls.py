from django.urls import path
from .views import MemoSearchView

urlpatterns = [
    path('<str:search>/', MemoSearchView.as_view(), name='search'),
]