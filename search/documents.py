from django_opensearch_dsl import Document
from opensearch_dsl import Document
from memo.models import Memo
from node.models import Node
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

class NodeDocument(Document):
    class Index:
        name = 'node'

    class Django:
        model = Node  # Node 모델을 참조하여 매핑

        # Node 모델에서 정의된 필드를 Openearch 필드로 자동 매핑
        fields = [
            'node_id',
            'name',
            'created_at',
            'is_deleted',
            'deleted_at',
            'node_img',
        ]