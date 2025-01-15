from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse  # 임시로 홈 페이지 뷰를 작성

# 루트 URL에 대한 간단한 응답을 추가
def home(request):
    return HttpResponse("Welcome to the homepage!")

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="프로젝트명",
        default_version='v1',
        description="자동생성 인간관계도 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # 루트 URL에 홈 페이지 뷰 연결
    path('api/', include('memo.urls')),  # memo 앱의 URL 연결
    path('api/', include('node.urls')),  # node 앱의 URL 연결
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
