from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from memo.models import Memo
from .documents import MemoDocument

@receiver(post_save, sender=Memo)
def index_memo(sender, instance, **kwargs):
    MemoDocument().update(instance)

@receiver(post_delete, sender=Memo)
def delete_memo_from_index(sender, instance, **kwargs):
    MemoDocument().delete(instance)