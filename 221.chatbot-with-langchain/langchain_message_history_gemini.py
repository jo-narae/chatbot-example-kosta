import os
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory  # 메모리에 대화 기록을 저장하는 클래스
from langchain_core.runnables.history import RunnableWithMessageHistory  # 메시지 기록을 활용해 실행 가능한 래퍼 클래스
from langchain_core.messages import HumanMessage  # 사용자 메시지를 표현하는 클래스
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini 모델을 사용하는 랭체인 클래스

# -----------------------------
# 1. 환경 변수 로드 및 키 확인
# -----------------------------
load_dotenv()  # .env 파일에서 환경변수를 불러오기
api_key = os.getenv("GOOGLE_API_KEY")  # GOOGLE_API_KEY 값 가져오기
if not api_key:
    raise ValueError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")

print("✅ 환경변수가 성공적으로 로드되었습니다.")

# -----------------------------
# 2. Gemini 모델 초기화
# -----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # 사용할 Gemini 모델 지정
    temperature=0.7,  # 창의성/랜덤성 조절
    model_kwargs={
        "system_instruction": (
            "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
            "모호하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
        )
    },
)

print("✅ Gemini 모델이 초기화되었습니다.")

# -----------------------------
# 3. 세션별 대화 기록 관리
# -----------------------------
store = {}  # 세션 ID별로 대화 기록을 저장할 딕셔너리

# 세션 ID에 따른 대화 기록 반환 (없으면 새로 생성)
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()  # 메모리 기반 히스토리 생성
    return store[session_id]

# 모델 실행 시 대화 기록을 자동으로 입출력에 붙여주는 래퍼
with_message_history = RunnableWithMessageHistory(model, get_session_history)

print("✅ 메시지 히스토리 관리 시스템이 설정되었습니다.")

# -----------------------------
# 4. 세션별 대화 예시 실행
# -----------------------------
# 세션 abc2 생성
config = {"configurable": {"session_id": "abc2"}}

# 첫 메시지: 자기소개
response = with_message_history.invoke(
    [HumanMessage(content="안녕? 난 김철수이야.")],
    config=config,
)
print("🤖 Gemini 응답:")
print(response.content)

# 같은 세션에서 이름 확인
response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config,
)
print("🤖 Gemini 응답:")
print(response.content)

# 새 세션 abc3에서 질문
config_new = {"configurable": {"session_id": "abc3"}}
response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config_new,
)
print("🤖 Gemini 응답 (새로운 세션):")
print(response.content)

# 다시 abc2 세션으로 돌아가기
config = {"configurable": {"session_id": "abc2"}}
response = with_message_history.invoke(
    [HumanMessage(content="아까 우리가 무슨 얘기 했지?")],
    config=config,
)
print("🤖 Gemini 응답 (원래 세션 복귀):")
print(response.content)

# -----------------------------
# 5. 스트리밍 응답 받기
# -----------------------------
print("🤖 Gemini 스트리밍 응답:")
print("="*50)

for r in with_message_history.stream(
    [HumanMessage(content="내가 어느 나라 사람인지 추측하고, 그 나라 문화 한 가지를 말해줘")],
    config=config,
):
    print(getattr(r, "content", ""), end="", flush=True)

print("\n" + "="*50)

# -----------------------------
# 6. 세션 상태 출력
# -----------------------------
print("📊 현재 활성 세션들:")
for session_id in store.keys():
    history = store[session_id]
    message_count = len(history.messages)
    print(f"  - 세션 {session_id}: {message_count}개 메시지")

print(f"\n📈 총 {len(store)} 개의 세션이 활성화되어 있습니다.")

# 특정 세션 대화 기록 출력
session_to_check = "abc2"
if session_to_check in store:
    print(f"💬 세션 '{session_to_check}'의 대화 기록:")
    print("-" * 40)
    for i, message in enumerate(store[session_to_check].messages, 1):
        speaker = "👤 사용자" if message.__class__.__name__ == "HumanMessage" else "🤖 AI"
        print(f"{i}. {speaker}: {message.content[:100]}{'...' if len(message.content) > 100 else ''}")
else:
    print(f"❌ 세션 '{session_to_check}'를 찾을 수 없습니다.")

# -----------------------------
# 7. 새로운 주제로 대화 이어가기
# -----------------------------
config = {"configurable": {"session_id": "abc2"}}  # 기존 세션 계속 사용
response = with_message_history.invoke(
    [HumanMessage(content="오늘 날씨가 좋다면 뭘 하면 좋을까?")],
    config=config,
)
print("🤖 Gemini 응답:")
print(response.content)

# 이전 대화 맥락 확인
response = with_message_history.invoke(
    [HumanMessage(content="아까 내 이름과 함께 추천해줄 수 있어?")],
    config=config,
)
print("🤖 Gemini 응답 (이름 기억 + 맥락 연결):")
print(response.content)
