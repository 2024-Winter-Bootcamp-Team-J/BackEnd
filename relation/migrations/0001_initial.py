from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('node', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeRelation',
            fields=[
                ('node_relation_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_relations', to='node.node')),
                ('to_node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_relations', to='node.node')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('relation_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('is_default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relation_types', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNodeRelation',
            fields=[
                ('user_node_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('is_canceled', models.BooleanField(default=False)),
                ('node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relations', to='node.node')),
                ('relation_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relation.relationtype')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_relations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNodeToType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relation.relationtype')),
                ('user_node_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relation.usernoderelation')),
            ],
        ),
        migrations.CreateModel(
            name='RelationToType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_relation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relation.noderelation')),
                ('relation_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relation.relationtype')),
            ],
        ),
    ]
