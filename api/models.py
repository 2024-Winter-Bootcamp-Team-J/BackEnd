from django.db import models

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

# Django 모델 정의
class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title

# OpenSearch Document 정의
@registry.register_document
class ArticleDocument(Document):
    class Index:
        # OpenSearch 인덱스 이름 설정
        name = 'articles'
        # 인덱싱을 위한 필드 정의
    title = fields.TextField()
    body = fields.TextField()

    class Django:
        model = Article  # 모델과 Document 연결
        fields = [
            'title',
            'body',
        ]
