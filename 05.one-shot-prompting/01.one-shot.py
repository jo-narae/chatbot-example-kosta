"""
One-Shot 프롬프팅 - 예시 1개로 형식 유도

Zero-Shot에서는 응답 형식이 들쭉날쭉했습니다.
예시를 딱 1개 주면 AI가 그 형식을 따라합니다.
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


# ── One-Shot: 예시 1개를 보여주고 같은 형식으로 답하게 함 ──
print("=" * 50)
print("One-Shot: 예시 1개로 리뷰 감정 분석")
print("=" * 50)
print()

# 예시 1개를 포함한 프롬프트
prompt_template = """다음 상품 리뷰의 감정을 분석해줘.

[예시]
리뷰: 제품이 사진과 똑같고 배송도 빨라서 만족합니다.
감정: 긍정
이유: 제품 품질과 배송 속도에 만족
점수: 5/5

[분석할 리뷰]
리뷰: {review}"""

reviews = [
    "배송도 빠르고 품질도 좋아요! 재구매 의사 있습니다.",
    "사이즈가 안 맞아서 교환했는데 교환도 느리고 불친절해요.",
    "가격 대비 그냥 그래요. 나쁘지는 않은데 특별하지도 않네요.",
]

for review in reviews:
    result = ask(prompt_template.format(review=review))
    print(f"[리뷰] {review}")
    print(f"[분석]\n{result}")
    print("-" * 40)

print()
print("=" * 50)
print("관찰 포인트")
print("=" * 50)
print("- Zero-Shot(04)과 비교해서 응답 형식이 통일되었나요?")
print("- '감정 / 이유 / 점수' 형식을 예시에서 보여줬더니 따라합니다")
print("- 하지만 예시가 1개라 가끔 형식이 흔들릴 수 있습니다")
print()
print("→ 더 안정적으로 만들고 싶다면? 06.few-shot을 확인하세요!")
