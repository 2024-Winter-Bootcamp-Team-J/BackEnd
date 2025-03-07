# search/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import MemoDocument  # MemoDocument를 import하여 사용
from .documents import NodeDocument  # NodeDocument를 import하여 사용
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class SearchView(APIView):
    """
        Opensearch에서 memo_content와 node_name을을 검색하는 API 뷰입니다.
    """
    # swaaager_auto_schema 데코레이터를 사용하여 query 테스트트
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'query',
                openapi.IN_QUERY,
                description="Search term",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    # GET 요청을 처리하는 함수
    def get(self, request):
        query = request.GET.get('query',None)  # GET 파라미터로 검색어를 받음
        if not query:
            return JsonResponse({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # opensearch에서 검색 실행
        memo_results = MemoDocument.search().query('wildcard', content=f'*{query}*').execute()
        print(f'memo_results: {memo_results}')
        # 검색 결과를 합쳐서 정렬
        
        # 검색된 결과를 직렬화하여 반환
        results = []
        results.extend(
            {
                'memo_id': result.memo_id,
                'node_id': result.node_id,
                'content': result.content,
                'created_at': result.created_at,
                'is_deleted': result.is_deleted,
            }
            for result in memo_results
        )
        
        # 검색결과가 없는 경우 404 에러를 반환
        if results == []:
            return JsonResponse({'error': 'No results found.'}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'results': results}, status=status.HTTP_200_OK)
