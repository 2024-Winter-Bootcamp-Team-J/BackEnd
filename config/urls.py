"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse  # 임시로 홈 페이지 뷰를 작성
from django.conf.urls.static import static
from django.conf import settings

def home(request):
    return HttpResponse("Welcome to the homepage!")

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="LinkIn",
        default_version='v1',
        description="자동생성 인간관계도 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

    url='https://api.link-in.site'  # Base URL 강제 설정

)

# Swagger에서 jwt 인증 관련
AUTH_HEADER = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="JWT Authorization header. Example: 'Bearer <token>'",
    type=openapi.TYPE_STRING
)

schema_view.with_ui("swagger", cache_timeout=0)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home),  # 루트 URL에 홈 페이지 뷰 연결
    path('memos', include('memo.urls')),
    path('node', include('node.urls')),  # node 앱의 URL 연결
    path('users', include('users.urls')),
    path('search', include('search.urls')), # search 앱의 URL을 포함
    path('controller', include('controller.urls')),
    path('relations', include('relation.urls')),  # relation 앱의 URL 연결
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # JWT 인증 관련 URL
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)