"""
Step 2-2: 멀티 턴 대화 (Multi-turn Conversation)

대화 히스토리를 유지하여 이전 대화 내용을 기억하는 챗봇을 구현합니다.
연속적인 대화가 가능하며, 맥락을 이해할 수 있습니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# 프로젝트 루트의 .env 파일 로드
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / ".env")

# API 키 확인
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

genai.configure(api_key=api_key)

print("=" * 60)
print("멀티 턴 대화 챗봇 (대화 히스토리 유지)")
print("=" * 60)
print()
print("설명: 이전 대화 내용을 기억하여 맥락 있는 대화가 가능합니다.")
print("명령어:")
print("  - exit/quit: 종료")
print("  - reset: 대화 히스토리 초기화")
print("  - history: 현재까지의 대화 히스토리 확인")
print()
print("=" * 60)
print()

# System Instruction 설정
system_instruction = (
    "너는 사용자를 도와주는 친절한 AI 어시스턴트입니다. "
    "이전 대화 내용을 기억하고, 맥락에 맞는 답변을 제공하세요. "
    "필요하면 추가 질문을 하여 사용자를 도와주세요."
)

# 모델 초기화
model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction=system_instruction
)

# 멀티턴 채팅 세션 시작 (히스토리 유지)
chat = model.start_chat(history=[])

print("💬 대화를 시작합니다...\n")

# 대화 루프
conversation_count = 0

while True:
    try:
        user_input = input("👤 사용자: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n챗봇을 종료합니다. 안녕히 가세요!")
        break

    # 빈 입력 처리
    if not user_input:
        print("⚠️ 질문을 입력해주세요.\n")
        continue

    # 종료 명령
    if user_input.lower() in ["exit", "quit", "종료"]:
        print("\n챗봇을 종료합니다. 안녕히 가세요!")
        break

    # 히스토리 초기화 명령
    if user_input.lower() in ["reset", "초기화"]:
        chat = model.start_chat(history=[])
        conversation_count = 0
        print("✅ 대화 히스토리를 초기화했습니다.\n")
        continue

    # 히스토리 확인 명령
    if user_input.lower() in ["history", "히스토리"]:
        print(f"\n📊 현재 대화 턴 수: {len(chat.history) // 2}")
        print(f"   총 메시지 수: {len(chat.history)}")
        if len(chat.history) > 0:
            print("\n대화 내역:")
            for i, msg in enumerate(chat.history):
                role = "사용자" if msg.role == "user" else "AI"
                content = msg.parts[0].text[:50] + "..." if len(msg.parts[0].text) > 50 else msg.parts[0].text
                print(f"   [{i+1}] {role}: {content}")
        print()
        continue

    try:
        # 멀티턴 대화: 이전 히스토리가 자동으로 반영됨
        response = chat.send_message(
            user_input,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )

        conversation_count += 1
        print(f"🤖 AI: {response.text}")
        print(f"   (대화 턴: {conversation_count})\n")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}\n")

print()
print("=" * 60)
print("💡 학습 포인트:")
print("  1. chat.start_chat()으로 대화 세션 생성")
print("  2. chat.send_message()로 메시지 전송")
print("  3. 이전 대화 내용이 자동으로 컨텍스트에 포함됨")
print("  4. chat.history로 대화 히스토리 확인 가능")
print()
print("다음 단계:")
print("  cd ../step-03-prompt-engineering")
print("  uv run python 01_zero_shot.py")
print("=" * 60)
