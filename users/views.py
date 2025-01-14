from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer

class UserRegistrationAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # 회원가입은 인증 없이 허용
        return [IsAuthenticated()]  # 다른 요청은 인증 필요

    # 회원가입
    @swagger_auto_schema( # swagger 테스트 설정
        request_body=UserRegisterSerializer,
        responses={201: '회원가입 완료', 400: '잘못된 요청'}
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'user_id': user.user_id,
                'email': user.email,
                'nickname': user.nickname,
                'message': "회원가입이 완료되었습니다."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
