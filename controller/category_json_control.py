import openai
import os
from dotenv import load_dotenv

load_dotenv()
# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# 파일 삭제 함수
def delete_file(file_id):
    """
    OpenAI 파일 시스템에서 파일을 삭제합니다.

    :param file_id: 삭제할 파일의 ID
    """
    try:
        response = openai.files.delete(file_id=file_id)
        print(f"파일 삭제 성공: {response}")
    except Exception as e:
        print(f"파일 삭제 실패: {e}")

# 파일 업로드 함수
def upload_file(file_path, purpose="fine-tune"):
    """
    :param file_path: 업로드할 파일 경로
    :param purpose: 파일 사용 목적 (예: 'fine-tune', 기본값: 'fine-tune')
    :return: 업로드된 파일의 ID
    """
    try:
        with open(file_path, "rb") as file:
            response = openai.files.create(
                file=file,
                purpose=purpose
            )
        print(f"파일 업로드 성공")
        return response
    except Exception as e:
        print(f"파일 업로드 실패: {e}")
        return None

# 업로드된 파일 목록 가져오기 함수
def list_uploaded_files():
    """
    OpenAI 파일 시스템에 업로드된 파일 목록을 가져옵니다.
    """
    try:
        response = openai.files.list()  # 수정된 부분: `openai.files.list()`
        files = response.data

        if files:
            print("업로드된 파일 목록:")
            for file in files:
                print(file)
        else:
            print("업로드된 파일이 없습니다.")

        return files
    except Exception as e:
        print(f"파일 목록 가져오기 실패: {e}")
        return []

# category.json 파일 업데이트 함수
def category_json_update():
    # 파일 목록 출력
    uploaded_files = list_uploaded_files()

    # 특정 파일 찾기 (예: 파일 이름으로 검색)
    file_name_to_find = "category.jsonl"  # 찾고자 하는 파일 이름
    try:
        for file in uploaded_files:
            if file.filename == file_name_to_find:
                old_file_id = file.id
                print(f"찾은 파일 ID: {old_file_id}")
                delete_file(old_file_id)
    except Exception as e:
        print("삭제하기 위한 중복 파일 찾기 중 오류")
        return
    # 새 파일 경로
    new_file_path = "/code/controller/category.jsonl"

    # 새로운 파일 업로드
    response = upload_file(new_file_path)

    return response.id
    

