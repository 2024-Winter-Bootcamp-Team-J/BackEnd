from rest_framework import serializers
from users.models import User
from .models import Node
from relation.models import UserNodeRelation

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)  # user_id만 사용
    class Meta:
        model = Node
        fields = ['name', 'user_id']  # user_id만 반환

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        user = None
        if user_id:
            try:
                # user_id로 User 객체를 찾음
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid user_id provided.")
        # Node 객체 생성 시 user 객체를 연결
        node = Node.objects.create(
            name=validated_data['name'],
            user=user  # user 객체 할당
        )
        return node
    
    def to_representation(self, instance):
        # 응답 데이터 포맷을 정의합니다.
        return {
            "message": "Node created successfully",
            "data": {
                "node_id": instance.node_id,
                "user_id": instance.user.user_id,
                "name": instance.name,
                "node_img": instance.node_img,
                "is_deleted": instance.is_deleted,
                "created_at": instance.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
        }

# Node 이미지 추가 시 데이터를 처리하는 Serializer
class NodeImageUpdateSerializer(serializers.ModelSerializer):
    node_id = serializers.IntegerField(required=True)
    node_img = serializers.ImageField(required=False)
    user_id = serializers.IntegerField(required=False)  # user_id만 사용

    class Meta:
        model = Node
        fields = ['node_id', 'node_img', 'user_id']  # user_id만 반환

# Node 전체 조회 시 응답 데이터를 처리하는 Serializer
class NodeListResponseSerializer(serializers.ModelSerializer):
    relation_type_ids = serializers.SerializerMethodField()  # 동적 필드를 위한 SerializerMethodField 사용


    class Meta:
        model = Node
        fields = ['node_id', 'name', 'node_img', 'is_deleted', 'created_at', 'relation_type_ids']

    def get_relation_type_ids(self, node):
        # UserNodeRelation에서 user_node_id 조회
        relation_type_ids = UserNodeRelation.objects.filter(node_id=node.node_id).values_list('relation_type_id', flat=True)
        # 로그 확인
        print(f"Relation type IDs for node_id {node.node_id}: {relation_type_ids}")
        return list(relation_type_ids)  # relation_type_id 리스트 반환

# Node 단일 조회 시 응답 데이터를 처리하는 Serializer
class NodeDetailResponseSerializer(NodeListResponseSerializer):
    # 단일 조회는 NodeListResponseSerializer를 상속받아 그대로 사용
    pass
