from rest_framework import serializers
from .models import Node

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    node_img = serializers.ImageField(required=True, use_url=True)

    class Meta:
        model = Node
        fields = ['name', 'node_img']

    def to_representation(self, instance):
        """
        `node_img` 필드가 URL로 직렬화되도록 보장합니다.
        """
        representation = super().to_representation(instance)
        if instance.node_img:
            representation['node_img'] = instance.node_img.url  # 이미지 필드를 URL로 변환
        return representation

# Node 전체 조회 시 응답 데이터를 처리하는 Serializer
class NodeListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'node_img', 'is_deleted', 'created_at']  # 모든 노드의 필드를 정의

# Node 단일 조회 시 응답 데이터를 처리하는 Serializer
class NodeDetailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'node_img', 'is_deleted', 'created_at', 'deleted_at']  # 추가적인 필드
