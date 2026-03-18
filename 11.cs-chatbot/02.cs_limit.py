"""
고객 상담 챗봇의 한계 - system prompt만으로는 부족한 이유

01에서 FAQ를 system prompt에 직접 넣었습니다.
FAQ가 적을 때는 괜찮지만, 많아지면 어떻게 될까요?

실행: uv run python 11.cs-chatbot/02.cs_limit.py
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

# ══════════════════════════════════════════════════
# 상황 1: FAQ 5개 → system prompt에 넣기 (잘 됨!)
# ══════════════════════════════════════════════════
print("=" * 50)
print("상황 1: FAQ 5개 - system prompt에 직접 넣기")
print("=" * 50)

small_faq = """
Q: 배송은 얼마나 걸려요? → 2~3 영업일
Q: 배송비는 얼마예요? → 3만원 이상 무료, 미만 시 3,000원
Q: 교환은 어떻게 해요? → 수령 후 7일 이내 가능
Q: 포인트는 어떻게 쓰나요? → 1,000포인트 이상부터 사용 가능
Q: 새벽 배송 되나요? → 수도권만 가능, 밤 11시 전 주문
"""

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": f"너는 쇼핑몰 상담사야. 아래 FAQ를 참고해서 답해줘.\n{small_faq}"},
        {"role": "user", "content": "배송비가 얼마예요?"},
    ],
    temperature=0.3,
)

print(f"[질문] 배송비가 얼마예요?")
print(f"[답변] {response.choices[0].message.content}")
print(f"[FAQ 크기] {len(small_faq)}자")
print("→ FAQ가 적으니까 잘 동작합니다!")

# ══════════════════════════════════════════════════
# 상황 2: FAQ 100개 → system prompt가 엄청 길어짐
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("상황 2: FAQ 100개로 늘어나면?")
print("=" * 50)

# FAQ 100개를 시뮬레이션
big_faq_lines = []
categories = ["배송", "교환", "환불", "포인트", "회원", "결제", "상품", "이벤트", "쿠폰", "앱"]
for i in range(100):
    cat = categories[i % len(categories)]
    big_faq_lines.append(f"Q: {cat} 관련 질문 {i+1}번 → {cat}에 대한 상세한 답변 내용이 여기에 들어갑니다. 이 답변은 꽤 길 수 있으며 여러 조건과 예외 사항을 포함합니다.")

big_faq = "\n".join(big_faq_lines)

print(f"[FAQ 크기] {len(big_faq):,}자 ({len(big_faq)//4:,} 토큰 추정)")
print()
print("문제점:")
print(f"  1. 매 질문마다 {len(big_faq):,}자를 보내야 함 → 비용 증가!")
print(f"  2. 토큰 한도 초과 위험 (모델마다 한계가 있음)")
print(f"  3. FAQ가 너무 많으면 AI가 정확한 답을 못 찾을 수 있음")
print(f"  4. FAQ가 추가/수정될 때마다 코드를 바꿔야 함")

# ══════════════════════════════════════════════════
# 상황 3: 실제 기업은 FAQ가 수백~수천 개
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("상황 3: 실제 기업의 데이터량")
print("=" * 50)
print()
print("  쇼핑몰 FAQ:     200~500개")
print("  은행 금융상품:   1,000개+")
print("  보험 약관:       수만 페이지")
print("  법률 문서:       수십만 페이지")
print()
print("→ 이걸 전부 system prompt에 넣을 수는 없습니다!")

# ══════════════════════════════════════════════════
# 해결 방향
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("해결 방법: RAG (Retrieval-Augmented Generation)")
print("=" * 50)
print()
print("  1. 문서를 미리 잘게 쪼개서 저장해둔다 (청킹)")
print("  2. 질문이 들어오면 관련된 조각만 검색한다 (검색)")
print("  3. 검색된 조각만 system prompt에 넣는다 (생성)")
print()
print("  FAQ 1,000개 중 → 질문과 관련된 3~5개만 골라서 넣기!")
print()
print("→ 다음 단계(12)에서 RAG를 직접 구현합니다!")
