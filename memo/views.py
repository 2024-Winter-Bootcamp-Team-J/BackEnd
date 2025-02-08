from rest_framework import generics
from .models import Memo
from .serializers import MemoCreateSerializer, MemoResponseSerializer, MemoRetrieveSerializer, NodeMemoRetrieveSerializer
from rest_framework.response import Response
from rest_framework import status

# 메모 생성을 처리하는 뷰
class MemoCreateView(generics.CreateAPIView):
    """
    메모 생성 요청을 처리하는 CreateAPIView입니다.
    """
    queryset = Memo.objects.all()  # Memo 모델의 모든 객체를 대상으로 함
    serializer_class = MemoCreateSerializer  # 요청 데이터를 처리할 직렬화 클래스 지정

    def create(self, request, *args, **kwargs):
        """
        POST 요청 시 메모를 생성하고 성공 메시지를 반환합니다.
        """
        # 직렬화된 데이터를 저장
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        memo = serializer.save()  # 메모 생성
        
        # 성공 응답 데이터 생성
        success_response = MemoResponseSerializer({'status': 'success', 'memo_id': memo.memo_id})
        return Response(success_response.data, status=201)  # 성공 응답 반환

# 특정 메모를 조회하는 뷰
class MemoRetrieveView(generics.RetrieveAPIView):
    """
    특정 메모 조회 요청을 처리하는 RetrieveAPIView입니다.
    """
    queryset = Memo.objects.all()  # Memo 모델의 모든 객체를 대상으로 함
    serializer_class = MemoRetrieveSerializer  # 조회 응답 데이터를 처리할 직렬화 클래스 지정
    lookup_field = 'pk'  # URL에서 메모 ID를 조회하기 위한 필드

class MemoListByUserView(generics.ListAPIView):
    """
    특정 사용자의 메모를 조회하는 ListAPIView입니다.
    """
    def get(self, request, node_id):
        # node_id로 메모 필터링
        memos = Memo.objects.filter(node_id=node_id)

        # 결과가 없는 경우
        if not memos.exists():
            return Response({"message": "No memos found for the given node_id"}, status=status.HTTP_404_NOT_FOUND)

        # 직렬화 후 응답 반환
        serializer = NodeMemoRetrieveSerializer(memos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)