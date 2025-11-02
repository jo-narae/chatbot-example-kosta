"""
LangChain 스트리밍 출력 기본 예제

실시간으로 토큰 단위로 응답을 스트리밍하는 방법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# 환경변수 로드
load_dotenv()

# API 키 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

print("=" * 60)
print("LangChain 스트리밍 출력 예제")
print("=" * 60)
print()

# 1. 모델 초기화
print("🤖 Gemini 모델 초기화 중...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    streaming=True  # 스트리밍 활성화
)
print("✅ 모델 초기화 완료!")
print()

# 2. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_template("{question}")

# 3. Output Parser
output_parser = StrOutputParser()

# 4. 체인 구성
chain = prompt | llm | output_parser

# 예제 1: 기본 스트리밍
print("=" * 60)
print("예제 1: 기본 스트리밍 출력")
print("=" * 60)

question1 = "파이썬의 주요 특징 5가지를 자세히 설명해주세요."
print(f"📝 질문: {question1}")
print()
print("🤖 AI 응답 (실시간 스트리밍):")
print("-" * 60)

start_time = time.time()

for chunk in chain.stream({"question": question1}):
    print(chunk, end="", flush=True)

elapsed_time = time.time() - start_time
print()
print("-" * 60)
print(f"⏱️ 응답 시간: {elapsed_time:.2f}초")
print()

# 예제 2: 스트리밍 vs 일반 호출 비교
print("=" * 60)
print("예제 2: 스트리밍 vs 일반 호출 성능 비교")
print("=" * 60)

question2 = "머신러닝과 딥러닝의 차이점을 설명해주세요."
print(f"📝 질문: {question2}")
print()

# 스트리밍 방식
print("[방식 1] 스트리밍 출력:")
print("-" * 60)
stream_start = time.time()

for chunk in chain.stream({"question": question2}):
    print(chunk, end="", flush=True)

stream_time = time.time() - stream_start
print()
print("-" * 60)
print(f"⏱️ 스트리밍 시간: {stream_time:.2f}초")
print()

# 일반 호출 방식
print("[방식 2] 일반 호출 출력:")
print("-" * 60)
invoke_start = time.time()

response = chain.invoke({"question": question2})
print(response)

invoke_time = time.time() - invoke_start
print("-" * 60)
print(f"⏱️ 일반 호출 시간: {invoke_time:.2f}초")
print()

# 예제 3: 긴 응답 스트리밍
print("=" * 60)
print("예제 3: 긴 응답의 스트리밍 효과")
print("=" * 60)

question3 = "웹 개발 초보자를 위한 학습 로드맵을 단계별로 상세히 작성해주세요."
print(f"📝 질문: {question3}")
print()
print("🤖 AI 응답 (실시간 스트리밍):")
print("-" * 60)

chunk_count = 0
start_time = time.time()

for chunk in chain.stream({"question": question3}):
    print(chunk, end="", flush=True)
    chunk_count += 1

elapsed_time = time.time() - start_time
print()
print("-" * 60)
print(f"⏱️ 응답 시간: {elapsed_time:.2f}초")
print(f"📦 총 청크 수: {chunk_count}개")
print()

# 결론
print("=" * 60)
print("스트리밍의 장점:")
print("  1. 사용자 경험 개선: 즉각적인 피드백")
print("  2. 긴 응답 처리: 전체 응답을 기다릴 필요 없음")
print("  3. 실시간성: 타이핑 효과로 자연스러운 대화감")
print("  4. 중단 가능: 필요시 중간에 응답 중단 가능")
print()
print("사용 사례:")
print("  - 챗봇 인터페이스")
print("  - 실시간 콘텐츠 생성")
print("  - 긴 문서 작성")
print("  - 대화형 애플리케이션")
print("=" * 60)
