from django.contrib import admin
from .models import RelationType, NodeRelation, UserNodeRelation, UserNodeToType, RelationToType

class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ('relation_type_id', 'user_id', 'name', 'is_default', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_default',)

class NodeRelationAdmin(admin.ModelAdmin):
    list_display = ('node_relation_id', 'from_node_id', 'to_node_id', 'user_id', 'is_active', 'created_at')
    search_fields = ('user_id', 'from_node_id', 'to_node_id')
    list_filter = ('is_active',)

class UserNodeRelationAdmin(admin.ModelAdmin):
    list_display = ('user_node_id', 'node_id', 'user_id', 'is_canceled', 'canceled_at')
    search_fields = ('user_id', 'node_id')
    list_filter = ('is_canceled',)

class UserNodeToTypeAdmin(admin.ModelAdmin):
    list_display = ('user_node_id', 'relation_type_id')
    search_fields = ('user_node_id', 'relation_type_id')

class RelationToTypeAdmin(admin.ModelAdmin):
    list_display = ('relation_type_id', 'node_relation_id')
    search_fields = ('relation_type_id', 'node_relation_id')

# 모델을 관리 사이트에 등록
admin.site.register(RelationType, RelationTypeAdmin)
admin.site.register(NodeRelation, NodeRelationAdmin)
admin.site.register(UserNodeRelation, UserNodeRelationAdmin)
admin.site.register(UserNodeToType, UserNodeToTypeAdmin)
admin.site.register(RelationToType, RelationToTypeAdmin)
