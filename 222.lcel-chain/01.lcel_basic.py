"""
LangChain Expression Language (LCEL) 기본 예제

LCEL을 사용하여 프롬프트 템플릿과 체인을 구성하는 방법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 환경변수 로드
load_dotenv()

# API 키 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

print("=" * 60)
print("LCEL (LangChain Expression Language) 기본 예제")
print("=" * 60)
print()

# 1. 모델 초기화
print("🤖 Gemini 모델 초기화 중...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)
print("✅ 모델 초기화 완료!")
print()

# 2. 프롬프트 템플릿 생성
print("📝 프롬프트 템플릿 생성")
prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 {num}가지 요점을 간단히 설명해주세요: {topic}"
)
print(f"템플릿: {prompt.messages[0].prompt.template}")
print()

# 3. Output Parser 설정
output_parser = StrOutputParser()

# 4. LCEL 체인 구성 (파이프 연산자 사용)
print("🔗 LCEL 체인 구성: prompt | llm | output_parser")
chain = prompt | llm | output_parser
print("✅ 체인 구성 완료!")
print()

# 5. 체인 실행
print("=" * 60)
print("예제 1: 파이썬의 특징 3가지")
print("=" * 60)

response = chain.invoke({
    "topic": "파이썬 프로그래밍 언어",
    "num": "3"
})

print(f"🤖 답변:\n{response}")
print()

# 6. 다양한 주제로 테스트
print("=" * 60)
print("예제 2: 여러 주제 배치 처리")
print("=" * 60)

topics = [
    {"topic": "머신러닝", "num": "3"},
    {"topic": "웹 개발", "num": "3"},
    {"topic": "데이터 분석", "num": "3"}
]

for i, params in enumerate(topics, 1):
    print(f"\n[질문 {i}] {params['topic']}의 특징 {params['num']}가지")
    print("-" * 40)
    response = chain.invoke(params)
    print(response)

print()
print("=" * 60)
print("LCEL의 장점:")
print("  1. 가독성: 파이프 연산자로 체인 흐름을 명확히 표현")
print("  2. 재사용성: 프롬프트 템플릿을 쉽게 재사용")
print("  3. 확장성: 체인에 새로운 컴포넌트를 쉽게 추가")
print("  4. 타입 안전성: 입력/출력 타입 검증")
print("=" * 60)
