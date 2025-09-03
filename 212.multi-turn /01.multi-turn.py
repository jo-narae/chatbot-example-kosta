import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1) 환경변수 로드 및 설정
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("환경변수 GOOGLE_API_KEY 가 설정되지 않았습니다.")
genai.configure(api_key=api_key)

# 2) 페르소나(시스템 인스트럭션)
system_instruction = (
    "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
    "불명확하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
)

# 3) 모델 준비
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=system_instruction
)

# 4) 멀티턴 채팅 세션 시작 (history 유지)
chat = model.start_chat(history=[])   # 최초엔 비워두고 시작

# 5) 대화 루프
print("대화를 시작합니다. 'exit'으로 종료, 'reset'으로 히스토리 초기화.")
while True:
    try:
        user_input = input("사용자: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n종료합니다.")
        break

    if user_input.lower() == "exit":
        print("종료합니다.")
        break

    if user_input.lower() == "reset":
        chat = model.start_chat(history=[])
        print("히스토리를 초기화했어요.")
        continue

    # 멀티턴: 이전 turns가 자동으로 반영됨
    response = chat.send_message(
        user_input,
        generation_config={"temperature": 0.9}  # 창의성 조절
        # safety_settings=...  # 필요시 안전 설정 추가 가능
    )

    # 응답 출력
    print("AI:", response.text)

    # (선택) 현재까지 히스토리 길이 확인
    # print(f"(history turns: {len(chat.history)})")