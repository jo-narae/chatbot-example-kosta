"""
Step 5-1: LangChain 소개 및 기본 사용법

LangChain을 사용하여 Gemini 모델을 래핑하고 기본적인 대화를 구현합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# 환경 설정
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / ".env")

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found")

print("=" * 60)
print("LangChain 기본 사용법")
print("=" * 60)
print()

# 1. 모델 초기화
print("1️⃣ ChatGoogleGenerativeAI 모델 초기화")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7
)
print("✅ 모델 초기화 완료")
print()

# 2. 기본 invoke
print("2️⃣ 기본 invoke 사용")
response = llm.invoke("파이썬의 주요 특징 3가지를 알려줘")
print(f"응답 타입: {type(response)}")
print(f"응답 내용:\n{response.content}")
print()

# 3. 메시지 형식 사용
print("3️⃣ 메시지 형식으로 대화")
messages = [
    SystemMessage(content="너는 친절한 프로그래밍 튜터입니다."),
    HumanMessage(content="Python의 리스트와 튜플의 차이점은?")
]
response = llm.invoke(messages)
print(f"응답:\n{response.content}")
print()

# 4. 연속 대화
print("4️⃣ 연속 대화 (메시지 추가)")
messages.append(response)  # AI 응답 추가
messages.append(HumanMessage(content="그럼 언제 튜플을 사용하나요?"))

response = llm.invoke(messages)
print(f"응답:\n{response.content}")
print()

print("=" * 60)
print("💡 LangChain의 장점:")
print("  1. 통일된 인터페이스 - 다양한 LLM을 같은 방식으로 사용")
print("  2. 메시지 관리 - SystemMessage, HumanMessage 등으로 구조화")
print("  3. 확장성 - Chain, Agent 등 고급 기능 사용 가능")
print("  4. 생태계 - 다양한 도구와 통합")
print()
print("다음: uv run python 02_message_history.py")
print("=" * 60)
