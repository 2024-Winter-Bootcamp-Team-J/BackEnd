from controller.tasks import example_task  # 실제 경로를 수정하세요.
result = example_task.delay(4, 6)
print(result.get())  # 결과가 제대로 출력되는지 확인
