from django.apps import AppConfig
from opensearch_dsl import connections

# opensearch config
class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    def ready(self):
        import search.signals  # 신호를 연결
        from opensearchpy import OpenSearch
        from django.conf import settings

        self.client = OpenSearch(
            hosts=[{'host': 'https://opensearch:9200', 'port': 9200}],
            http_auth=('admin', 'Link-in1234'),
            use_ssl=True,
            verify_certs=True,
        )