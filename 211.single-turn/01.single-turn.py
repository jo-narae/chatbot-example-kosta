import os
from dotenv import load_dotenv
import google.generativeai as genai

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# system_instruction = 페르소나 설정
system_instruction = "너는 사용자를 도와주는 상담사야."

# 모델 생성 (system_instruction 포함)
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=system_instruction
)

# 대화 루프
while True:
    user_input = input("사용자: ")

    if user_input.lower() == "exit":
        break

    response = model.generate_content(
        user_input,
        generation_config={"temperature": 0.9}
    )

    print("AI:", response.text)