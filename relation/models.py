from django_prometheus.models import ExportModelOperationsMixin
from django.db import models
from users.models import User
from node.models import Node

class RelationType(ExportModelOperationsMixin('RelationType'),models.Model):
    """
    관계 타입을 나타내는 모델.
    """
    relation_type_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relation_types',
        null=True,
        blank=True  # user_id를 nullable로 설정
    )
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserNodeRelation(ExportModelOperationsMixin('UserNodeRelation'),models.Model):
    user_node_id = models.BigAutoField(primary_key=True)
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='user_relations')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='node_relations')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    is_canceled = models.BooleanField(default=False)
    relation_type_id = models.ForeignKey(RelationType, on_delete=models.CASCADE)


    def __str__(self):
        return f"UserNodeRelation {self.user_node_id}"


class NodeRelation(ExportModelOperationsMixin('NodeRelation'),models.Model):
    """
    노드 간 관계를 나타내는 모델.
    - 두 노드 간의 관계 정보를 저장
    """
    node_relation_id = models.BigAutoField(primary_key=True)
    from_node_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='from_relations')
    to_node_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='to_relations')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"NodeRelation {self.node_relation_id}"

class UserNodeToType(ExportModelOperationsMixin('UserNodeToType'),models.Model):
    """
    NodeRelation과 RelationType 간의 연결을 나타내는 모델.
    - 특정 관계(NodeRelation)가 어떤 타입(RelationType)에 속하는지 저장
    """
    user_node_id = models.ForeignKey(UserNodeRelation, on_delete=models.CASCADE)
    relation_type_id = models.ForeignKey(RelationType, on_delete=models.CASCADE)

class RelationToType(ExportModelOperationsMixin('RelationToType'),models.Model):
    """
    노드 관계와 관계 타입 연결 모델
    - 특정 노드 간 관계(NodeRelation)가 어떤 관계 타입(RelationType)에 속하는지를 저장.
    - 이 모델은 NodeRelation과 RelationType의 다대다 연결을 가능하게 하며,
      특정 관계(NodeRelation)에 대해 여러 관계 타입(RelationType)을 지정할 수 있도록 지원
    """
    relation_type_id = models.ForeignKey(RelationType,on_delete=models.CASCADE)
    node_relation_id = models.ForeignKey(NodeRelation,on_delete=models.CASCADE)