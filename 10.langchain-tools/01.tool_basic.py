"""
LangChain Tool 정의 기본

@tool 데코레이터로 커스텀 도구를 만들고, LLM이 도구를 선택하는 과정을 확인합니다.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# ── 1단계: 도구 만들기 ──
# @tool 데코레이터를 붙이면 일반 함수가 LLM이 호출할 수 있는 "도구"가 됩니다.
# docstring이 곧 도구 설명이 되므로 반드시 작성해야 합니다.

@tool
def get_current_time() -> str:
    """현재 시간을 반환합니다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def get_word_length(word: str) -> int:
    """주어진 단어의 글자 수를 반환합니다."""
    return len(word)

# 만든 도구 확인
print("=" * 50)
print("1단계: 도구 정의 확인")
print("=" * 50)
print(f"도구 이름: {get_current_time.name}")
print(f"도구 설명: {get_current_time.description}")
print(f"직접 호출: {get_current_time.invoke({})}")
print()
print(f"도구 이름: {get_word_length.name}")
print(f"도구 설명: {get_word_length.description}")
print(f"직접 호출: {get_word_length.invoke({'word': '안녕하세요'})}")

# ── 2단계: LLM에 도구 연결하기 ──
# bind_tools()로 LLM에게 "이런 도구들을 쓸 수 있어"라고 알려줍니다.

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
tools = [get_current_time, get_word_length]
llm_with_tools = llm.bind_tools(tools)

print()
print("=" * 50)
print("2단계: LLM이 도구를 선택하는지 확인")
print("=" * 50)

# LLM에게 질문하면, 직접 답하지 않고 어떤 도구를 쓸지 "제안"합니다.
response = llm_with_tools.invoke("지금 몇 시야?")

print(f"\n[질문] 지금 몇 시야?")
print(f"[LLM 응답 텍스트] {response.content}")
print(f"[LLM이 선택한 도구] {response.tool_calls}")

# ── 3단계: 도구 직접 실행하기 ──
# LLM은 도구를 "선택"만 합니다. 실제 실행은 우리가 해야 합니다.

print()
print("=" * 50)
print("3단계: 선택된 도구 직접 실행")
print("=" * 50)

if response.tool_calls:
    tc = response.tool_calls[0]
    print(f"호출할 도구: {tc['name']}")
    print(f"전달할 인자: {tc.get('args', {})}")

    # 이름으로 도구 찾아서 실행
    tool_map = {t.name: t for t in tools}
    result = tool_map[tc["name"]].invoke(tc.get("args", {}))
    print(f"실행 결과: {result}")

print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print("1. @tool 데코레이터 → 함수를 도구로 변환")
print("2. bind_tools() → LLM에 도구 목록 알려주기")
print("3. LLM은 도구를 '선택'만 하고, 실행은 별도로 해야 함")
print("→ 다음 파일(02)에서 이 과정을 자동화하는 Agent를 배웁니다!")
