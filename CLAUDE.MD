# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 목적
1일 챗봇 개발 워크샵을 위한 교육 자료 저장소입니다. 단계적 진행을 통해 OpenAI API부터 LangChain + RAG까지 체계적으로 학습할 수 있도록 구성되었습니다.

## 개발 환경
- Python 3.10+
- uv 패키지 매니저 사용
- **Python 스크립트(.py) 기반 실습**
- Streamlit for UI
- OpenAI API (gpt-4.1-nano 모델)

## 주요 명령어
```bash
# 환경 설정
uv sync                           # 의존성 설치
uv add [package]                 # 패키지 추가

# 실행 명령어
uv run python [script.py]        # Python 스크립트 실행
uv run streamlit run [file.py]   # Streamlit 앱 실행
```

## 워크샵 진행 순서
1. **01.settings**: 환경 설정 및 API 연결 테스트
2. **02~06**: OpenAI API 직접 사용 (단일/멀티턴, 프롬프트 엔지니어링)
3. **07.streamlit**: Streamlit으로 웹 UI 추가
4. **08~10**: LangChain 도입 (기본, LCEL, Tool/Agent)
5. **11.cs-chatbot**: 고객 상담 챗봇 + system prompt 한계 체험
6. **12.single-pdf-rag**: RAG 시스템 단계별 구현
7. **13.chatbot-examples**: 실전 챗봇 예제 (언어 튜터 등)

## 코드 작성 규칙

### Python 스크립트 구조
- 각 스크립트는 독립적으로 실행 가능
- 구조: docstring(설명) → import → 환경변수 로드 → 메인 로직 → 출력
- 모든 스크립트 상단에서 환경변수 로드 필수

### API 키 관리
```python
# 모든 스크립트 표준 형태
import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
```

### 스크립트 작성 예제
```python
"""
스크립트 설명 (간단한 제목)

더 자세한 설명이 필요한 경우 여기에 작성
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

# 메인 로직
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role": "user", "content": "안녕하세요"}],
    temperature=0.7,
)
print(response.choices[0].message.content)
```

### LangChain 스크립트 예제
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)
```

### 코드 스타일
- 교육 목적에 맞는 명확한 변수명 사용
- 핵심 코드에는 한글 주석 추가
- 복잡한 로직은 단계별로 분리하여 설명

## 파일 명명 규칙
- **디렉토리**: `{순번}.{주제}` (예: `01.settings`, `08.langchain-basic`)
- **Python 스크립트**: `{번호}.{설명}.py` (예: `01.langchain.py`, `01.single-turn.py`)

## 각 단계별 핵심 학습 포인트

### 02~06: OpenAI API 기본
- **02.single-turn**: 단일 대화 (01), system prompt 역할 비교 (02)
- **03.multi-turn**: 대화 루프 (01), 히스토리 없는 대화 (02), 히스토리 있는 대화 (03)
- **04~06**: Zero-shot, One-shot, Few-shot (같은 리뷰 분석 태스크로 비교)

### 07: Streamlit
- 기본 챗봇 UI (01), 사이드바 설정 + 스트리밍 (02)

### 08~10: LangChain
- **08**: LangChain 기본 (01), LangSmith (02), 메시지 히스토리 (03), OpenAI vs LangChain 비교 (04), 스트리밍 (05)
- **09**: LCEL 기본 (01), 출력 파서 (02), 프롬프트 템플릿 (03), 템플릿 대화형 활용 (04), 복잡한 체인 연결 (05)
- **10**: Tool 정의 (01), Agent 자동 실행 (02), Agent 도구 선택 관찰 (03), Wikipedia 검색 Agent (04)

### 11: 고객 상담 챗봇
- system prompt에 FAQ 넣어서 상담 챗봇 만들기 (01)
- FAQ가 많아지면? system prompt 한계 체험 → RAG 필요성 (02)

### 12: RAG
- PDF 문서 기반 RAG 시스템 단계별 구현

### 13: 실전 챗봇 예제
- 언어 회화 튜터 등 완성형 챗봇 데모

## 빠른 참조

### 전체 워크샵 실행 순서
```bash
# Phase 1: 기초
uv run python 01.settings/01.test.py
uv run python 02.single-turn/01.single-turn.py
uv run python 02.single-turn/02.system_prompt.py
uv run python 03.multi-turn/01.multi-turn.py
uv run python 03.multi-turn/02.no_history.py
uv run python 03.multi-turn/03.with_history.py
uv run python 04.zero-shot-prompting/01.zero-shot.py
uv run streamlit run 07.streamlit/01.streamlit.py
uv run streamlit run 07.streamlit/02.streamlit_chat.py

# Phase 2: LangChain
uv run python 08.langchain-basic/01.langchain.py
uv run python 08.langchain-basic/02.langsmith_example.py
uv run python 08.langchain-basic/03.message_history.py
uv run python 08.langchain-basic/04.langchain_vs_openai.py
uv run python 08.langchain-basic/05.langchain_streaming.py
uv run python 09.lcel-chain/01.lcel_basic.py
uv run python 09.lcel-chain/02.lcel_parser.py
uv run python 09.lcel-chain/03.prompt_template.py
uv run python 09.lcel-chain/04.prompt_interactive.py
uv run python 09.lcel-chain/05.lcel_complex_chain.py
uv run python 10.langchain-tools/01.tool_basic.py
uv run python 10.langchain-tools/02.tool_agent.py
uv run python 10.langchain-tools/03.agent_routing.py
uv run python 10.langchain-tools/04.tool_wikipedia.py

# Phase 3: 상담 챗봇 → RAG → 실전 예제
uv run streamlit run 11.cs-chatbot/01.cs_chatbot.py
uv run python 11.cs-chatbot/02.cs_limit.py
uv run python 12.single-pdf-rag/step1_load_pdf.py
uv run python 12.single-pdf-rag/step2_chunking.py
uv run python 12.single-pdf-rag/step3_embedding.py
uv run python 12.single-pdf-rag/step4_vector_store.py
uv run python 12.single-pdf-rag/step5_rag_chain.py
uv run streamlit run 12.single-pdf-rag/app.py
uv run streamlit run 13.chatbot-examples/01.language_tutor.py
uv run streamlit run 13.chatbot-examples/02.restaurant_recommender.py
```

## 문제 해결 가이드
- **API 에러시**: `.env` 파일의 OPENAI_API_KEY 확인
- **의존성 문제시**: `uv sync`로 재설치
- **LangChain 문법 오류시**: 공식 문서 최신 버전 확인
