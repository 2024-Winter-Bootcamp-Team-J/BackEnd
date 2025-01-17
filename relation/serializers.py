from rest_framework import serializers
from .models import RelationType, NodeRelation, RelationToType

# serializers.py

class RelationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationType
        fields = ('relation_type_id', 'user_id', 'name', 'is_default', 'created_at')


class NodeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeRelation
        fields = ('node_relation_id', 'from_node_id', 'to_node_id', 'user_id', 'is_active', 'created_at')


class RelationToTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationToType
        fields = ('relation_type_id', 'node_relation_id')