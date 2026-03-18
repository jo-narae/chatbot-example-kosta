"""
LangChain Agent - 도구 자동 실행

01에서는 LLM이 도구를 '선택'만 하고 우리가 직접 실행했습니다.
Agent는 이 과정을 자동화합니다: 질문 → 도구 선택 → 실행 → 답변까지 한번에!
"""

import os
import math
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# ── 도구 정의 (01에서 배운 것 + 계산기 추가) ──

@tool
def get_current_time() -> str:
    """현재 시간을 반환합니다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """수학 표현식을 계산합니다. 예: '2 + 2', '10 * 5', 'sqrt(16)'"""
    allowed_names = {
        "abs": abs, "round": round, "min": min, "max": max,
        "pow": pow, "sqrt": math.sqrt,
    }
    result = eval(expression, {"__builtins__": {}}, allowed_names)
    return str(float(result))

@tool
def get_word_length(word: str) -> int:
    """주어진 단어의 글자 수를 반환합니다."""
    return len(word)

tools = [get_current_time, calculate, get_word_length]

# ── Agent 만들기 ──
# Agent = LLM + 도구 + 프롬프트 (도구 선택 → 실행 → 답변을 자동으로 반복)

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

# Agent용 프롬프트 (agent_scratchpad는 Agent가 생각 과정을 기록하는 공간)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 도구를 활용하여 사용자의 질문에 정확히 답하는 도우미입니다."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Agent 생성 및 실행기 구성
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ── 테스트 ──
print("=" * 50)
print("Agent 테스트 - 도구 선택부터 실행까지 자동!")
print("=" * 50)

questions = [
    "지금 몇 시야?",
    "123 곱하기 456은 얼마야?",
    "'인공지능'이라는 단어는 몇 글자야?",
]

for q in questions:
    print(f"\n{'─' * 50}")
    print(f"[질문] {q}")
    print(f"{'─' * 50}")
    result = agent_executor.invoke({"input": q})
    print(f"\n[최종 답변] {result['output']}")

print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print("01(수동): 질문 → LLM이 도구 선택 → 우리가 실행 → 결과 확인")
print("02(Agent): 질문 → Agent가 알아서 도구 선택+실행+답변!")
print()
print("Agent 장점: 복잡한 질문도 여러 도구를 조합해서 자동으로 해결")
