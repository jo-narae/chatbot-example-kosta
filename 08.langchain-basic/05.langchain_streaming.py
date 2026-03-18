"""
LangChain 스트리밍 출력

응답이 한꺼번에 나오는 대신, 한 글자씩 실시간으로 출력됩니다.
→ ChatGPT처럼 글자가 타이핑되는 효과!
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

# ── 일반 호출: 전체 응답이 한번에 나옴 ──
print("=" * 50)
print("[비교 1] 일반 호출 - 응답이 한번에!")
print("=" * 50)

response = llm.invoke("파이썬의 장점 3가지를 간단히 알려줘.")
print(response.content)

# ── 스트리밍 호출: 한 글자씩 나옴 ──
print()
print("=" * 50)
print("[비교 2] 스트리밍 - 글자가 하나씩!")
print("=" * 50)

# .stream()을 쓰면 토큰 단위로 조각이 날아옵니다
for chunk in llm.stream("파이썬의 장점 3가지를 간단히 알려줘."):
    print(chunk.content, end="", flush=True)

print()  # 줄바꿈

# ── 스트리밍 대화 루프 ──
print()
print("=" * 50)
print("[체험] 스트리밍 대화 - 직접 해보세요!")
print("=" * 50)
print("종료: exit")

while True:
    try:
        user_input = input("\n사용자: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n종료합니다.")
        break

    if not user_input:
        continue
    if user_input.lower() == "exit":
        print("종료합니다.")
        break

    print("AI: ", end="")
    for chunk in llm.stream(user_input):
        print(chunk.content, end="", flush=True)
    print()

print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print("일반: response = llm.invoke(질문)       → 한번에 받기")
print("스트리밍: for chunk in llm.stream(질문)  → 조각씩 받기")
print("→ 07.streamlit에서 st.write_stream()이 바로 이 원리입니다!")
