# search/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import MemoDocument  # MemoDocument를 import하여 사용
from django.http import JsonResponse

class MemoSearchView(APIView):
    """
    Elasticsearch에서 메모를 검색하는 API 뷰입니다.
    """
    def get(self, request):
        query = request.GET.get('query', '')  # GET 파라미터로 검색어를 받음
        if not query:
            return JsonResponse({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Elasticsearch에서 검색 실행
        search_results = MemoDocument.search().query('match', content=query)

        # 검색된 결과를 직렬화하여 반환
        results = []
        results.extend(
            {
                'memo_id': result.memo_id,
                'content': result.content,
                'created_at': result.created_at,
                'is_deleted': result.is_deleted,
            }
            for result in search_results
        )
        return JsonResponse({'results': results}, status=status.HTTP_200_OK)
