import openai
import os
# API 키 설정
def name_extract(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 입력에 대해 사람 이름만을 각각 추출하고 그룹화 하는 챗봇이야. \
            사람 이름이 없으면 none라고 대답해. 여러 사람이 등장하면 같은 무리에 속하는지 그룹을 판단하고 전부 추출해야 해. \
            예를 들어 '오전에는 윤서랑 밥을 먹고 오후에는 우민이랑 영화를 봤다' 라는 입력이 들어오면 group1 : ""우민"", group2 : ""김철수""를 추출해야 해. \
            문맥을 파악해서 사람이름을 판단하는게 중요해 그래서 문장을 잘 읽어보고 답해줘. 일반명사와 사람이름을 잘 구분해야돼. 예시에서 밥은 사람이 아니야. 인칭대명사는 제외해"},
            {"role": "user", "content": f'{text} 출력은 json형식으로 추출해줘.'},
        ]
    )

    # 응답 출력
    choices = response.choices  # .choices로 접근
    message = choices[0].message.content  # 'message' 객체에서 'content'를 직접 접근
    # 추후 로깅으로 대체
    print(message) #json 형식 ex: {"group1": ["윤서"], "group2": ["우민"]}
    return message

# 테스트용
# name_extract(input())