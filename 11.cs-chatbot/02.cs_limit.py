"""
고객 상담 챗봇의 한계 - system prompt에 FAQ를 박는 방식이 왜 무너지는가

세 가지 시나리오를 실제로 호출해서 비교한다:
  1) FAQ 5개   → 작고 정확, 빠르고 저렴
  2) FAQ 200개 → 답이 묻혀서 못 찾기 시작, 비용/지연 폭증
  3) FAQ 1000개→ 토큰 폭발, 실전 서비스 불가능

이 비교를 보고 나면 RAG가 왜 필요한지 자연스럽게 납득된다.
"""

import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 환경변수 로드
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

# gpt-4.1-nano 가격 (2025년 기준, 1M 토큰당 USD)
PRICE_INPUT_PER_1M = 0.10
PRICE_OUTPUT_PER_1M = 0.40


def make_faq(n: int, hidden_answer_index: int | None = None) -> str:
    """N개의 FAQ를 만든다. hidden_answer_index 위치에 '정답'을 숨겨둔다."""
    categories = ["배송", "교환", "환불", "포인트", "회원", "결제", "상품", "이벤트", "쿠폰", "앱"]
    lines = []
    for i in range(n):
        if i == hidden_answer_index:
            # 진짜 정답을 한 줄 숨겨둠
            lines.append(
                "Q: 새벽 배송 마감 시간이 몇 시인가요? "
                "→ 새벽 배송은 밤 11시(23:00)까지 주문하시면 다음날 오전 7시 전에 도착합니다. 수도권만 가능합니다."
            )
        else:
            cat = categories[i % len(categories)]
            lines.append(
                f"Q: {cat} 관련 일반 안내 {i+1}번 "
                f"→ {cat}에 대한 일반적인 답변입니다. 자세한 사항은 고객센터로 문의해 주세요. "
                f"운영시간은 평일 09시부터 18시까지이며, 주말과 공휴일은 휴무입니다."
            )
    return "\n".join(lines)


def run_scenario(label: str, faq_size: int, question: str):
    """하나의 시나리오를 실행하고 결과를 출력한다."""
    # FAQ 중간 지점에 정답을 숨김 (Lost-in-the-Middle 효과 노출)
    hidden_idx = faq_size // 2
    faq = make_faq(faq_size, hidden_answer_index=hidden_idx)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 쇼핑몰 상담사야. 아래 FAQ만 참고해서 정확히 답해줘.\n\n{faq}"),
        ("human", "{question}"),
    ])
    chain = prompt | llm

    start = time.time()
    response = chain.invoke({"faq": faq, "question": question})
    elapsed = time.time() - start

    usage = response.usage_metadata or {}
    in_tok = usage.get("input_tokens", 0)
    out_tok = usage.get("output_tokens", 0)

    cost = (in_tok * PRICE_INPUT_PER_1M + out_tok * PRICE_OUTPUT_PER_1M) / 1_000_000

    print(f"\n{'='*70}")
    print(f"📊 {label}  (FAQ {faq_size}개, 약 {len(faq):,}자)")
    print(f"{'='*70}")
    print(f"  ⏱  응답 시간:   {elapsed:.2f}초")
    print(f"  🔢 입력 토큰:   {in_tok:,}")
    print(f"  🔢 출력 토큰:   {out_tok:,}")
    print(f"  💰 1건 비용:    ${cost:.6f}")
    print(f"  💰 1000건 비용: ${cost * 1000:.2f}  (월 1000건 상담 가정)")
    print(f"\n  💬 답변:")
    print(f"     {response.content}")


# ─────────────────────────────────────────────────────────────
QUESTION = "새벽 배송은 몇 시까지 주문해야 하나요?"
print(f"\n🙋 동일한 질문: \"{QUESTION}\"")
print(f"   (정답: 밤 11시 / 23:00)")

# 시나리오 1: 작은 FAQ — 잘 작동
run_scenario("시나리오 1: FAQ 5개 (현재)", faq_size=5, question=QUESTION)

# 시나리오 2: FAQ가 늘어남 — 답이 묻히기 시작
run_scenario("시나리오 2: FAQ 200개 (3개월 후)", faq_size=200, question=QUESTION)

# 시나리오 3: 실전 규모 — 비용/지연 폭발
run_scenario("시나리오 3: FAQ 1000개 (1년 후)", faq_size=1000, question=QUESTION)

# ─────────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("🚨 관찰된 문제")
print(f"{'='*70}")
print("  1. 비용:  FAQ가 200배 늘면 토큰도 200배, 비용도 200배")
print("  2. 속도:  매 질문마다 같은 FAQ 전체를 다시 보내야 함")
print("  3. 품질:  정답이 FAQ 중간에 있어도 LLM이 못 찾을 수 있음 (Lost-in-the-Middle)")
print("  4. 운영:  FAQ 추가/수정마다 코드 배포 필요")
print("  5. 한계:  토큰 한도(128K) 넘으면 아예 호출 불가")

print(f"\n{'='*70}")
print("✅ 해결책: RAG (Retrieval-Augmented Generation)")
print(f"{'='*70}")
print("  - FAQ 1000개를 벡터 DB에 저장")
print("  - 질문과 가장 관련 있는 3~5개만 검색해서 LLM에 전달")
print("  - 토큰 사용: 1000개 분량 → 5개 분량으로 감소")
print("  - 정확도: 관련 없는 노이즈가 제거되어 LLM이 핵심에 집중")
print("  - 운영: FAQ 추가/수정 시 DB만 업데이트, 코드 변경 불필요\n")
