from django.urls import path
from .views import MemoSearchView

urlpatterns = [
    path('search/', MemoSearchView.as_view(), name='memo-search'),
]