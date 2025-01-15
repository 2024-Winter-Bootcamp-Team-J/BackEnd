from django.contrib import admin
from .models import Node

class NodeAdmin(admin.ModelAdmin):
    # 필드를 지정하여 Admin 화면에서 표시할 항목을 설정
    list_display = ('node_id', 'name', 'created_at', 'is_deleted', 'deleted_at', 'node_img')

admin.site.register(Node, NodeAdmin)
