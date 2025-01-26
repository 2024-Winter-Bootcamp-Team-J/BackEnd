from opensearchpy.serializer import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Node
from .serializers import NodeCreateSerializer, NodeListResponseSerializer, NodeDetailResponseSerializer, NodeImageUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from utils.s3_utils import upload_to_s3  # upload_to_s3 함수가 utils.py에 정의된 경우
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class NodeCreateView(APIView):
    """
    노드 이름으로 생성하는 API
    """
    @swagger_auto_schema(
        operation_summary="노드 생성",
        request_body=NodeCreateSerializer,  # 시리얼라이저를 그대로 사용
        responses={
            201: openapi.Response('Node 생성 성공', NodeCreateSerializer),
            400: '잘못된 요청 데이터',
        }
    )
    def post(self, request):
        # user_id가 제공되지 않으면 현재 로그인한 사용자로 설정
        if 'user_id' not in request.data:
            request.data['user_id'] = request.user.user_id # 로그인된 사용자 ID

        serializer = NodeCreateSerializer(data=request.data)
        if serializer.is_valid():
            node = serializer.save()
            return Response(
                {"node_id": node.node_id, "name": node.name},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodeImageUpdateView(APIView):
    """
    노드 이미지 추가 API
    """
    parser_classes = (MultiPartParser,FormParser)


    @swagger_auto_schema(
        operation_summary="노드 이미지 추가",
        request_body=NodeImageUpdateSerializer,
        responses={201:"노드이미지 추가 성공", 400:"잘못된 요청"}
    )
    def post(self, request):
        """
        노드 이미지 추가API
        """
        serializer = NodeImageUpdateSerializer(data=request.data)

        if serializer.is_valid():
            node_id = serializer.validated_data['node_id']

            try:
                # 노드가 존재하는지 확인
                node = Node.objects.get(node_id=node_id)

                # 이미지 처리
                node_img = request.FILES.get('node_img')

                if node_img:
                    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                    file_name = f"nodes/{node_img.name}"
                    node_img_url = upload_to_s3(node_img, bucket_name,file_name)
                else:
                    node_img_url = None

                node.node_img = node_img_url
                node.save()

                return Response(
                    {"message" : "노드 이미지 추가 완료", "node_id": node.node_id,'node_img_url': node_img_url},
                    status=status.HTTP_201_CREATED,
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class NodeListView(APIView):
    """
    모든 노드 목록 조회 API
    """
    @swagger_auto_schema(
        operation_summary="노드 목록 조회",
        responses={
            200: openapi.Response(
                '노드 목록 조회 성공',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='노드 ID'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='노드 이름'),
                            'is_deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='삭제 여부'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='생성 시각', format=openapi.FORMAT_DATETIME),
                            'deleted_at': openapi.Schema(type=openapi.TYPE_STRING, description='삭제 시각', format=openapi.FORMAT_DATETIME, nullable=True),
                        }
                    )
                )
            ),
            404: '노드를 찾을 수 없음'
        }
    )
    def get(self, request):
        nodes = Node.objects.filter(is_deleted=False)  # 삭제되지 않은 노드만 조회
        if not nodes.exists():
            return Response({"detail": "No nodes found."}, status=status.HTTP_404_NOT_FOUND)

        # 시리얼라이저로 노드 목록 반환
        serializer = NodeListResponseSerializer(nodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NodeDetailView(APIView):
    """
    특정 노드 조회 API
    """
    @swagger_auto_schema(
        operation_summary="단일 노드 조회",
        responses={
            200: openapi.Response(
                '노드 상세 조회 성공',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='노드 ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='노드 이름'),
                        'is_deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='삭제 여부'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='생성 시각', format=openapi.FORMAT_DATETIME),
                        'deleted_at': openapi.Schema(type=openapi.TYPE_STRING, description='삭제 시각', format=openapi.FORMAT_DATETIME, nullable=True),
                    }
                )
            ),
            404: '노드를 찾을 수 없음'
        }
    )
    def get(self, request, node_id):
        try:
            node = Node.objects.get(node_id=node_id, is_deleted=False)  # 삭제되지 않은 노드만 조회
            # 시리얼라이저로 노드 상세 데이터 반환
            serializer = NodeDetailResponseSerializer(node)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({'detail': 'Node not found'}, status=status.HTTP_404_NOT_FOUND)