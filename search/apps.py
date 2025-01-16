from django.apps import AppConfig
from elasticsearch_dsl import connections

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    def ready(self):
        import search.signals  # 신호를 연결
        connections.create_connection(
        alias='default',
        hosts=['https://localhost:9200'],  # Elasticsearch가 실행 중인 호스트와 포트
)