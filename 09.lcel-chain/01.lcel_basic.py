"""
LCEL 기본 - 파이프(|)로 연결하기

LCEL(LangChain Expression Language)은 파이프(|)로 구성요소를 연결합니다.
프롬프트와 LLM을 파이프로 연결해서 호출하는 가장 기본적인 형태입니다.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

# ══════════════════════════════════════════════════
# LLM 단독 호출
# ══════════════════════════════════════════════════
print("=" * 50)
print("1. LLM만 호출")
print("=" * 50)

result = llm.invoke("파이썬을 한 줄로 설명해줘.")
print(f"결과: {result.content}")
print(f"타입: {type(result)}")
print("→ 매번 질문을 직접 문자열로 써야 합니다")

# ══════════════════════════════════════════════════
# 프롬프트 + LLM 파이프 연결
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("2. prompt | llm (파이프로 연결)")
print("=" * 50)

# 프롬프트 템플릿: {변수}를 넣을 수 있는 틀
prompt = ChatPromptTemplate.from_template("{topic}을(를) 한 줄로 설명해줘.")

# 파이프(|)로 연결 = 체인!
chain = prompt | llm

# 변수만 넣으면 프롬프트 완성 → LLM 호출까지 자동
result = chain.invoke({"topic": "파이썬"})
print(f"결과: {result.content}")
print(f"타입: {type(result)}")

# ══════════════════════════════════════════════════
# 변수만 바꿔서 재사용
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("3. 변수만 바꿔서 재사용")
print("=" * 50)

topics = ["인공지능", "클라우드", "블록체인"]
for topic in topics:
    result = chain.invoke({"topic": topic})
    print(f"  [{topic}] {result.content}")

# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print()
print("  prompt | llm  =  체인(Chain)")
print()
print("  데이터 흐름: {변수} → 프롬프트 완성 → LLM 호출 → AIMessage")
print()
print("  지금은 결과가 AIMessage 객체라서 .content로 꺼내야 합니다")
print("  → 다음 파일(02)에서 이걸 해결하는 '파서'를 배웁니다!")
