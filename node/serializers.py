from rest_framework import serializers
from .models import Node

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['name']

# Node 이미지 추가 시 데이터를 처리하는 Serializer
class NodeImageUpdateSerializer(serializers.ModelSerializer):
    node_id = serializers.IntegerField(required=True)

    class Meta:
        model = Node
        fields = ['node_id','node_img']

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
