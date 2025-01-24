from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from .models import Write
from .serializers import WriteSerializer
from .name_extract_API import name_extract
from search.documents import NodeDocument
from node.models import Node
from memo.models import Memo
from node.serializers import NodeCreateSerializer
from memo.serializers import MemoCreateSerializer
import requests
import os


class ExampleView(APIView):
    def get(self, request):
        # Celery 비동기 작업 호출
        result = example_task.delay(5, 7)
        return Response({'task_id': result.id})


class ControllerView(APIView):

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

            # 그룹(이벤트)별 node 검색 및 생성
            nodes_result = {}
            node_data = {}
            for group, names in extracted_names.items():
                nodes_result[group] = []  # 그룹별 Node 정보를 저장
                for name in names:
                    # Node 검색 (OpenSearch)
                    search_results = NodeDocument.search().query("match", name=name).execute()
                    if search_results.hits:
                        # 검색 결과가 있으면 Node 정보를 저장
                        node_result = search_results[0]
                        node_data = {
                            "name": node_result.name,
                            "node_id": node_result.node_id,
                        }
                        print(node_data)
                    else:
                        node_serializer = NodeCreateSerializer(
                            data={"name": name, "user": write.user.pk, "node_img": None})
                        if node_serializer.is_valid():  # 유효성 검사
                            node_create_result = node_serializer.save()  # 저장
                            node_data = node_serializer.to_representation(node_create_result)["data"]

                            nodes_result[group].append(node_data)
                            print(nodes_result)
                        else:
                            nodes_result[group].append({
                                "error": "노드 생성 실패",
                                "details": node_serializer.errors,
                                "name": name,
                            })

                            # 성공적으로 생성된 노드를 결과에 추가
                    # nodes_result[group].append(node_data)
                    # 메모 생성
                    memo_serializer = MemoCreateSerializer(data={
                        "node": node_data.get("node_id"),
                        "content": write.content,
                    })
                    if memo_serializer.is_valid():
                        memo_serializer.save()
                    else:
                        nodes_result[group].append({
                            "error": "메모 저장 실패",
                            "details": memo_serializer.errors,
                            "name": name,
                        })
                        continue

                    nodes_result[group].append(node_data)

                # 결과 반환
                return Response(
                    {
                        "message": "글 작성, 이름 추출, Node 및 메모 처리 완료",
                        "write": serializer.data,
                        "extracted_names": extracted_names,
                        "nodes": nodes_result,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        writes = Write.objects.all()
        serializer = WriteSerializer(writes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
