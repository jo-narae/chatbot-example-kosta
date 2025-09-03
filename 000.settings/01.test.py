# 운영체제와 상호작용하는 기능(파이썬 표준 라이브러리)
import os
# 환경변수 관리 라이브러리
from dotenv import load_dotenv
# 구글 Gemini API의 공식 파이썬 SDK 임포트
import google.generativeai as genai


# .env 불러오기
load_dotenv()

# 환경변수에서 API 키 가져오기
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini 클라이언트 초기화
genai.configure(api_key=api_key)

# 모델 불러오기
model = genai.GenerativeModel("gemini-2.0-flash")

# 프롬프트 요청
response = model.generate_content("한국의 수도는?")

# 출력
print(response.text)