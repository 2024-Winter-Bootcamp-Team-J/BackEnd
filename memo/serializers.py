from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Memo

# 메모 생성 요청과 응답을 처리하기 위한 Serializer
class MemoCreateSerializer(serializers.Serializer):
    """
    메모 생성을 위한 요청 데이터를 처리하는 Serializer입니다.
    """
    node_id = serializers.IntegerField()  # 메모를 생성할 사용자 ID
    content = serializers.CharField()  # 메모 내용
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d-%H-%M-%S", read_only=True
    )  # 생성 시각(자동 생성, 읽기 전용)

# 메모 생성 성공 시 반환되는 응답을 처리하기 위한 Serializer
class MemoResponseSerializer(serializers.Serializer):
    """
    메모 생성 성공 시 반환하는 응답 데이터 구조를 정의하는 Serializer입니다.
    """
    status = serializers.CharField(default="success")  # 성공 상태 메시지(기본값: 'success')

# 메모 조회 요청에 대한 응답을 처리하기 위한 Serializer
class MemoRetrieveSerializer(serializers.Serializer):
    """
    메모 조회 요청에 대한 응답 데이터를 처리하는 Serializer입니다.
    """
    content = serializers.CharField()  # 메모 내용
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d-%H-%M-%S"
    )  # 생성 시각('yyyy-mm-dd-hh-mm-ss' 형식)

# 메모 생성을 처리하는 API View
class MemoCreateView(APIView):
    """
    메모 생성 요청을 처리하는 API View입니다.
    """
    def post(self, request):
        # 요청 데이터를 역직렬화(deserialize)하고 검증합니다.
        serializer = MemoCreateSerializer(data=request.data)
        if serializer.is_valid():  # 데이터가 유효한지 확인
            # 데이터베이스에 새 메모를 생성합니다.
            Memo.objects.create(
                user_id=serializer.validated_data['user_id'],  # 사용자 ID
                content=serializer.validated_data['content']  # 메모 내용
            )
            # 성공 응답 데이터를 반환합니다.
            response = MemoResponseSerializer({'status': 'success'})
            return Response(response.data, status=201)  # HTTP 201 Created
        # 데이터가 유효하지 않을 경우 오류 메시지를 반환합니다.
        return Response(serializer.errors, status=400)  # HTTP 400 Bad Request

# 메모 조회를 처리하는 API View
class MemoRetrieveView(APIView):
    """
    메모 조회 요청을 처리하는 API View입니다.
    """
    def get(self, request, pk):
        try:
            # primary key(메모 ID)를 사용하여 메모를 검색합니다.
            memo = Memo.objects.get(pk=pk)
            # 검색된 메모 데이터를 직렬화(serialize)합니다.
            serializer = MemoRetrieveSerializer({
                'content': memo.content,  # 메모 내용
                'created_at': memo.created_at  # 생성 시각
            })
            # 직렬화된 데이터를 반환합니다.
            return Response(serializer.data, status=200)  # HTTP 200 OK
        except Memo.DoesNotExist:
            # 메모가 존재하지 않을 경우 처리합니다.
            return Response({'error': 'Memo not found'}, status=404)  # HTTP 404 Not Found
