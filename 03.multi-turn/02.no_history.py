"""
히스토리 없는 대화 - AI가 기억을 못하는 체험

직접 대화해보세요. 이름을 알려준 뒤 "내 이름이 뭐야?"라고 물어보세요.
→ AI가 매번 기억을 잃습니다!
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

# ── 히스토리 없는 대화 루프 ──
# 매번 사용자 메시지 1개만 보냅니다. 이전 대화는 전달하지 않습니다.

print("=" * 50)
print("히스토리 없는 챗봇")
print("=" * 50)
print("직접 대화해보세요!")
print("TIP: '내 이름은 홍길동이야'라고 한 뒤, '내 이름이 뭐야?'라고 물어보세요")
print("종료: exit 입력")
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

    # 매번 새 메시지 1개만 보냄 (이전 대화 없음!)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
    )

    print(f"AI: {response.choices[0].message.content}")

print()
print("=" * 50)
print("느낀 점이 있나요?")
print("AI가 이전 대화를 전혀 기억하지 못합니다!")
print("→ 이유: 매번 메시지 1개만 보내기 때문 (Stateless)")
print("→ 해결: 03.with_history.py를 실행해보세요!")
print("=" * 50)
