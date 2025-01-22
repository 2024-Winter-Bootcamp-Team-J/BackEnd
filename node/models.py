from django.db import models
from django.conf import settings

class Node(models.Model):
    node_id = models.BigAutoField(primary_key=True)  # Primary Key로 BigInt 타입
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)  # 이름, 최대 길이 50
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각, 자동 생성
    is_deleted = models.BooleanField(default=False)  # 삭제 여부 (기본값: False)
    deleted_at = models.DateTimeField(null=True, blank=True)  # 삭제 시각 (Null 가능)
    node_img = models.URLField(max_length=255, null=True, blank=True) # 이미지 링크 (최대 길이 255)

    def __str__(self):
        return self.name
