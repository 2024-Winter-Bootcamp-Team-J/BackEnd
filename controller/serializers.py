from rest_framework import serializers
from .models import Write
from django.contrib.auth import get_user_model

class WriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)  # 내용 필수 필드

    class Meta:
        model = Write
        fields = ['controller_id', 'user_id', 'content', 'created_at']  # 필요한 필드만 정의
        read_only_fields = ['controller_id', 'created_at']  # 읽기 전용 필드

    def create(self, validated_data):
        # user_id를 User 인스턴스로 변환
        User = get_user_model()
        try:
            user_instance = User.objects.get(pk=validated_data.pop('user_id'))
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "유효하지 않은 사용자 ID입니다."})

        # Write 객체 생성
        return Write.objects.create(user=user_instance, content=validated_data['content'])

    def to_representation(self, instance):
        # 응답 데이터 포맷을 정의합니다.
        return {
            "message": "Written successfully",
            "data": {
                "controller_id": instance.controller_id,
                "user_id": instance.user.user_id,
                "content": instance.content,
                "created_at": instance.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
        }
