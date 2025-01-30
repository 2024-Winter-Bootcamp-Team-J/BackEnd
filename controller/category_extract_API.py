import openai
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()


def category_extract(text, model_id="ft:gpt-4o-2024-08-06:test::Av6krlJm"):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    try:
        start_time = time.time()  # 시작 시간 기록

        response = openai.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "넌 입력된 텍스트를 분석하여 카테고리를 반환하는 ai야"},
                {
                    "role": "user",
                    "content": (f'{text} \n \
                                위 입력에서 [\'친구\', \'가족\', \'게임\', \'대학동기\', \'직장\'] 중 어느 카테고리에 속할지 분석해서 json으로 반환해')
                }
            ],
            temperature=0.0,
            top_p=1.0,
        )

        end_time = time.time()  # 응답 시간 기록
        duration = end_time - start_time
        print(f"API 호출 완료, 응답 시간: {duration}초")  # 응답 시간 로그 추가

        choices = response.choices
        message = choices[0].message.content
        message = json.loads(message)
        print(message)
        return message

    except Exception as e:
        print(f"카테고리 추출 오류: {str(e)}")
        return {"error": "카테고리 추출 실패", "details": str(e)}
#테스트용
#category_extract(input())