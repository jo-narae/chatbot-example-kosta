"""
LangChain 챗봇 개발 및 LangSmith 추적 예제

LangSmith를 활용하여 LLM 애플리케이션을 추적하고 모니터링하는 방법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 환경변수 로드 (LangSmith 추적 자동 활성화)
load_dotenv()

# API 키 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

# LangSmith 설정 확인 (선택사항)
print("🔍 LangSmith 설정 확인:")
print(f"  - Tracing: {os.environ.get('LANGCHAIN_TRACING_V2', 'false')}")
print(f"  - Project: {os.environ.get('LANGCHAIN_PROJECT', 'default')}")
print()

# Gemini 모델 초기화
print("🤖 Gemini 모델 초기화 중...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)

print("✅ 모델 초기화 완료!")
print()

# 기본 질문 테스트
print("=" * 60)
print("예제 1: 기본 질문 (LangSmith에 자동 추적됨)")
print("=" * 60)

question = "파이썬의 주요 특징 3가지를 간단히 설명해주세요."
print(f"📝 질문: {question}")
print()

response = llm.invoke(question)
print(f"🤖 답변:\n{response.content}")
print()

# 대화 히스토리 예제
print("=" * 60)
print("예제 2: 대화 히스토리 (ConversationChain)")
print("=" * 60)

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 메모리 설정
memory = ConversationBufferMemory()

# 대화 체인 생성
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False  # True로 설정하면 상세 로그 출력
)

# 연속 대화
questions = [
    "안녕하세요! 저는 파이썬을 배우고 싶어요.",
    "파이썬으로 무엇을 만들 수 있나요?",
    "초보자에게 추천하는 첫 번째 프로젝트는 무엇인가요?"
]

for i, q in enumerate(questions, 1):
    print(f"[대화 {i}]")
    print(f"👤 사용자: {q}")
    answer = conversation.predict(input=q)
    print(f"🤖 AI: {answer}")
    print()

# LangSmith 대시보드 안내
print("=" * 60)
print("📊 LangSmith 대시보드에서 추적 결과 확인하기")
print("=" * 60)
print("1. https://smith.langchain.com 접속")
print("2. 로그인 후 프로젝트 선택")
print("3. 최근 실행 내역에서 이 세션의 추적 데이터 확인")
print()
print("확인 가능한 정보:")
print("  - 입력/출력 데이터")
print("  - 실행 시간 및 토큰 사용량")
print("  - 체인 실행 흐름")
print("  - 에러 및 디버깅 정보")
