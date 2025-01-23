from django.urls import path
from .views import MemoSearchView
from .views import NodeSearchView

urlpatterns = [
    path('search/memosearch', MemoSearchView.as_view(), name='search'),
    path('search/nodesearch', NodeSearchView.as_view(), name='search_nodes'),
]