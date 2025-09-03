# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 목적
1일 챗봇 개발 워크샵을 위한 교육 자료 저장소입니다. 단계적 진행을 통해 Gemini API부터 LangChain + RAG까지 체계적으로 학습할 수 있도록 구성되었습니다.

## 개발 환경
- Python 3.10+
- uv 패키지 매니저 사용
- Jupyter Notebook 기반 실습
- Streamlit for UI

## 주요 명령어
```bash
# 환경 설정
uv sync                           # 의존성 설치
uv add [package]                 # 패키지 추가
uv add --upgrade [package]       # 패키지 최신 버전으로 업그레이드

# 실행 명령어
jupyter lab                      # Jupyter Lab 실행
streamlit run [file.py]          # Streamlit 앱 실행

# 개발 도구
uv run jupyter lab               # uv 환경에서 실행
```

## 워크샵 진행 순서
1. **00-setup**: 환경 설정 및 확인
2. **01-theory**: LLM/챗봇 기본 개념
3. **02-gemini-basic**: Gemini API 직접 사용한 챗봇
4. **03-streamlit**: Streamlit으로 UI 추가
5. **04-langchain**: LangChain 도입
6. **05-rag**: RAG 시스템으로 확장

## 코드 작성 규칙

### Jupyter Notebook 구조
- 각 노트북은 독립적으로 실행 가능
- 셀 순서: 제목 → 개념설명 → 코드예제 → 실습과제
- 모든 노트북 첫 셀에서 환경변수 로드 필수

### 코드 스타일
- 교육 목적에 맞는 명확한 변수명 사용
- 핵심 코드에는 한글 주석 추가
- 복잡한 로직은 단계별로 분리하여 설명
- 에러 처리 코드 포함하여 실무적 접근

### API 키 관리
```python
# 모든 노트북 첫 셀 표준 형태
import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")
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
- 노트북: `{단계번호}-{주제}.ipynb` 
  - 예: `01-theory-basics.ipynb`
- Python 파일: snake_case
  - 예: `chatbot_app.py`
- 슬라이드: `{단계번호}-{주제}-slides`
  - 예: `02-gemini-basic-slides`

## 실습 데이터 관리
- 샘플 문서는 `documents/` 폴더에 저장
- 저작권 문제없는 공개 데이터만 사용
- 한글 문서 우선 (한국어 처리 실습 목적)

## 각 단계별 핵심 학습 포인트

### 02-gemini-basic
- Google AI Studio vs API 차이점
- 프롬프트 엔지니어링 기초
- 응답 스트리밍 처리

### 03-streamlit
- session_state 활용한 대화 기록 관리
- UI/UX 고려사항
- 배포 준비

### 04-langchain
- LangChain의 추상화 이점
- ChatModel vs LLM 차이점
- Chain 개념 도입

### 05-rag
- 문서 로딩과 청킹 전략
- 임베딩과 벡터 저장소
- 검색 정확도 향상 방법

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
- LangChain 문법 오류시: 공식 문서 최신 버전 확인
- API 에러시: 환경변수 및 API 키 유효성 검사
- 의존성 문제시: `uv sync --upgrade`로 재설치
- 패키지 충돌시: 최신 버전으로 통일 후 재시도