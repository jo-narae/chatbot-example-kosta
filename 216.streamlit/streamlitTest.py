import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 초기 설정 / 키 로드
# -----------------------------
# .env 파일을 읽어 환경변수를 불러옵니다.
# GOOGLE_API_KEY 값이 있으면 기본 키로 사용합니다.
load_dotenv()
DEFAULT_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Streamlit 페이지 기본 설정 (브라우저 탭 제목, 아이콘 등)
st.set_page_config(page_title="Gemini Chat (Streamlit)", page_icon="💬")

# -----------------------------
# 사이드바: 설정 UI
# -----------------------------
st.sidebar.title("⚙️ 설정")

# API 키 입력 (기본값은 .env에서 가져온 키)
api_key = st.sidebar.text_input("GOOGLE_API_KEY", value=DEFAULT_API_KEY, type="password")

# 생성 온도(창의성) 슬라이더
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.05)

# Thinking 토큰 사용 여부 체크박스 (기본 비활성화)
thinking_off = st.sidebar.checkbox("Disable Thinking (budget=0)", value=True)

# Reset 버튼: 대화 히스토리와 시스템 지시어 초기화
if st.sidebar.button("💥 Reset Conversation"):
    st.session_state.pop("history", None)
    st.session_state.pop("system_instruction", None)
    st.rerun()

# 시스템 지시어 기본값
sys_default = (
    "너는 사용자를 도와주는 상담사야. 공감적으로 답하고, "
    "불명확하면 짧게 되물어봐. 필요하면 단계별로 안내해줘."
)

# 시스템 지시어 편집 가능 (세션 상태에 저장)
system_instruction = st.sidebar.text_area(
    "System Instruction",
    value=st.session_state.get("system_instruction", sys_default),
    height=120
)
st.session_state["system_instruction"] = system_instruction

# -----------------------------
# 유효성 체크
# -----------------------------
# API 키가 없으면 경고 후 실행 중단
if not api_key:
    st.warning("좌측 사이드바에 GOOGLE_API_KEY를 입력하세요.")
    st.stop()

# -----------------------------
# 클라이언트 생성
# -----------------------------
# Gemini API와 통신할 클라이언트 생성
client = genai.Client(api_key=api_key)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
# 대화 히스토리를 세션 상태에 저장 (첫 실행 시 빈 리스트로 초기화)
if "history" not in st.session_state:
    st.session_state.history: list[types.Content] = []

# -----------------------------
# 채팅 UI (이전 메시지 렌더)
# -----------------------------
st.title("💬 Gemini Chat (Streamlit)")
for msg in st.session_state.history:
    # role: "user" / "assistant" 구분
    role = "assistant" if msg.role == "model" else "user"
    # Content.parts 안의 텍스트를 합쳐 출력
    text = "".join(p.text for p in msg.parts if getattr(p, "text", None))
    with st.chat_message(role):
        st.markdown(text)

# -----------------------------
# 입력창
# -----------------------------
user_input = st.chat_input("메시지를 입력하세요… (exit / reset 지원)")
if user_input:
    cmd = user_input.strip().lower()

    # 명령 처리
    if cmd == "exit":
        st.info("세션을 종료하려면 페이지를 닫으세요.")
    elif cmd == "reset":
        # 히스토리 초기화 후 새로고침
        st.session_state.history = []
        st.rerun()
    else:
        # -----------------------------
        # 사용자 메시지 기록 & 출력
        # -----------------------------
        st.session_state.history.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # -----------------------------
        # 모델 호출 설정값 구성
        # -----------------------------
        cfg = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
        if thinking_off:
            cfg.thinking_config = types.ThinkingConfig(thinking_budget=0)

        # -----------------------------
        # 모델 호출 및 응답 출력
        # -----------------------------
        with st.chat_message("assistant"):
            with st.spinner("생각중…"):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=st.session_state.history,  # 지금까지의 대화 히스토리 전달
                    config=cfg,
                )
                assistant_text = response.text or "(빈 응답)"
                st.markdown(assistant_text)

        # -----------------------------
        # 모델 응답을 히스토리에 추가
        # -----------------------------
        st.session_state.history.append(
            types.Content(role="model", parts=[types.Part(text=assistant_text)])
        )