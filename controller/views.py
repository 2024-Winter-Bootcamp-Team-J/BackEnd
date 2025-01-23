from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Write
from .serializers import WriteSerializer
from .name_extract_API import name_extract

class WriteCreateView(APIView):
    def get(self, request):
        writes = Write.objects.all()
        serializer = WriteSerializer(writes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=WriteSerializer,
        responses={
            201: WriteSerializer,
            400: openapi.Response(description="유효성 검사 실패")
        }
    )

    def post(self, request):
        serializer = WriteSerializer(data=request.data)
        if serializer.is_valid():
            write = serializer.save()
            try:
                extracted_names = name_extract(write.content)
            except ValueError as e:
                return Response(
                    {"error": f"이름 추출 실패: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

                # 저장된 데이터와 이름 추출 결과 반환
            return Response(
                {
                    "message": "글 작성 및 이름 추출 완료",
                    "write": serializer.data,
                    "extracted_names": extracted_names,
                },
                status=status.HTTP_201_CREATED,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
