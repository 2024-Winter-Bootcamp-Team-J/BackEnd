from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from memo.models import Memo
from .documents import MemoDocument

# memo앱의 save이벤트가 발생하면 index_memo함수 실행
@receiver(post_save, sender=Memo)
def index_memo(sender, instance, created, **kwargs):
    if created:
        # memo_document는 opensearch에 저장할 데이터를 정의
        # openserach에 index가 자동으로 저장되어 있어서 한 번에 합치기가 불가능..
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
