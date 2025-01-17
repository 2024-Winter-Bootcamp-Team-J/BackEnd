from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import NodeRelation, RelationType
from .serializers import (
    RelationTypeSerializer, NodeRelationSerializer, RelationToTypeSerializer
)

class CreateRelationView(APIView):
    """
    관계 생성 API
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'from_node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='시작 노드 ID'),
                'to_node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='끝 노드 ID'),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='사용자 ID'),
                'relation_type_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='관계 타입 ID'),
            },
            required=['from_node_id', 'to_node_id', 'user_id', 'relation_type_id']
        ),
        responses={
            201: openapi.Response('생성된 데이터', NodeRelationSerializer),
            400: '잘못된 요청 데이터'
        }
    )
    def post(self, request):
        serializer = NodeRelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRelationsView(APIView):
    """
    관계 목록 조회 API
    """
    @swagger_auto_schema(
        responses={
            200: openapi.Response('관계 목록', NodeRelationSerializer(many=True))
        }
    )
    def get(self, request):
        relations = NodeRelation.objects.all()
        serializer = NodeRelationSerializer(relations, many=True)
        return Response(serializer.data)


class CreateRelationTypeView(APIView):
    """
    관계 타입 생성 API
    """
    @swagger_auto_schema(
        request_body=RelationTypeSerializer,
        responses={
            201: openapi.Response('생성된 관계 타입', RelationTypeSerializer),
            400: '잘못된 요청 데이터'
        }
    )
    def post(self, request):
        serializer = RelationTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRelationTypesView(APIView):
    """
    관계 타입 목록 조회 API
    """
    @swagger_auto_schema(
        responses={
            200: openapi.Response('관계 타입 목록', RelationTypeSerializer(many=True))
        }
    )
    def get(self, request):
        relation_types = RelationType.objects.all()
        serializer = RelationTypeSerializer(relation_types, many=True)
        return Response(serializer.data)


class GetRelationTypeView(APIView):
    """
    특정 관계 타입 조회 API
    """
    @swagger_auto_schema(
        responses={
            200: openapi.Response('관계 타입 데이터', RelationTypeSerializer),
            404: '데이터를 찾을 수 없음'
        }
    )
    def get(self, request, pk):
        try:
            relation_type = RelationType.objects.get(pk=pk)
        except RelationType.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RelationTypeSerializer(relation_type)
        return Response(serializer.data)
