from django.urls import path
from .views import (
    CreateRelationView, GetRelationsView, CreateRelationTypeView,
    ListRelationTypesView, GetRelationTypeView
)

urlpatterns = [
    path('relations/', GetRelationsView.as_view(), name='get_relations'),
    path('relations/create/', CreateRelationView.as_view(), name='create_relation'),
    path('relation-types/', ListRelationTypesView.as_view(), name='list_relation_types'),
    path('relation-types/create/', CreateRelationTypeView.as_view(), name='create_relation_type'),
    path('relation-types/<int:pk>/', GetRelationTypeView.as_view(), name='get_relation_type'),
]