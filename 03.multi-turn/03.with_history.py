"""
히스토리 있는 대화 - AI가 기억하는 것처럼!

02에서 AI가 기억을 못했죠? 이번에는 이전 대화를 함께 보내봅니다.
→ 같은 질문을 해보세요. 이번에는 기억합니다!
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

client = OpenAI(api_key=api_key)

# ── 히스토리 있는 대화 루프 ──
# 이전 대화를 모두 쌓아서 함께 보냅니다.

history = []  # ← 이 리스트에 대화가 계속 쌓입니다

print("=" * 50)
print("히스토리 있는 챗봇")
print("=" * 50)
print("직접 대화해보세요!")
print("TIP: 아까처럼 '내 이름은 홍길동이야' → '내 이름이 뭐야?' 해보세요")
print("종료: exit / 히스토리 확인: history")
print("=" * 50)

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

    # 'history' 입력하면 현재 히스토리 내부를 보여줌
    if user_input.lower() == "history":
        print()
        print("-" * 40)
        print(f"현재 히스토리 (총 {len(history)}개 메시지)")
        print("-" * 40)
        for i, msg in enumerate(history):
            role = "사용자" if msg["role"] == "user" else "AI"
            print(f"  [{i}] {role}: {msg['content'][:60]}")
        print("-" * 40)
        print("→ 이 전체가 매번 API에 전달됩니다!")
        continue

    # 1. 사용자 메시지를 히스토리에 추가
    history.append({"role": "user", "content": user_input})

    # 2. 히스토리 전체를 API에 전달
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history,  # ← 이전 대화가 모두 들어있음!
        temperature=0.7,
    )

    # 3. AI 응답도 히스토리에 추가
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}")

print()
print("=" * 50)
print("02 vs 03 비교")
print("=" * 50)
print("02 (히스토리 없음): messages = [현재 메시지 1개만]")
print("03 (히스토리 있음): messages = [이전 대화 전부 + 현재 메시지]")
print()
print("핵심 코드 3줄:")
print("  1. history.append(user_message)    # 사용자 메시지 저장")
print("  2. chat(messages=history)          # 히스토리 전체 전달")
print("  3. history.append(ai_message)      # AI 응답도 저장")
print("=" * 50)
