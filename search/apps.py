from django.apps import AppConfig
from opensearch_dsl import connections

# opensearch config
class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    def ready(self):
        import search.signals  # 신호를 연결
        connections.create_connection(
        alias='default',
        hosts=['https://opensearch:9200'],  # opensearch가 실행 중인 호스트와 포트
        http_auth=('admin', 'admin'),  # 인증 정보 (필요시)
        use_ssl=True,
        verify_certs=False,  # SSL 인증서 검증 비활성화
        ssl_assert_hostname=False,  # 호스트 이름 검증 비활성화
        ssl_show_warn=False  # SSL 경고 비활성화
        )