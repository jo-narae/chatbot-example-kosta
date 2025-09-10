import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. .env 로드
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

# 2. 클라이언트 초기화
client = genai.Client(api_key=api_key)

# 3. 시스템 지시어 (system_instruction)
system_instruction = (
    "당신은 유치원 선생님입니다. 쉽고 친절하게 한 문장으로 대답해 주세요."
)

# 4. 프롬프트
prompt = "호랑이는 무슨 동물일까요?"

# 5. 모델 호출 (신 SDK 방식)
response = client.models.generate_content(
    model="gemini-2.0-flash",   # 모델명 문자열로 직접 지정
    contents=prompt,            # 사용자 프롬프트
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,           # 시스템 지시어를 config에 전달
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Thinking 비활성화
    ),
)

# 6. 응답 출력
print(response.text)