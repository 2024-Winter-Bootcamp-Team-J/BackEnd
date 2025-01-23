from django.urls import path
from .views import MemoSearchView

urlpatterns = [
    path('', MemoSearchView.as_view(), name='search'),
]