"""
Zero-Shot 프롬프팅 - 예시 없이 지시만으로

예시를 하나도 주지 않고, 지시만으로 AI에게 작업을 시킵니다.
→ AI가 알아서 해석하기 때문에 형식이 들쭉날쭉할 수 있습니다.
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


def ask(prompt):
    """API 호출 헬퍼"""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ── Zero-Shot: 예시 없이 바로 지시 ──
print("=" * 50)
print("Zero-Shot: 예시 없이 리뷰 감정 분석")
print("=" * 50)
print()

reviews = [
    "배송도 빠르고 품질도 좋아요! 재구매 의사 있습니다.",
    "사이즈가 안 맞아서 교환했는데 교환도 느리고 불친절해요.",
    "가격 대비 그냥 그래요. 나쁘지는 않은데 특별하지도 않네요.",
]

for review in reviews:
    result = ask(
        f"다음 상품 리뷰의 감정을 분석해줘.\n\n리뷰: {review}"
    )
    print(f"[리뷰] {review}")
    print(f"[분석] {result}")
    print("-" * 40)

print()
print("=" * 50)
print("관찰 포인트")
print("=" * 50)
print("- 분석 결과의 '형식'이 일정한가요?")
print("- 어떤 건 길고, 어떤 건 짧고, 형식이 제각각일 수 있습니다")
print("- 예시를 주지 않았기 때문에 AI가 자유롭게 해석합니다")
print()
print("→ 형식을 통일하고 싶다면? 05.one-shot을 확인하세요!")
