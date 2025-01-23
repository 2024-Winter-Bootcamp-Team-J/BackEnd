from django.db import models

class Memo(models.Model):
    memo_id = models.BigAutoField(primary_key=True)
    node = models.ForeignKey('node.Node', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.memo_id)
