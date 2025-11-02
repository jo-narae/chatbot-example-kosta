"""
LangChain Tool 기본 예제

커스텀 도구를 정의하고 LLM이 도구를 활용하도록 하는 방법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from datetime import datetime
import math

# 환경변수 로드
load_dotenv()

# API 키 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

print("=" * 60)
print("LangChain Tool (도구) 기본 예제")
print("=" * 60)
print()

# 1. 커스텀 도구 정의
print("🛠️ 커스텀 도구 정의 중...")

@tool
def get_current_time() -> str:
    """현재 시간을 반환합니다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str) -> float:
    """수학 표현식을 계산합니다. 예: '2 + 2' 또는 '10 * 5'"""
    try:
        # 안전한 계산을 위해 eval 대신 제한된 함수 사용
        allowed_names = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "sqrt": math.sqrt
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        return f"계산 오류: {str(e)}"

@tool
def get_word_length(word: str) -> int:
    """주어진 단어의 글자 수를 반환합니다."""
    return len(word)

tools = [get_current_time, calculate, get_word_length]

print(f"✅ {len(tools)}개의 도구 정의 완료:")
for t in tools:
    print(f"  - {t.name}: {t.description}")
print()

# 2. 모델 초기화 (Tool Binding)
print("🤖 Gemini 모델 초기화 및 도구 바인딩 중...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0
)

# 모델에 도구 바인딩
llm_with_tools = llm.bind_tools(tools)
print("✅ 도구 바인딩 완료!")
print()

# 3. 도구 호출 테스트
print("=" * 60)
print("예제 1: 현재 시간 질문")
print("=" * 60)

question1 = "지금 몇 시야?"
print(f"👤 질문: {question1}")

response1 = llm_with_tools.invoke(question1)
print(f"\n🤖 모델 응답:")
print(f"  Content: {response1.content}")

# Tool calls 확인
if hasattr(response1, 'tool_calls') and response1.tool_calls:
    print(f"  Tool Calls: {response1.tool_calls}")

    # 실제 도구 실행
    for tool_call in response1.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call.get('args', {})

        # 도구 찾기 및 실행
        for tool_obj in tools:
            if tool_obj.name == tool_name:
                result = tool_obj.invoke(tool_args)
                print(f"\n  ✅ 도구 실행 결과: {result}")
                break

print()

# 4. 계산 도구 테스트
print("=" * 60)
print("예제 2: 계산 질문")
print("=" * 60)

question2 = "123 곱하기 456은 얼마야?"
print(f"👤 질문: {question2}")

response2 = llm_with_tools.invoke(question2)
print(f"\n🤖 모델 응답:")
print(f"  Content: {response2.content}")

if hasattr(response2, 'tool_calls') and response2.tool_calls:
    print(f"  Tool Calls: {response2.tool_calls}")

    for tool_call in response2.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call.get('args', {})

        for tool_obj in tools:
            if tool_obj.name == tool_name:
                result = tool_obj.invoke(tool_args)
                print(f"\n  ✅ 도구 실행 결과: {result}")
                break

print()

# 5. 단어 길이 도구 테스트
print("=" * 60)
print("예제 3: 단어 길이 질문")
print("=" * 60)

question3 = "안녕하세요라는 단어는 몇 글자야?"
print(f"👤 질문: {question3}")

response3 = llm_with_tools.invoke(question3)
print(f"\n🤖 모델 응답:")
print(f"  Content: {response3.content}")

if hasattr(response3, 'tool_calls') and response3.tool_calls:
    print(f"  Tool Calls: {response3.tool_calls}")

    for tool_call in response3.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call.get('args', {})

        for tool_obj in tools:
            if tool_obj.name == tool_name:
                result = tool_obj.invoke(tool_args)
                print(f"\n  ✅ 도구 실행 결과: {result}")
                break

print()
print("=" * 60)
print("Tool의 장점:")
print("  1. 실시간 데이터 접근: LLM이 최신 정보를 활용")
print("  2. 정확한 계산: 수학적 계산의 정확성 보장")
print("  3. 외부 API 연동: 다양한 서비스와 통합 가능")
print("  4. 확장성: 필요에 따라 새로운 도구 추가")
print("=" * 60)
