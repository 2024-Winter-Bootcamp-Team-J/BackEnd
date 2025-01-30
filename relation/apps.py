from django.apps import AppConfig
from django.db.models.signals import post_migrate

class RelationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relation'

    def ready(self):
        from .models import RelationType
        from django.db import connection

        def create_default_relation_types(sender, **kwargs):
            if 'relation_relationtype' in connection.introspection.table_names():
                default_types = ['친구', '가족', '게임', '대학동기', '직장']
                for name in default_types:
                    RelationType.objects.get_or_create(name=name, user_id=None, is_default=True)

        post_migrate.connect(create_default_relation_types, sender=self)
