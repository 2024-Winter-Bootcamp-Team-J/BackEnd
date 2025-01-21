from rest_framework import serializers
from .models import Write

class WriteSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)  # 내용 필수 필드

    class Meta:
        model = Write
        fields = ['id', 'content', 'created_at']  # 필요한 필드만 정의
        read_only_fields = ['id', 'created_at']  # 읽기 전용 필드