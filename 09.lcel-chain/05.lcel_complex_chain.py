"""
복잡한 체인 - 체인끼리 연결하기

하나의 체인 출력을 다른 체인의 입력으로 연결합니다.
→ 설명 생성 → 퀴즈 생성 → 정답 확인까지 자동으로!
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

# ══════════════════════════════════════════════════
# 1단계 체인: 주제 → 설명 생성
# ══════════════════════════════════════════════════
explain_chain = (
    ChatPromptTemplate.from_template(
        "{topic}을(를) 초등학생도 이해할 수 있게 3줄로 설명해줘."
    )
    | llm
    | StrOutputParser()
)

# ══════════════════════════════════════════════════
# 2단계 체인: 설명 → 퀴즈 생성
# ══════════════════════════════════════════════════
quiz_chain = (
    ChatPromptTemplate.from_template(
        "다음 설명을 읽고 O/X 퀴즈 2개를 만들어줘.\n"
        "형식: 'Q: (문제) → 정답: O 또는 X'\n\n"
        "설명:\n{explanation}"
    )
    | llm
    | StrOutputParser()
)

# ══════════════════════════════════════════════════
# 수동 연결: 1단계 결과를 2단계에 전달
# ══════════════════════════════════════════════════
print("=" * 50)
print("방법 1: 수동으로 체인 연결")
print("=" * 50)

topic = "인공지능"
print(f"[주제] {topic}")

explanation = explain_chain.invoke({"topic": topic})
print(f"\n[1단계: 설명]\n{explanation}")

quiz = quiz_chain.invoke({"explanation": explanation})
print(f"\n[2단계: 퀴즈]\n{quiz}")

# ══════════════════════════════════════════════════
# 자동 연결: RunnablePassthrough로 한번에!
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("방법 2: RunnablePassthrough로 자동 연결")
print("=" * 50)

# 설명 → 퀴즈를 한 번에 연결하는 파이프라인
full_chain = (
    # 1단계: topic → explanation 생성
    {"explanation": explain_chain}
    # 2단계: explanation → quiz 생성
    | quiz_chain
)

print(f"[주제] 블록체인")
result = full_chain.invoke({"topic": "블록체인"})
print(f"\n[결과 (설명→퀴즈 자동)]\n{result}")

# ══════════════════════════════════════════════════
# 3단계 추가: 설명 + 퀴즈 + 학습 요약까지
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("방법 3: 3단계 체인 (설명 → 퀴즈 → 요약)")
print("=" * 50)

summary_chain = (
    ChatPromptTemplate.from_template(
        "다음 퀴즈를 보고 학습 포인트를 2줄로 요약해줘:\n\n{quiz}"
    )
    | llm
    | StrOutputParser()
)

# 3단계 수동 연결 (흐름이 보이도록)
topic = "클라우드 컴퓨팅"
print(f"[주제] {topic}")

step1 = explain_chain.invoke({"topic": topic})
print(f"\n[1단계: 설명]\n{step1}")

step2 = quiz_chain.invoke({"explanation": step1})
print(f"\n[2단계: 퀴즈]\n{step2}")

step3 = summary_chain.invoke({"quiz": step2})
print(f"\n[3단계: 학습 요약]\n{step3}")

# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print("체인 연결 = 한 체인의 출력을 다른 체인의 입력으로")
print()
print("  explain_chain: topic → 설명")
print("  quiz_chain:    설명 → 퀴즈")
print("  summary_chain: 퀴즈 → 요약")
print()
print("이것이 LCEL의 진짜 힘입니다!")
print("복잡한 AI 워크플로우를 레고 블록처럼 조립할 수 있습니다.")
