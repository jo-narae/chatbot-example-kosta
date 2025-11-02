"""
Step 2-1: 단일 턴 대화 (Single-turn Conversation)

Gemini API를 사용하여 기본적인 질문-응답 챗봇을 구현합니다.
각 질문은 독립적이며, 이전 대화를 기억하지 않습니다.
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
print("단일 턴 대화 챗봇")
print("=" * 60)
print()
print("설명: 각 질문은 독립적입니다. 이전 대화를 기억하지 않습니다.")
print("종료: 'exit' 또는 'quit' 입력")
print()
print("=" * 60)
print()

# System Instruction 설정 (챗봇의 페르소나)
system_instruction = "너는 친절하고 도움이 되는 AI 어시스턴트입니다. 간결하고 명확하게 답변하세요."

# 모델 초기화
model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction=system_instruction
)

# 대화 루프
while True:
    user_input = input("👤 사용자: ")

    # 종료 명령 확인
    if user_input.lower() in ["exit", "quit", "종료"]:
        print("\n챗봇을 종료합니다. 안녕히 가세요!")
        break

    # 빈 입력 처리
    if not user_input.strip():
        print("⚠️ 질문을 입력해주세요.\n")
        continue

    try:
        # Gemini API 호출
        response = model.generate_content(
            user_input,
            generation_config={
                "temperature": 0.7,  # 창의성 조절 (0.0~1.0)
                "max_output_tokens": 1000,  # 최대 출력 토큰
            }
        )

        print(f"🤖 AI: {response.text}")
        print()

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()

print()
print("=" * 60)
print("💡 학습 포인트:")
print("  1. 각 질문은 독립적으로 처리됩니다")
print("  2. 이전 대화 내용을 기억하지 못합니다")
print("  3. temperature로 응답의 창의성을 조절할 수 있습니다")
print()
print("다음 단계:")
print("  uv run python 02_multi_turn.py")
print("=" * 60)
