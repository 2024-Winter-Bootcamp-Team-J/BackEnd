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
    def post(self, request):
        # 요청 데이터를 역직렬화(deserialize)하고 검증합니다.
        serializer = NodeCreateSerializer(data=request.data)
        if serializer.is_valid():  # 데이터가 유효한지 확인
            # 새 노드를 생성하고 반환합니다.
            node = serializer.save()  # 직렬화된 데이터로 노드를 생성
            return Response(serializer.to_representation(node), status=status.HTTP_201_CREATED)  # HTTP 201 Created 응답
        # 데이터가 유효하지 않을 경우 오류 메시지를 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # HTTP 400 Bad Request

# Node 전체 조회 처리하는 APIView
class NodeListView(APIView):
    """
    모든 노드를 조회하는 API View입니다.
    """
    def get(self, request):
        # 모든 노드 객체를 가져옵니다.
        nodes = Node.objects.filter(is_deleted=False)  # 삭제되지 않은 노드만 조회
        # 노드들을 직렬화합니다.
        serializer = NodeListResponseSerializer(nodes)
        return Response(serializer.to_representation(serializer.data), status=status.HTTP_200_OK)  # HTTP 200 OK 응답

# Node 단일 조회 처리하는 APIView
class NodeDetailView(APIView):
    """
    단일 노드를 조회하는 API View입니다.
    """
    def get(self, request, node_id):
        try:
            # node_id로 특정 노드를 찾습니다.
            node = Node.objects.get(node_id=node_id, is_deleted=False)  # 삭제되지 않은 노드만 조회
            # 노드를 직렬화합니다.
            serializer = NodeDetailResponseSerializer(node)
            return Response(serializer.to_representation(serializer.data), status=status.HTTP_200_OK)  # HTTP 200 OK 응답
        except Node.DoesNotExist:
            # 노드가 없으면 404 Not Found 응답을 반환합니다.
            return Response({'error': 'Node not found'}, status=status.HTTP_404_NOT_FOUND)
