from django.db import models


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
