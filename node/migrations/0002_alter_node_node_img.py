# Generated by Django 4.2.18 on 2025-01-20 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='node_img',
            field=models.ImageField(blank=True, null=True, upload_to='node_images/'),
        ),
    ]
