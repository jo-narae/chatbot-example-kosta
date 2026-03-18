"""
OpenAI 직접 호출 vs LangChain 비교

같은 작업을 OpenAI로 하는 것과 LangChain으로 하는 것을 비교합니다.
→ 왜 LangChain을 쓰는지 체감할 수 있습니다.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# ══════════════════════════════════════════════════
# 방법 1: OpenAI 직접 사용 (지금까지 배운 방식)
# ══════════════════════════════════════════════════
print("=" * 50)
print("방법 1: OpenAI 직접 사용")
print("=" * 50)

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": "너는 요리 전문가야."},
        {"role": "user", "content": "김치찌개 레시피를 간단히 알려줘."},
    ],
    temperature=0.7,
)

# 응답에서 텍스트를 꺼내야 함
result = response.choices[0].message.content
print(result)

# ══════════════════════════════════════════════════
# 방법 2: LangChain 사용
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("방법 2: LangChain 사용")
print("=" * 50)

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

response = llm.invoke([
    SystemMessage(content="너는 요리 전문가야."),
    HumanMessage(content="김치찌개 레시피를 간단히 알려줘."),
])

# .content로 바로 텍스트 접근
print(response.content)

# ══════════════════════════════════════════════════
# 비교 정리
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("코드 비교")
print("=" * 50)
print()
print("OpenAI 직접:")
print('  client = OpenAI(api_key=api_key)')
print('  response = client.chat.completions.create(...)')
print('  result = response.choices[0].message.content  # 깊이 들어가야 함')
print()
print("LangChain:")
print('  llm = ChatOpenAI(model="gpt-4.1-nano")')
print('  response = llm.invoke(messages)')
print('  result = response.content  # 간단!')
print()
print("지금은 차이가 작아 보이지만...")
print("→ 체인(09), 도구(10), RAG(11)로 갈수록 LangChain의 편리함이 커집니다!")
