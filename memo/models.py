from django.db import models
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

class Memo(models.Model):
    memo_id = models.BigAutoField(primary_key=True)
    node_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.memo_id)

@registry.register_document
class MemoDocument(Document):
    class Index:
        name = 'memos'

    class Django:
        model = Memo  # Memo 모델을 참조하여 매핑

        # Memo 모델에서 정의된 필드를 Elasticsearch 필드로 자동 매핑
        fields = [
            'memo_id',
            'node_id',
            'user_id',
            'content',
            'is_deleted',
            'created_at',
            'deleted_at',
        ]
