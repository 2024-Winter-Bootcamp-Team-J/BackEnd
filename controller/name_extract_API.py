import openai
import os
from dotenv import load_dotenv
load_dotenv()
import json

# API 키 설정
def name_extract(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "입력된 텍스트에서 사람 이름을 그룹화 하여 json으로 출력해"},
            {"role": "user", "content": f'{text}\n \
            위 입력을 아래 규칙을 하나도 어기지 말고 따라서 응답해줘. \
            1. 입력에서 사람이름이 등장하지 않으면 none이라고 응답해.\n \
            2. 만약 여러 명의 사람이 등장한다면, 그들이 같은 활동을 했거나 같은 문맥에서 등장하면 같은 그룹으로 묶어.\n \
            3. 문장을 잘 분석해서 사람이름을 정확히 식별하고 일반명사와 구분하여 사람이름을 반환하는 것이 중요해.\n \
            4  밥, 영화처럼 사람이 아닌 일반 명사는 이름에서 제외해.\n \
            5. 인칭대명사(예: 나, 너, 그, 그녀)는 이름에서 제외해.\n \
            6. 응답을 바로 json.loads(message)에 message로 사용할 수 있게 JSON으로 출력해.\n \
            7. 사용자의 입력을 받아 이름을 추출해서 아래 예시의 형식대로 응답해.\n \
            8. <입력>은 사용자의 입력이야.\n \
            <입력> 윤서랑 우민이랑 밥을 먹었다.\n \
            "group1": ["윤서", "우민"] \n \
            <입력> 오전에는 지훈이랑, 저녁은 세영이랑 밥을 먹었다.\n \
            "group1": "지훈", "group2": "세영" \n \
            <입력> 나는 오늘 밥을 먹었다.\n \
            "group1": none \n \
            <입력> 윤서랑 영화를 봤다.\n \
            "group1": "윤서" \n \
            <입력> 민수랑 밥을 먹고 소연이랑 도서관에 갔다.\n \
            "group1": ["민수", "소연"] \n \
            <입력> 윤아랑 밥을 먹고 준호랑 영화를 봤다.\n \
            "group1": "윤아", "group2": "준호" \n \
            <입력> 영희랑 철수와 같이 놀이공원에 가고 집에 오다가 민호를 만났다.\n \
            "group1": ["영희", "철수"], "group2": "민호"" '}]
    )

    result = response.choices[0].message.content
    return json.loads(result)  # JSON 형식 파싱 후 반환

# 테스트용
# name_extract(input())