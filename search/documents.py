from django_opensearch_dsl import Document
from opensearch_dsl import Document
from memo.models import Memo

#model과 document를 연결하는 곳
#document는 Opensearch에 저장할 데이터를 정의

class MemoDocument(Document):
    class Index:
        name = 'memo'

    class Django:
        model = Memo  # Memo 모델을 참조하여 매핑

        # Memo 모델에서 정의된 필드를 Openearch 필드로 자동 매핑
        fields = [
            'memo_id',
            'node_id',
            'user_id',
            'content',
            'is_deleted',
            'created_at',
            'deleted_at',
        ]
    # 메모 검색을 위한 메소드
    @classmethod
    def search_memo(cls, query):
        # content 필드에 대해 full-text search
        return cls.search().filter('match', content=query)