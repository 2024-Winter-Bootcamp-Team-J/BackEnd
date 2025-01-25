from django.apps import AppConfig
from opensearch_dsl import connections

# opensearch config
class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    def ready(self):
        import search.signals  # 신호를 연결
        connections.create_connection(
        alias="default",  # 기본 alias
        hosts=["http://opensearch:9200"],  # OpenSearch 클러스터 호스트
        http_auth=("admin", "Link-in1234"),  # 인증 정보
        use_ssl=True,
        verify_certs=False
        )