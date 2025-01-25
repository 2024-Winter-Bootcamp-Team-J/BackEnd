from django.urls import path
from .views import (
    CreateRelationView, GetRelationsView, CreateRelationTypeView,
    ListRelationTypesView, GetRelationTypeView,
    CreateUserNodeRelationView, GetUserNodeRelationsView
)

urlpatterns = [
    path('', GetRelationsView.as_view(), name='get_relations'),
    path('/create', CreateRelationView.as_view(), name='create_relation'),
    path('/types', ListRelationTypesView.as_view(), name='list_relation_types'),
    path('/types/create', CreateRelationTypeView.as_view(), name='create_relation_type'),
    path('/types/<int:pk>', GetRelationTypeView.as_view(), name='get_relation_type'),
    path('/user-node-relations/create', CreateUserNodeRelationView.as_view(), name='create_user_node_relation'),
    path('/user-node-relations/<int:user_id>', GetUserNodeRelationsView.as_view(), name='get_user_node_relations'),
]
