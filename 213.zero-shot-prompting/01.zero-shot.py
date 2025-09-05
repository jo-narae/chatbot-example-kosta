import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("이 문장이 긍정적인지 부정적인지 분류해줘: '이 영화는 정말 재미없었다.'")

print(response.text)

