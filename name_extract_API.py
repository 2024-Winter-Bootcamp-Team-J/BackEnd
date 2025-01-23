import openai
import os
from dotenv import load_dotenv
import json
load_dotenv()
# API 키 설정
def name_extract(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "입력된 텍스트에서 사람 이름을 그룹화하여 json으로 출력해"},            
            {"role": "user", "content": f'{text}\n \
            위 텍스트가 입력이야. 아래 규칙을 반드시 전부 따라서 응답해줘. \
            1. 입력에서 사람이름이 등장하지 않으면 none이라고 응답해.\n \
            2. 출력에는 사람 이름만 등장해야돼. \n \
            3. 만약 여러 명의 사람이 등장한다면, 그들이 같은 활동을 했거나 같은 문맥에서 등장하면 같은 그룹으로 묶어.\n \
            4. 문장을 잘 분석해서 일반명사와 사람이름을 정확히 식별해서 응답해. \n \
            5  밥, 영화, 소라, 미나, 강, 산, 하늘, 장미, 진주, 나래, 별, 사랑 등의 사람이름과 혼동되는 일반 명사를 구분하여 이름에서 제외해. \n \
            6. 인칭대명사(예: 나, 너, 그, 그녀)는 이름이 아니야. \n \
            7. 은/는/이/가/을/를/에/에서/로/으로/와/랑/과/만/마저/조차/부터/까지/도/의/처럼/같이/마다/마다/에게/한테/께/에게서/한테서/께서 와 같은 조사는 제외해. \n \
            8. 응답을 json.loads(message)에 message로 넣을 수 있게 JSON으로 출력해.'}
            ]
    )
    
    # 응답 
    choices = response.choices  # .choices로 접근
    message = choices[0].message.content  # 'message' 객체에서 'content'를 직접 접근
    # message = json.loads(message)    
    # 추후 로깅으로 대체
    print(message) #json 형식 ex: {"group1": "윤서", "group2": "우민"}
    return message

# 테스트용
name_extract(input())