import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# system_instruction = 페르소나 설정
system_instruction = (
    "당신은 유치원 선생님입니다. "
    "사용자는 유치원생입니다. "
    "쉽고 친절하게 이야기하되, 1문장 이내로 짧게 대답하세요."
)

# 모델 불러오기
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=system_instruction
)

# === Few-shot 프롬프트 구성 ===
prompt = """
[예시1]
유치원생: 사자는 어떤 동물이에요?
선생님: 사자는 왕처럼 숲을 지배하는 동물이야.

[예시2]
유치원생: 코끼리는 어떤 동물이에요?
선생님: 코끼리는 기다란 코로 물을 시원하게 뿌리지.

[예시3]
유치원생: 기린은 어떤 동물이에요?
선생님: 기린은 목이 길어서 멀리 있는 걸 잘 볼 수 있어.

[예시4]
유치원생: 참새는 어떤 동물이에요?
선생님: 참새는 작은 날개로 빠르게 훨훨 날아다녀.

[예시5]
유치원생: 오리는 무슨 동물일까요?
선생님:
"""

response = model.generate_content(
    prompt,
    generation_config={"temperature": 0.9}
)

print(response.text)