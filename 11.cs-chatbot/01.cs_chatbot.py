"""
실전 챗봇 1 - 고객 상담 챗봇 (LangChain 버전)

쇼핑몰 고객 상담 챗봇입니다.
FAQ를 system prompt에 넣어 상담원처럼 응대합니다.

실행: uv run streamlit run 11.cs-chatbot/01.cs_chatbot.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# 환경설정
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    st.stop()

# ── 고객 상담 시스템 프롬프트 ──
SYSTEM_PROMPT = """너는 온라인 쇼핑몰 '해피몰'의 고객 상담 챗봇이야.

## 회사 정보
- 회사명: 해피몰
- 운영시간: 평일 09:00~18:00
- 고객센터 전화: 1588-0000
- 이메일: help@happymall.com

## 자주 묻는 질문 (FAQ)

### 배송
- 일반 배송: 결제 후 2~3 영업일 소요
- 새벽 배송: 밤 11시 전 주문 시 다음 날 아침 7시 전 도착 (수도권만)
- 배송비: 3만원 이상 무료, 미만 시 3,000원
- 배송 추적: 마이페이지 > 주문내역에서 확인 가능

### 교환/환불
- 수령 후 7일 이내 교환/환불 가능
- 단순 변심: 반품 배송비 3,000원 고객 부담
- 상품 불량: 배송비 무료, 즉시 교환 또는 전액 환불
- 환불 소요: 카드 결제 시 취소 후 3~5 영업일

### 회원/포인트
- 회원가입 시 2,000 포인트 지급
- 구매 금액의 1% 포인트 적립
- 포인트는 1,000포인트 이상부터 사용 가능
- 포인트 유효기간: 적립일로부터 1년

## 응대 규칙
1. 항상 친절하고 공손하게 답변해
2. FAQ에 있는 내용은 정확하게 안내해
3. FAQ에 없는 질문은 "고객센터(1588-0000)로 문의해 주시면 더 자세히 안내드리겠습니다"로 안내해
4. 인사에는 "해피몰입니다! 무엇을 도와드릴까요?" 로 답해
5. 답변은 3문장 이내로 간결하게 해
"""

# ── LangChain 체인 구성 ──
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.3, streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# ── Streamlit UI ──
st.title("🛒 해피몰 고객 상담")
st.caption("배송, 교환/환불, 회원/포인트에 대해 물어보세요!")

# 세션 상태 초기화
if "cs_messages" not in st.session_state:
    st.session_state.cs_messages = [
        {"role": "assistant", "content": "해피몰입니다! 무엇을 도와드릴까요? 😊"}
    ]

# 사이드바 - FAQ 바로가기
st.sidebar.title("자주 묻는 질문")
faq_questions = [
    "배송은 얼마나 걸려요?",
    "배송비가 얼마예요?",
    "교환/환불 어떻게 해요?",
    "포인트는 어떻게 쓰나요?",
    "새벽 배송 되나요?",
]
for faq in faq_questions:
    if st.sidebar.button(faq, key=f"faq_{faq}"):
        st.session_state.pending_input = faq

if st.sidebar.button("대화 초기화"):
    st.session_state.cs_messages = [
        {"role": "assistant", "content": "해피몰입니다! 무엇을 도와드릴까요? 😊"}
    ]
    st.rerun()

# 기존 메시지 출력
for msg in st.session_state.cs_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 (직접 입력 또는 FAQ 버튼)
user_input = st.chat_input("질문을 입력하세요...")
if not user_input and "pending_input" in st.session_state:
    user_input = st.session_state.pop("pending_input")

if user_input:
    st.session_state.cs_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 대화 기록을 LangChain 메시지로 변환 (마지막 user 메시지는 input으로 따로 전달)
    history = []
    for m in st.session_state.cs_messages[:-1]:
        if m["role"] == "user":
            history.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            history.append(AIMessage(content=m["content"]))

    # 스트리밍 응답
    with st.chat_message("assistant"):
        stream = chain.stream({"history": history, "input": user_input})
        response = st.write_stream(stream)

    st.session_state.cs_messages.append({"role": "assistant", "content": response})
