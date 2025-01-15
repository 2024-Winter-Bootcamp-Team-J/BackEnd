from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .user_service import register_user, login_user
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

class UserRegistrationAPIView(APIView):
    # multipart 파서를 추가합니다.
    parser_classes = (MultiPartParser, FormParser)
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # 회원가입은 인증 없이 허용
        return [IsAuthenticated()]  # 다른 요청은 인증 필요

    # 회원가입
    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={201: '회원가입 완료', 400: '잘못된 요청'},
    )
    def post(self, request):
        """
        회원가입 API
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = register_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    nickname=serializer.validated_data['nickname'],
                    profile_img_file=request.FILES.get('profile_img'),
                )
                return Response(
                    {"message": "회원가입이 완료되었습니다.", "user_id": user.user_id},
                    status=status.HTTP_201_CREATED,
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    # 로그인
    @swagger_auto_schema(  # swagger 테스트 설정
        request_body=UserLoginSerializer,
        responses={201: '로그인 완료', 400: '잘못된 요청'}
    )
    def post(self, request):
        """
        로그인 API
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = login_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                )
                return Response(
                    {"message": "로그인 성공", "user_id": user.user_id, "nickname": user.nickname},
                    status=status.HTTP_200_OK,
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)