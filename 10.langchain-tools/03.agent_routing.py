"""
Agent의 도구 선택 - 상황에 맞는 도구를 알아서 고른다

같은 Agent에게 다양한 질문을 던지면
Agent가 질문을 분석해서 적절한 도구를 선택하거나,
도구 없이 직접 답하거나, 여러 도구를 조합합니다.
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

# ── 도구 4개 정의 ──

@tool
def get_current_time() -> str:
    """현재 날짜와 시간을 반환합니다."""
    return datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")

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

@tool
def translate_to_english(text: str) -> str:
    """한국어 텍스트를 영어로 번역합니다. 간단한 단어/문장만 지원합니다."""
    # 간단한 사전 기반 번역 (데모용)
    dictionary = {
        "안녕하세요": "Hello",
        "감사합니다": "Thank you",
        "파이썬": "Python",
        "인공지능": "Artificial Intelligence",
        "사랑": "Love",
        "컴퓨터": "Computer",
    }
    return dictionary.get(text, f"'{text}'의 번역을 찾을 수 없습니다.")

tools = [get_current_time, calculate, get_word_length, translate_to_english]

# ── Agent 구성 ──
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "당신은 도구를 활용하여 사용자를 돕는 도우미입니다. "
     "도구가 필요하면 적절한 도구를 선택하고, "
     "도구가 필요 없는 질문에는 직접 답하세요."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ══════════════════════════════════════════════════
# 테스트: Agent가 상황에 맞게 도구를 선택하는지 관찰
# ══════════════════════════════════════════════════
print("=" * 50)
print("Agent의 도구 선택 관찰하기")
print("=" * 50)
print("verbose=True라서 Agent의 생각 과정이 보입니다!")
print("어떤 도구를 선택하는지 주목하세요.")

questions = [
    # 도구가 필요한 질문들 (어떤 도구를 고를까?)
    "지금 몇 시야?",                          # → 시간 도구
    "250 나누기 7은?",                         # → 계산기 도구
    "'프로그래밍'은 몇 글자야?",               # → 글자 수 도구
    "'감사합니다'를 영어로 뭐라고 해?",        # → 번역 도구

    # 도구가 필요 없는 질문 (직접 답할까?)
    "파이썬이 뭐야?",                          # → 도구 없이 직접 답변

    # 여러 도구를 조합해야 하는 질문
    "'인공지능'은 몇 글자이고, 영어로는 뭐야?",  # → 글자 수 + 번역 조합
]

for q in questions:
    print(f"\n{'━' * 60}")
    print(f"[질문] {q}")
    print(f"{'━' * 60}")
    result = agent_executor.invoke({"input": q})
    print(f"\n✅ [최종 답변] {result['output']}")

# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print()
print("Agent는 질문을 보고 스스로 판단합니다:")
print("  '시간 관련이네' → get_current_time 선택")
print("  '계산이네'      → calculate 선택")
print("  '번역이네'      → translate_to_english 선택")
print("  '일반 질문이네' → 도구 없이 직접 답변")
print("  '복합 질문이네' → 여러 도구 조합!")
print()
print("→ 도구의 docstring(설명)이 선택 기준이 됩니다.")
print("→ 설명을 잘 쓰면 Agent가 더 정확하게 도구를 고릅니다!")
