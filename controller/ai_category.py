import openai

# OpenAI API 키 설정
openai.api_key = "your-api-key"

# 파일 업로드 함수
def upload_file(file_path, purpose="fine-tune"):
    """
    OpenAI 파일 시스템에 파일을 업로드합니다.

    :param file_path: 업로드할 파일 경로
    :param purpose: 파일 사용 목적 (예: 'fine-tune', 기본값: 'fine-tune')
    :return: 업로드된 파일의 ID
    """
    try:
        # 파일 업로드
        response = openai.File.create(
            file=open(file_path, "rb"),  # 파일 열기
            purpose=purpose              # 파일 목적 설정
        )
        # 성공 시 파일 ID 반환
        print(f"파일 업로드 성공: {response['id']}")
        return response["id"]
    except Exception as e:
        print(f"파일 업로드 실패: {e}")
        return None


# 파일 경로 지정
file_path = "category.jsonl"  # JSONL 형식의 데이터 파일
uploaded_file_id = upload_file(file_path)

# 업로드된 파일 ID 출력
if uploaded_file_id:
    print(f"업로드된 파일 ID: {uploaded_file_id}")
else:
    print("파일 업로드에 실패했습니다.")
