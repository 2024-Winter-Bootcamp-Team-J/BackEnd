import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

def name_extract(text):
    api_key = os.getenv('OPENAI_API_KEY')
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 입력된 텍스트에서 사람 이름만을 추출하고 이를 그룹화하는 챗봇이야."},
                {
                    "role": "user",
                    "content": f"""{text} json형식으로 아래 규칙에 따라서 추출해줘:
                1. 입력된 문장에서 사람이름이 등장하지 않으면 none이라고 답해야 해.
                2. 만약 여러 명의 사람이 등장한다면, 그들이 같은 활동을 했거나 같은 문맥에서 등장하면 같은 그룹으로 묶어야 해.
                3. 예를 들어 '오전에는 윤서랑 밥을 먹고 오후에는 우민이랑 영화를 봤다' 라는 문장이 주어지면,
                   group1: 윤서, group2: 우민 이 출력이야.
                4. 문장을 잘 분석해서 사람이름을 정확히 식별하고 일반명사와 구분하는 것이 중요해.
                4.1. '밥', '영화'처럼 사람이 아닌 일반 명사는 이름에서 제외해야 해.
                5. 인칭대명사(예: 나, 너, 그, 그녀)는 이름에서 제외해야 해.
                6. 결과는 항상 JSON 형식으로 반환해야 해."""
                }
            ]
        )

        # 응답 데이터 처리
        result = response.choices[0].message.content
        return json.loads(result)  # JSON 형식 파싱 후 반환

    except json.JSONDecodeError:
        raise ValueError("AI 응답이 JSON 형식이 아닙니다.")
    except Exception as e:
        raise ValueError(f"OpenAI 호출 오류: {str(e)}")
