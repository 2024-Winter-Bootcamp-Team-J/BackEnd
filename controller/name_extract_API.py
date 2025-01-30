import openai
import os
from dotenv import load_dotenv
import json
load_dotenv()


def name_extract(text):

    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages = [
            {"role": "system", "content": "입력된 텍스트에서 사람 이름을 그룹화하여 json으로 출력해"},
            {
                "role": "user",
                "content": (
                    f"{text}\n"
                    "다음 텍스트에서 사람 이름을 그룹화하여 JSON 형식으로 출력해줘. 반드시 아래 규칙을 따라야 해.\n\n"
                    "1. '나'라는 화자가 입력을 할 거야. 나와 관련된 사람 이름만 추출해줘.\n"
                    "2. '밥', '영화' 등과 같은 일반명사는 사람 이름으로 인식하지 않아야 해. 반드시 문맥적으로 판단해.\n"
                    "3. 같은 문맥이나 활동에서 등장한 이름은 같은 그룹으로 묶어야 해. 문맥이 다르면 그룹을 분리해.\n"
                    "   예시:\n"
                    "   입력: \"윤서랑 밥을 먹고 지민이랑 영화를 봤다.\"\n"
                    "   출력: {\"group1\": [\"윤서\"], \"group2\": [\"지민\"]}\n"
                    "4. 입력에 사람이름이 없다면 다음과 같이 응답해:\n"
                    "   {\"group1\": \"none\"}\n"
                    "5. 출력은 **오직 JSON 형식**만 해야 하며, 추가적인 설명이나 텍스트는 포함되지 않도록 해\n"
                    "6. 가족을 나타내는 단어는 이름과 같이 추출해. \n"
                    "   예시:\n"
                    "   입력: \"엄마랑 고스톱을 쳤다.\"\n"
                    "   출력: {\"group1\": [\"엄마\"]}\n"

                )
            }
        ]

    )
    
    # 응답 
    choices = response.choices  # .choices로 접근
    message = choices[0].message.content  # 'message' 객체에서 'content'를 직접 접근
    try:
        message = message.replace("```","").strip()
        message = message.replace("json","").strip()
    except:
        pass
    message = json.loads(message)    
    print(message) #json 형식 ex: {"group1": "윤서", "group2": "우민"}
    return message

# 테스트용
#name_extract(input())