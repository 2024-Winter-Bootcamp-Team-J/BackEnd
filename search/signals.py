from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from memo.models import Memo
from .documents import MemoDocument
from node.models import Node
from .documents import NodeDocument

# memo앱의 save이벤트가 발생하면 index_memo함수 실행
@receiver(post_save, sender=Memo)
def index_memo(sender, instance, created, **kwargs):
    if created:
        # memo_document는 opensearch에 저장할 데이터를 정의
        memo_document = MemoDocument(meta={'id': instance.memo_id})
        memo_document.memo_id = instance.memo_id
        memo_document.node_id = instance.node_id
        memo_document.user_id = instance.user_id
        memo_document.content = instance.content
        memo_document.is_deleted = instance.is_deleted
        memo_document.created_at = instance.created_at
        memo_document.deleted_at = instance.deleted_at
        memo_document.save(index='memo')

# memo앱의 delete이벤트가 발생하면 delete_memo_from_index함수 실행
@receiver(post_delete, sender=Memo)
def delete_memo_from_index(sender, instance, **kwargs):
    MemoDocument.get(id=instance.memo_id).delete()
    

@receiver(post_save, sender=Node)
def index_node(sender, instance, **kwargs):
    node_document = NodeDocument(meta={'id': instance.node_id})
    node_document.node_id = instance.node_id
    node_document.name = instance.name
    node_document.created_at = instance.created_at
    node_document.is_deleted = instance.is_deleted
    node_document.deleted_at = instance.deleted_at
    node_document.node_img = instance.node_img
    node_document.save(index='node')

@receiver(post_delete, sender=Node)
def delete_node_from_index(sender, instance, **kwargs):
    NodeDocument.get(id=instance.node_id).delete()