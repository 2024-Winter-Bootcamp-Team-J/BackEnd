from rest_framework import generics
from .models import Memo
from .serializers import MemoCreateSerializer, MemoResponseSerializer, MemoRetrieveSerializer
from rest_framework.response import Response

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
