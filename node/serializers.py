from rest_framework import serializers
from .models import Node

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['name', 'node_img']  # 생성 시 필요한 필드

    def create(self, validated_data):
        # Node 객체를 생성하고 저장합니다.
        node = Node.objects.create(**validated_data)
        # 생성된 Node 객체를 반환합니다.
        return node

    def to_representation(self, instance):
        # 응답 데이터 포맷을 정의합니다.
        return {
            "message": "Node created successfully",
            "data": {
                "id": instance.node_id,
                "name": instance.name,
                "node_img": instance.node_img,
                "is_deleted": instance.is_deleted,
                "created_at": instance.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
        }

# Node 전체 조회 시 응답 데이터를 처리하는 Serializer
class NodeListResponseSerializer(serializers.Serializer):
    nodes = NodeCreateSerializer(many=True)

    def to_representation(self, instance):
        return {
            "nodes": instance
        }

# Node 단일 조회 시 응답 데이터를 처리하는 Serializer
class NodeDetailResponseSerializer(serializers.Serializer):
    node = NodeCreateSerializer()

    def to_representation(self, instance):
        return {
            "node": instance
        }
