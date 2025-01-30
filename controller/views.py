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
from .tasks import category_extract_task
from relation.models import RelationType
import requests
import os
import json


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
                input_text = write.content
                # 비동기 작업에서 카테고리 추출
                category = category_extract(input_text)
                if 'error' in category:
                    # 카테고리 추출 실패 처리
                    return Response(
                        {"error": f"카테고리 추출 실패: {category['details']}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                extracted_names = name_extract(input_text)
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
                    try:
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
                                data={"name": name, "user_id": write.user.pk})
                            if node_serializer.is_valid():  # 유효성 검사
                                node_create_result = node_serializer.save()  # 저장
                                node_data = node_serializer.to_representation(node_create_result)["data"]
                            else:
                                nodes_result[group].append({
                                    "error": "노드 생성 실패",
                                    "details": node_serializer.errors,
                                    "name": name,
                                })
                    except Exception as e:
                        print(f"첫 검색이면 들어오는 except")
                        node_serializer = NodeCreateSerializer(
                            data={"name": name, "user_id": write.user.pk})
                        if node_serializer.is_valid():  # 유효성 검사
                            node_create_result = node_serializer.save()  # 저장
                            print(node_serializer.to_representation(node_create_result))
                            node_data = node_serializer.to_representation(node_create_result)["data"]
                        else:
                            nodes_result[group].append({
                                "error": "노드 생성 실패",
                                "details": node_serializer.errors,
                                "name": name,
                            })

                    # 성공적으로 생성된 노드를 결과에 추가
                    nodes_result[group].append(node_data)

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

            try:
                type_name = category.get()['category']
                print(f'type_name: {type_name}')
                type_id = RelationType.objects.filter(name=type_name[0]).values("relation_type_id")[0]
                return Response(
                    {
                        "message": "글 작성, 이름 추출, Node 및 메모 처리 완료",
                        "write": serializer.data,
                        "extracted_names": extracted_names,
                        "nodes": nodes_result,
                        "category": [json.loads('{"type_name": "' + type_name[0] + '"}'), type_id]
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                print(f"예외 발생: {str(e)}")
                return Response({"error": f"카테고리 처리 중 오류 발생: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        writes = Write.objects.all()
        serializer = WriteSerializer(writes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
