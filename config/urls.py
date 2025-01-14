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
from django.urls import path
from django.urls import path, include, re_path
from django.http import HttpResponse  # 임시로 홈 페이지 뷰를 작성
def home(request):
    return HttpResponse("Welcome to the Memo App!")  # 간단한 메시지 출력

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('memo.urls')),  # 메모 앱의 URL 연결
    path('api/', include('node.urls')),  # node 앱의 URL 연결
]
