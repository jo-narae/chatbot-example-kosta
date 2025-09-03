import os
import time
import streamlit as st
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False
import google.generativeai as genai

# -----------------------------
# 1. 환경설정
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("환경변수 GOOGLE_API_KEY 가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=api_key)

# system_instruction = 페르소나 설정
system_instruction = (
    "너는 사용자를 도와주는 상담사야. "
    "공감적으로 짧게 답하고, 필요한 경우 되물어봐."
)

# 모델 객체
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=system_instruction
)

# -----------------------------
# 2. 세션 상태 초기화
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요? 👇"}]

# -----------------------------
# 3. 기존 메시지 출력
# -----------------------------
st.title("💬 Gemini 상담 챗봇")
st.caption("Gemini API를 이용한 멀티턴 대화 예제")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 4. 사용자 입력 처리
# -----------------------------
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 화면에 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # -----------------------------
    # 5. Gemini 응답 생성 (streaming 시뮬레이션)
    # -----------------------------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = st.session_state.chat.send_message(
            prompt,
            generation_config={"temperature": 0.9}
        )

        # chunk 단위 스트리밍 (단순 시뮬레이션)
        for chunk in response.text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # 어시스턴트 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})


    # 실행 방법
    # uv run streamlit run 216.streamlit/01.streamlit.py