# Generated by Django 3.2.25 on 2025-01-15 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
