from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Node
from .serializers import NodeCreateSerializer, NodeListResponseSerializer, NodeDetailResponseSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from utils.s3_utils import upload_to_s3  # upload_to_s3 함수가 utils.py에 정의된 경우

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser

class NodeCreateView(APIView):
    """
    노드 생성 API (파일 업로드 포함)
    """
    parser_classes = [MultiPartParser]  # 파일 업로드를 처리하기 위해 MultiPartParser 추가

    @swagger_auto_schema(
        operation_summary="노드 생성",
        operation_description="노드 생성 및 S3에 이미지 업로드",
        request_body=NodeCreateSerializer,  # 시리얼라이저를 그대로 사용
        responses={
            201: openapi.Response(
                'Node 생성 성공',
                NodeCreateSerializer  # 응답 데이터도 시리얼라이저를 사용
            ),
            400: '잘못된 요청 데이터',
        }
    )
    def post(self, request):
        # 시리얼라이저로 요청 데이터 유효성 검사
        serializer = NodeCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 파일 업로드 로직
            node_img = request.FILES.get('node_img')
            if node_img:
                # S3에 업로드된 이미지 파일의 URL 얻기
                file_name = f"nodes/{node_img.name}"
                s3_url = upload_to_s3(node_img, settings.AWS_STORAGE_BUCKET_NAME, file_name)
                # serializer에 S3 URL 저장
                serializer.validated_data['node_img'] = s3_url
            else:
                return Response({"detail": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

            # 노드 생성 및 반환
            node = serializer.save()
            return Response(
                serializer.data,  # 시리얼라이저 데이터 반환 (S3 URL 포함)
                status=status.HTTP_201_CREATED,
            )

        # 유효성 검사 실패 시 에러 응답 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodeListView(APIView):
    """
    모든 노드 목록 조회 API
    """
    @swagger_auto_schema(
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
                            'node_img': openapi.Schema(type=openapi.TYPE_STRING, description='노드 이미지 URL', format=openapi.FORMAT_URI),
                            'is_deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='삭제 여부'),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='생성 시각', format=openapi.FORMAT_DATETIME),
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
        responses={
            200: openapi.Response(
                '노드 상세 조회 성공',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'node_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='노드 ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='노드 이름'),
                        'node_img': openapi.Schema(type=openapi.TYPE_STRING, description='노드 이미지 URL', format=openapi.FORMAT_URI),
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
