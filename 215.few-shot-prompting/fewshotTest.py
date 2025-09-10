# -----------------------------
# 1) 라이브러리 임포트
# -----------------------------
import os
from dotenv import load_dotenv   # .env 파일 로드
from google import genai         # Google Gemini API SDK
from google.genai import types   # 요청 설정 타입

# -----------------------------
# 2) API 키 로드
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

# -----------------------------
# 3) 클라이언트 생성
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# 4) 시스템 지시어 설정
# -----------------------------
system_instruction = (
    "당신은 초등학교 선생님입니다. 쉽고 친절하게 한 문장으로 대답해 주세요."
)

# -----------------------------
# 5) 프롬프트(Few-shot 예시 포함)
# -----------------------------
prompt = ("""
    [예시1]
    초등학생: 아파트는 어떻게 생겼어요?
    선생님: 아파트는 사각형 모양의 큰 건물이에요.
    [예시2]
    초등학생: 축구공은 어떻게 생겼어요?
    선생님: 축구공은 원형 모양의 작은 물체예요.
    [예시3]  # 번호 중복 수정 권장
    초등학생: 책은 어떻게 생겼어요?
    선생님: 책은 원형 모양의 작은 물체예요.  # 잘못된 예시 (모델 혼란 가능)
    [질문]
    초등학생: 달은 어떻게 생겼어요?
    선생님:
""")

# -----------------------------
# 6) 모델 호출
# -----------------------------
response = client.models.generate_content(
    model="gemini-2.0-flash",  # 사용할 모델
    contents=prompt,           # 프롬프트 전달
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,  # 시스템 지시어 적용
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Thinking 비활성화
    ),
)

# -----------------------------
# 7) 응답 출력
# -----------------------------
print(response.text)