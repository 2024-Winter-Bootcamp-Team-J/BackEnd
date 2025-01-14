from django.db import models
from node.models import Node

class Memo(models.Model):
    memo_id = models.BigIntegerField(primary_key=True)
    node = models.ForeignKey(
        Node,  # 참조할 모델
        on_delete=models.CASCADE,  # 연결된 Node가 삭제되면 Memo도 삭제
        related_name="memos"  # 역참조 이름 설정
    ) # Node와 일대다 관계, 노드 삭제 시 메모도 삭제
    user_id = models.BigIntegerField()
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.memo_id)
