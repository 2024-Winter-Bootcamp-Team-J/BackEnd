from django.urls import path
from .views import NodeCreateView, NodeListView, NodeDetailView

urlpatterns = [
    path('', NodeListView.as_view(), name='list_nodes'),  # 모든 노드 조회
    path('<int:node_id>', NodeDetailView.as_view(), name='detail_node'),  # 특정 노드 조회
    path('create', NodeCreateView.as_view(), name='create_node'),  # 노드 생성
]
