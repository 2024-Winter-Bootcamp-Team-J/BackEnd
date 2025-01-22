from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from node.models import Node
from .documents import NodeDocument
from memo.models import Memo
from .documents import MemoDocument

# Node 객체 저장 시 OpenSearch에 인덱싱
@receiver(post_save, sender=Node)
def index_node(sender, instance, created, **kwargs):
    if created:
        # NodeDocument 인스턴스 생성 및 OpenSearch에 저장
        node_document = NodeDocument(
            meta={'id': instance.node_id},  # OpenSearch의 고유 ID
            node_id=instance.node_id,
            name=instance.name,
            created_at=instance.created_at,
            deleted_at=instance.deleted_at,
            is_deleted=instance.is_deleted,
        )
        # OpenSearch에 저장
        node_document.save(index='node')

# Node 객체 삭제 시 OpenSearch에서 해당 데이터 삭제
@receiver(post_delete, sender=Node)
def delete_node_from_index(sender, instance, **kwargs):
    NodeDocument.get(id=instance.node_id).delete()

# memo앱의 save이벤트가 발생하면 index_memo함수 실행
@receiver(post_save, sender=Memo)
def index_memo(sender, instance, created, **kwargs):
    if created:
        # memo_document는 opensearch에 저장할 데이터를 정의
        memo_document = MemoDocument(meta={'id': instance.memo_id})
        memo_document.memo_id = instance.memo_id
        memo_document.node_id = instance.node_id
        memo_document.content = instance.content
        memo_document.is_deleted = instance.is_deleted
        memo_document.created_at = instance.created_at
        memo_document.deleted_at = instance.deleted_at
        memo_document.save(index='memo')

# memo앱의 delete이벤트가 발생하면 delete_memo_from_index함수 실행
@receiver(post_delete, sender=Memo)
def delete_memo_from_index(sender, instance, **kwargs):
    MemoDocument.get(id=instance.memo_id).delete()
    