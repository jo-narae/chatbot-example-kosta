import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

# 페르소나 설정 (system_instruction) = 원샷 프롬프팅
system_instruction = "당신은 유치원 선생님입니다. 사용자는 유치원생입니다. 쉽고 친절하게 이야기하되 1문장 이내로 짧게 얘기하세요."

# 모델 불러오기 설정
model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_instruction)

prompt = "오리는 무슨 동물일까요?"

# temperature 지정 가능
response = model.generate_content(prompt, generation_config={"temperature": 0.9})

print(response.text)

