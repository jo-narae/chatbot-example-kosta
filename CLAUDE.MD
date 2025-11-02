# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 목적
1일 챗봇 개발 워크샵을 위한 교육 자료 저장소입니다. 단계적 진행을 통해 Gemini API부터 LangChain + RAG까지 체계적으로 학습할 수 있도록 구성되었습니다.

## 개발 환경
- Python 3.10+
- uv 패키지 매니저 사용
- **Python 스크립트(.py) 기반 실습** (VSCode Jupyter 호환 문제로 변경)
- Streamlit for UI

## 주요 명령어
```bash
# 환경 설정
uv sync                           # 의존성 설치
uv add [package]                 # 패키지 추가
uv add --upgrade [package]       # 패키지 최신 버전으로 업그레이드

# 실행 명령어 (주로 사용)
uv run python [script.py]        # Python 스크립트 실행
uv run streamlit run [file.py]   # Streamlit 앱 실행

# Jupyter (선택사항, 호환 문제 있음)
uv run jupyter lab               # uv 환경에서 실행
```

## 워크샵 진행 순서
1. **000.settings**: 환경 설정 및 확인
2. **211-215**: Gemini API 직접 사용 (단일/멀티턴, 프롬프트 엔지니어링)
3. **216.streamlit**: Streamlit으로 UI 추가
4. **221-224**: LangChain 도입 (기본, LCEL, Tool, 스트리밍)
5. **231.rag-chatbot**: RAG 시스템으로 확장

## 코드 작성 규칙

### Python 스크립트 구조 (주요 방식)
- 각 스크립트는 독립적으로 실행 가능
- 구조: 상단 주석(설명) → import → 환경변수 로드 → 메인 로직 → 출력
- 모든 스크립트 상단에서 환경변수 로드 필수
- 실행: `uv run python [script.py]`

### Jupyter Notebook (선택사항)
- VSCode 최신 버전에서 호환 문제 있음 (Python 스크립트 사용 권장)
- 각 노트북은 독립적으로 실행 가능
- 셀 순서: 제목 → 개념설명 → 코드예제 → 실습과제

### 코드 스타일
- 교육 목적에 맞는 명확한 변수명 사용
- 핵심 코드에는 한글 주석 추가
- 복잡한 로직은 단계별로 분리하여 설명
- 에러 처리 코드 포함하여 실무적 접근

### API 키 관리
```python
# 모든 스크립트/노트북 표준 형태
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")
```

### 스크립트 작성 예제
```python
"""
스크립트 설명 (간단한 제목)

더 자세한 설명이 필요한 경우 여기에 작성
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 환경변수 로드
load_dotenv()

# API 키 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

# 메인 로직
print("=" * 60)
print("예제 제목")
print("=" * 60)

# ... 코드 구현 ...

print("완료!")
```

## Context7 사용 규칙

### 언제 사용하는가
- 각 챕터의 핵심 이론 설명 슬라이드 생성시
- 복잡한 아키텍처나 플로우 다이어그램 필요시
- LangChain 문법 변경사항 정리시 (최신 버전 반영 필수)

### 슬라이드 생성 가이드
- 제목: 간결하고 명확하게
- 내용: 핵심 개념 위주, 코드 예시 포함
- 시각화: 플로우차트, 아키텍처 다이어그램 적극 활용
- 실습 연결: 각 슬라이드 후 바로 실습할 수 있도록 구성

## 파일 명명 규칙
- **Python 스크립트 (주요)**: `{번호}.{설명}.py`
  - 예: `01.langchain.py`, `01.single-turn.py`
  - 기본 예제: `01.*.py`
  - 추가 예제: `02.*.py`, `langchain_message_history_gemini.py`
- Jupyter 노트북 (선택): `{주제}.ipynb` 또는 `{주제}_gemini.ipynb`
  - 예: `lcel.ipynb`, `langchain_tool_gemini.ipynb`
- 테스트 스크립트: `*Test.py`
  - 예: `singleturnTest.py`, `streamlitTest.py`
- 슬라이드: `{단계번호}-{주제}-slides`
  - 예: `02-gemini-basic-slides`

## 실습 데이터 관리
- 샘플 문서는 `documents/` 폴더에 저장
- 저작권 문제없는 공개 데이터만 사용
- 한글 문서 우선 (한국어 처리 실습 목적)

## 각 단계별 핵심 학습 포인트

### 211-215: Gemini API 기본
- **211.single-turn**: 단일 대화 구현
- **212.multi-turn**: 대화 히스토리 관리
- **213-215**: Zero-shot, One-shot, Few-shot 프롬프트 엔지니어링
- 실행: `uv run python 211.single-turn/01.single-turn.py`

### 216: Streamlit
- session_state 활용한 대화 기록 관리
- UI/UX 고려사항
- 실행: `uv run streamlit run 216.streamlit/01.streamlit.py`

### 221-224: LangChain
- **221**: LangChain 기본, 메시지 히스토리, LangSmith 추적
- **222**: LCEL 체인 구성
- **223**: Tool과 Agent 사용법
- **224**: 스트리밍 출력
- 실행 예: `uv run python 221.chatbot-with-langchain/01.langchain.py`

### 231: RAG 시스템
- 문서 로딩과 청킹 전략
- 임베딩과 벡터 저장소
- 검색 정확도 향상 방법
- 실행 순서: `fix_encoding.py` → `build_vector_db.py` → `retrieve_final.py`

## 패키지 관리 규칙

### 최신 버전 사용 필수
- 모든 패키지는 반드시 최신 버전 사용
- 새 패키지 추가시: `uv add --upgrade [package]`
- 기존 패키지 업데이트: `uv sync --upgrade`
- 정기적으로 `uv lock --upgrade` 실행하여 모든 의존성 최신화

### 버전 확인 방법
```bash
# 설치된 패키지 버전 확인
uv pip list

# 특정 패키지 최신 버전 확인
uv add --dry-run [package]
```

## 문제 해결 가이드
- **LangChain 문법 오류시**: 공식 문서 최신 버전 확인
- **API 에러시**: 환경변수 및 API 키 유효성 검사
- **의존성 문제시**: `uv sync --upgrade`로 재설치
- **패키지 충돌시**: 최신 버전으로 통일 후 재시도
- **Jupyter 호환 문제시**: Python 스크립트(.py) 사용으로 전환
- **uv 실행 오류시**: 가상환경 활성화 후 `python` 직접 사용

## 빠른 참조

### 전체 워크샵 실행 순서
```bash
# Phase 1: 기초
uv run python 000.settings/01.test.py
uv run python 211.single-turn/01.single-turn.py
uv run python 212.multi-turn/01.multi-turn.py
uv run python 213.zero-shot-prompting/01.zero-shot.py
uv run streamlit run 216.streamlit/01.streamlit.py

# Phase 2: LangChain
uv run python 221.chatbot-with-langchain/01.langchain.py
uv run python 221.chatbot-with-langchain/langchain_message_history_gemini.py
uv run python 222.lcel-chain/01.lcel_basic.py
uv run python 223.langchain-agent-tools/01.tool_basic.py
uv run python 224.stream-output/01.stream_basic.py

# Phase 3: RAG
cd 231.rag-chatbot
uv run python fix_encoding.py
uv run python build_vector_db.py
uv run python retrieve_final.py
```

### 주요 파일 위치
- 환경 설정: `000.settings/`
- 기본 챗봇: `211.single-turn/`, `212.multi-turn/`
- 프롬프트 엔지니어링: `213-215/`
- 웹 UI: `216.streamlit/`
- LangChain: `221-224/`
- RAG: `231.rag-chatbot/`
- 실행 가이드: `EXECUTION_GUIDE.md`