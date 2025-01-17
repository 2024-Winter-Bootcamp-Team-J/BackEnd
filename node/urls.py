from django.urls import path
from .views import NodeCreateView, NodeListView, NodeDetailView

urlpatterns = [
    path('nodes/', NodeListView.as_view(), name='list_nodes'),  # 모든 노드 조회
    path('nodes/<int:node_id>/', NodeDetailView.as_view(), name='detail_node'),  # 특정 노드 조회
    path('nodes/create/', NodeCreateView.as_view(), name='create_node'),  # 노드 생성
]
