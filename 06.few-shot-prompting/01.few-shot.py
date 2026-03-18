"""
Few-Shot 프롬프팅 - 예시 여러 개로 패턴 학습

예시를 여러 개 주면 AI가 패턴을 더 정확하게 파악합니다.
특히 긍정/부정/중립 각각의 예시를 보여주면 분류 정확도가 올라갑니다.
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


# ── Few-Shot: 긍정/부정/중립 예시를 각각 보여줌 ──
print("=" * 50)
print("Few-Shot: 예시 3개로 리뷰 감정 분석")
print("=" * 50)
print()

# 긍정/부정/중립 각 1개씩 = 총 3개 예시
prompt_template = """다음 상품 리뷰의 감정을 분석해줘.

[예시 1 - 긍정]
리뷰: 제품이 사진과 똑같고 배송도 빨라서 만족합니다.
감정: 긍정
이유: 제품 품질과 배송 속도에 만족
점수: 5/5

[예시 2 - 부정]
리뷰: 포장이 찢어져서 왔고 제품에 스크래치가 있었어요. 실망입니다.
감정: 부정
이유: 포장 불량 및 제품 손상
점수: 1/5

[예시 3 - 중립]
리뷰: 쓸만한데 가격이 좀 비싼 느낌이에요. 할인하면 또 살 것 같아요.
감정: 중립
이유: 품질은 인정하나 가격 대비 아쉬움
점수: 3/5

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
print("04 → 05 → 06 비교 정리")
print("=" * 50)
print()
print("Zero-Shot (예시 0개): 형식이 제각각, AI가 자유롭게 해석")
print("One-Shot  (예시 1개): 형식을 따라하지만 가끔 흔들림")
print("Few-Shot  (예시 3개): 형식도 안정적, 분류 정확도도 높음")
print()
print("정리:")
print("  예시가 많을수록 → 형식이 안정적 + 정확도 향상")
print("  하지만 예시가 너무 많으면 → 토큰 비용 증가 + 느려짐")
print("  실무에서는 2~5개 예시가 적절합니다!")
