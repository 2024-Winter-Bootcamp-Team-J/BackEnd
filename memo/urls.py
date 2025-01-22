from django.urls import path
from .views import MemoCreateView, MemoRetrieveView  # MemoCreateView와 MemoRetrieveView를 사용

urlpatterns = [
    path('', MemoCreateView.as_view(), name='memo-create'),  # 메모 생성
    path('<int:pk>', MemoRetrieveView.as_view(), name='memo-detail'),  # 특정 메모 조회
]
