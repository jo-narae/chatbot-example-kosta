import os
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# -----------------------------
# 1) 환경설정
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")
genai.configure(api_key=api_key)

# -----------------------------
# 2) Gemini 모델 (system_instruction 사용)
# -----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    system_instruction=(
        "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
        "모호하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
    ),
)

print("✅ Gemini 모델이 초기화되었습니다.")

# -----------------------------
# 3) 세션별 대화 기록 저장소
# -----------------------------
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 모델 실행 시 대화 기록을 함께 전달하는 래퍼
with_message_history = RunnableWithMessageHistory(model, get_session_history)

# -----------------------------
# 4) 테스트 실행
# -----------------------------
def main():
    print("\n" + "="*50)
    print("🤖 Gemini 메시지 히스토리 테스트 (system_instruction 기반)")
    print("="*50)

    # 동일 세션(abc2)에서 기억 확인
    config = {"configurable": {"session_id": "abc2"}}

    print("\n📝 테스트 1: 첫 번째 세션 (abc2)")
    resp = with_message_history.invoke([HumanMessage(content="안녕? 난 이성용이야.")], config=config)
    print(f"🤖 응답: {resp.content}")

    print("\n📝 테스트 2: 같은 세션에서 이름 확인")
    resp = with_message_history.invoke([HumanMessage(content="내 이름이 뭐지?")], config=config)
    print(f"🤖 응답: {resp.content}")

    # 다른 세션(abc3)에서는 모름
    print("\n📝 테스트 3: 새로운 세션 (abc3)")
    config_new = {"configurable": {"session_id": "abc3"}}
    resp = with_message_history.invoke([HumanMessage(content="내 이름이 뭐지?")], config=config_new)
    print(f"🤖 응답: {resp.content}")

    # 세션 abc2로 복귀
    print("\n📝 테스트 4: 첫 번째 세션으로 돌아가서 대화 기록 확인")
    resp = with_message_history.invoke([HumanMessage(content="아까 우리가 무슨 얘기 했지?")], config=config)
    print(f"🤖 응답: {resp.content}")

    # 스트리밍 응답
    print("\n📝 테스트 5: 스트리밍 응답")
    print("🤖 응답: ", end="")
    for r in with_message_history.stream(
        [HumanMessage(content="내가 어느 나라 사람인지 추측하고, 그 나라 문화 한 가지를 말해줘")],
        config=config,
    ):
        # r는 ChatMessage/AIMessage 조각일 수 있음 → content 이어 붙이기
        print(getattr(r, "content", ""), end="", flush=True)
    print()

if __name__ == "__main__":
    main()