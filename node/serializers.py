from rest_framework import serializers
from .models import Node
from django.contrib.auth import get_user_model

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=True)
    class Meta:
        model = Node
        fields = ['name', 'node_img', 'user']  # 생성 시 필요한 필드

    def create(self, validated_data):
        User = get_user_model()
        try:
            user_instance = User.objects.get(pk=validated_data.pop('user'))
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "유효하지 않은 사용자 ID입니다."})

        # Node 객체를 생성하고 저장합니다.
        node = Node.objects.create(user=user_instance, **validated_data)
        # 생성된 Node 객체를 반환합니다.
        return node

    def to_representation(self, instance):
        # 응답 데이터 포맷을 정의합니다.
        return {
            "message": "Node created successfully",
            "data": {
                "node_id": instance.node_id,
                "user": instance.user.user_id,
                "name": instance.name,
                "node_img": instance.node_img,
                "is_deleted": instance.is_deleted,
                "created_at": instance.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
        }

# Node 전체 조회 시 응답 데이터를 처리하는 Serializer
class NodeListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'node_img', 'is_deleted', 'created_at']  # 모든 노드의 필드를 정의

    def to_representation(self, instance):
        # 응답 데이터 포맷을 정의합니다.
        return {
            "node_id": instance.node_id,
            "name": instance.name,
            "node_img": instance.node_img,
            "is_deleted": instance.is_deleted,
            "created_at": instance.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
        }

# Node 단일 조회 시 응답 데이터를 처리하는 Serializer
class NodeDetailResponseSerializer(NodeListResponseSerializer):
    # 단일 조회는 NodeListResponseSerializer를 상속받아 그대로 사용
    pass
