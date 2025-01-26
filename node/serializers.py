from rest_framework import serializers
from users.models import User
from .models import Node

# Node 생성 시 응답 데이터를 처리하는 Serializer
class NodeCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField( required=False)  # user_id만 사용
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
    user_id = serializers.IntegerField(required=False)  # user_id만 사용
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'is_deleted', 'created_at', 'user_id']  # user_id만 반환

# Node 단일 조회 시 응답 데이터를 처리하는 Serializer
class NodeDetailResponseSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)  # user_id만 사용
    class Meta:
        model = Node
        fields = ['node_id', 'name', 'is_deleted', 'created_at', 'deleted_at', 'user_id']  # user_id만 반환
