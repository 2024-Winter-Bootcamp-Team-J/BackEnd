from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Node
from .serializers import NodeCreateSerializer, NodeListResponseSerializer, NodeDetailResponseSerializer

# Node 생성 처리하는 APIView
class NodeCreateView(APIView):
    """
    노드를 생성하는 API View입니다.
    """
    @swagger_auto_schema(request_body=NodeCreateSerializer, responses={201: NodeCreateSerializer})
    def post(self, request):
        serializer = NodeCreateSerializer(data=request.data)
        if serializer.is_valid():
            node = serializer.save()  # 직렬화된 데이터로 노드를 생성
            return Response(serializer.to_representation(node), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Node 전체 조회 처리하는 APIView
class NodeListView(APIView):
    """
    모든 노드를 조회하는 API View입니다.
    """
    @swagger_auto_schema(responses={200: NodeListResponseSerializer(many=True)})
    def get(self, request):
        nodes = Node.objects.filter(is_deleted=False)  # 삭제되지 않은 노드만 조회
        serializer = NodeListResponseSerializer(nodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Node 단일 조회 처리하는 APIView
class NodeDetailView(APIView):
    """
    단일 노드를 조회하는 API View입니다.
    """
    @swagger_auto_schema(responses={200: NodeDetailResponseSerializer})
    def get(self, request, node_id):
        try:
            node = Node.objects.get(node_id=node_id, is_deleted=False)  # 삭제되지 않은 노드만 조회
            serializer = NodeDetailResponseSerializer(node)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({'error': 'Node not found'}, status=status.HTTP_404_NOT_FOUND)
