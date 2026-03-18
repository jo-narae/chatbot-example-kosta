"""
System Prompt의 힘 - 역할 부여 전 vs 후 비교

같은 질문이라도 system prompt(역할 설정)에 따라 답변이 완전히 달라집니다.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

client = OpenAI(api_key=api_key)

# 같은 질문을 다른 역할로 물어보기
question = "파이썬이 뭐야?"

# ── 역할 없이 질문 ──
print("=" * 50)
print("[역할 없음] 그냥 질문")
print("=" * 50)

response1 = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "user", "content": question},
    ],
    temperature=0.7,
)
print(response1.choices[0].message.content)

# ── 초등학교 선생님 역할 ──
print()
print("=" * 50)
print("[역할: 초등학교 선생님]")
print("=" * 50)

response2 = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": "너는 초등학교 3학년 담임선생님이야. 아이들이 이해할 수 있게 쉽고 재미있게 설명해줘."},
        {"role": "user", "content": question},
    ],
    temperature=0.7,
)
print(response2.choices[0].message.content)

# ── 시니어 개발자 역할 ──
print()
print("=" * 50)
print("[역할: 시니어 개발자]")
print("=" * 50)

response3 = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": "너는 10년차 백엔드 시니어 개발자야. 기술적으로 정확하고 실무 관점에서 답해줘."},
        {"role": "user", "content": question},
    ],
    temperature=0.7,
)
print(response3.choices[0].message.content)

# ── 정리 ──
print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print("같은 질문 '파이썬이 뭐야?'에 대해:")
print("- 역할 없음 → 일반적인 답변")
print("- 초등학교 선생님 → 쉽고 재미있는 설명")
print("- 시니어 개발자 → 기술적이고 실무적인 답변")
print()
print("→ system prompt로 AI의 '성격'과 '전문성'을 컨트롤할 수 있습니다!")
