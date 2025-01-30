import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

def category_extract(text, model_id = "ft:gpt-4o-2024-08-06:test::Av6krlJm"):

    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.chat.completions.create(
        model=model_id,
        messages = [
            {"role": "system", "content": "넌 입력된 텍스트를 분석하여 카테고리를 반환하는 ai야"},
            {
                "role": "user",
                "content": (f'{text} \n \
                            위 입력에서 [\'친구\', \'가족\', \'게임\', \'대학동기\', \'직장\'] 중 어느 카테고리에 속할지 분석해서 json으로 반환해 사람이 2명 이상이면 각각 추출해')
            }
        ],
        temperature=0.0,  # 파인튜닝된 모델이 더 정확한 응답을 하도록 설정
        top_p=1.0,  # 다양한 응답을 제한
    )
    
    # 응답 
    choices = response.choices  # .choices로 접근
    message = choices[0].message.content  # 'message' 객체에서 'content'를 직접 접근

    message = json.loads(message)
    print(message) #json 형식 ex: {"category":['가족']}
    return message

#테스트용
#category_extract(input())