# 🤖 Kosta 챗봇 개발 워크샵

**1일 챗봇 개발 워크샵을 위한 완전한 교육 자료 저장소**

Gemini API부터 LangChain, RAG까지 단계적으로 배우는 실습 중심 챗봇 개발 가이드

## 📋 목차

1. [프로젝트 개요](#-프로젝트-개요)
2. [환경 설정](#-환경-설정)
3. [워크샵 진행 순서](#-워크샵-진행-순서)
4. [학습 단계별 가이드](#-학습-단계별-가이드)
5. [주요 개념 및 기술](#-주요-개념-및-기술)
6. [실행 방법](#-실행-방법)
7. [문제 해결](#-문제-해결)

## 🎯 프로젝트 개요

### 목적
- **교육 중심**: 1일 워크샵에 최적화된 단계적 학습 과정
- **실습 위주**: 이론보다는 직접 구현하며 배우는 방식
- **현실적 예제**: 실무에서 바로 활용 가능한 예제 중심
- **확장 가능**: 기본부터 고급까지 점진적 발전

### 학습 목표
- Gemini API를 활용한 기본 챗봇 개발
- LangChain을 통한 고급 챗봇 기능 구현
- RAG(Retrieval-Augmented Generation) 시스템 이해
- 실무 배포 가능한 챗봇 애플리케이션 완성

## 🛠️ 환경 설정

### 1. 시스템 요구사항
- **Python**: 3.10 이상
- **패키지 매니저**: UV (권장) 또는 pip
- **운영체제**: Windows, macOS, Linux

### 2. 필수 설치

#### Python 및 UV 설치
```bash
# Python 3.10+ 설치 확인
python --version

# UV 패키지 매니저 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경 생성
uv venv --python 3.13
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

#### 기본 패키지 설치
```bash
# 환경 변수 관리
uv pip install python-dotenv

# Gemini API SDK
uv pip install google-generativeai

# 웹 인터페이스
uv pip install streamlit

# 노트북 환경
uv pip install jupyter jupyterlab
```

#### LangChain 및 RAG 관련 패키지
```bash
# LangChain 생태계
uv pip install langchain langchain-google-genai

# RAG 시스템용
uv pip install langchain-chroma chromadb pandas

# 추적 및 모니터링 (선택사항)
uv pip install langsmith
```

### 3. 환경변수 설정

`.env` 파일 생성:
```bash
# Gemini API 키 (필수)
GOOGLE_API_KEY=your_gemini_api_key_here

# LangSmith 설정 (선택사항)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=kosta-chatbot-workshop
```

### 4. API 키 발급

#### Gemini API 키 발급
1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. 계정 로그인 후 API 키 생성
3. `.env` 파일에 추가

#### LangSmith API 키 발급 (선택사항)
1. [LangSmith](https://smith.langchain.com) 접속
2. 계정 생성 후 API 키 발급
3. `.env` 파일에 추가

## 📚 워크샵 진행 순서

### Phase 1: 기초 다지기 (2시간)
1. **환경 설정 및 확인** → `000.settings/`
2. **기본 Gemini API 활용** → `211~215/`
3. **Streamlit으로 웹 인터페이스** → `216.streamlit/`

### Phase 2: LangChain 도입 (2시간)
4. **LangChain 기본 사용법** → `221.chatbot-with-langchain/`
5. **체인과 프롬프트 관리** → `222.lcel-chain/`
6. **도구와 에이전트 활용** → `223.langchain-agent-tools/`

### Phase 3: 고급 기능 (2시간)
7. **스트리밍 출력 구현** → `224.stream-output/`
8. **RAG 시스템 구축** → `231.rag-chatbot/`

### Phase 4: 종합 실습 (2시간)
9. **LangSmith 추적 및 모니터링**
10. **성능 최적화 및 배포 준비**

## 🎓 학습 단계별 가이드

### 📁 000.settings - 환경 설정
**학습 목표**: 개발 환경 구축 및 기본 설정

- **주요 내용**: Python, UV, 가상환경 설정
- **예상 시간**: 30분
- **핵심 파일**: `00.setting.md`, `01.test.py`

```bash
# 환경 확인
.venv/bin/python --version
python 01.test.py
```

### 📁 211.single-turn - 단일 대화
**학습 목표**: Gemini API 기본 사용법 익히기

- **핵심 개념**: API 키 설정, 모델 초기화, 단일 요청-응답
- **주요 기능**: System instruction, Temperature 조절
- **예상 시간**: 20분

```python
# 핵심 코드 패턴
model = genai.GenerativeModel("gemini-2.0-flash", system_instruction="...")
response = model.generate_content(user_input)
```

### 📁 212.multi-turn - 다중 대화
**학습 목표**: 대화 컨텍스트 유지하기

- **핵심 개념**: Chat session, 대화 히스토리 관리
- **주요 기능**: 연속 대화, 컨텍스트 유지
- **예상 시간**: 20분

```python
# 핵심 코드 패턴
chat = model.start_chat(history=[])
response = chat.send_message(user_input)
```

### 📁 213-215 - 프롬프트 엔지니어링
**학습 목표**: 효과적인 프롬프트 작성법

- **213.zero-shot**: 예시 없이 작업 수행
- **214.one-shot**: 하나의 예시로 패턴 학습
- **215.few-shot**: 여러 예시로 정확도 향상
- **예상 시간**: 40분

### 📁 216.streamlit - 웹 인터페이스
**학습 목표**: 사용자 친화적인 웹 UI 구축

- **핵심 개념**: Streamlit 컴포넌트, 세션 상태 관리
- **주요 기능**: 채팅 인터페이스, 스트리밍 시뮬레이션
- **예상 시간**: 30분

```bash
# 실행 명령
uv run streamlit run 216.streamlit/01.streamlit.py
```

### 📁 221.chatbot-with-langchain - LangChain 도입
**학습 목표**: LangChain 기본 사용법과 LangSmith 모니터링

- **핵심 개념**: LangChain 모델, 대화 체인, 메모리 관리
- **주요 기능**: ConversationChain, LangSmith 추적
- **상세 가이드**: [README.md](./221.chatbot-with-langchain/README.md)
- **예상 시간**: 45분

### 📁 222.lcel-chain - LCEL 체인
**학습 목표**: LangChain Expression Language 활용

- **핵심 개념**: 체인 구성, 파이프라인 설계
- **주요 기능**: 프롬프트 템플릿, 체인 조합
- **예상 시간**: 30분

### 📁 223.langchain-agent-tools - 도구 활용
**학습 목표**: 에이전트와 도구 시스템 이해

- **핵심 개념**: Tool, Agent, Pydantic 스키마
- **주요 기능**: 함수 호출, 외부 API 연동
- **예상 시간**: 45분

### 📁 224.stream-output - 스트리밍 출력
**학습 목표**: 실시간 응답 스트리밍 구현

- **핵심 개념**: 스트리밍 API, 비동기 처리
- **주요 기능**: 토큰 단위 실시간 출력
- **예상 시간**: 30분

### 📁 231.rag-chatbot - RAG 시스템
**학습 목표**: 문서 검색 기반 챗봇 구현

- **핵심 개념**: 문서 임베딩, 벡터 검색, 컨텍스트 생성
- **주요 기능**: 3가지 검색 전략, 하이브리드 검색
- **상세 가이드**: [README.md](./231.rag-chatbot/README.md)
- **예상 시간**: 60분

```bash
# RAG 시스템 실행 순서
python fix_encoding.py        # 데이터 전처리
python build_vector_db.py     # 벡터 DB 구축
python retrieve_final.py      # RAG 챗봇 실행 (권장)
```

## 🧠 주요 개념 및 기술

### 1. 대화형 AI 기본 개념

#### LLM (Large Language Model)
- **정의**: 대규모 텍스트 데이터로 훈련된 언어 모델
- **특징**: 자연어 이해 및 생성, 다양한 작업 수행
- **예시**: Gemini, GPT, Claude 등

#### 프롬프트 엔지니어링
- **Zero-shot**: 예시 없이 작업 설명만으로 수행
- **One-shot**: 하나의 예시와 함께 작업 수행
- **Few-shot**: 여러 예시를 통한 패턴 학습

#### Temperature 설정
- **0.0**: 가장 예측 가능한 답변 (결정론적)
- **0.7**: 균형잡힌 창의성과 일관성
- **1.0**: 높은 창의성과 다양성

### 2. LangChain 생태계

#### 핵심 구성요소
```python
# 모델 래퍼
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template("질문: {question}")

# 체인 구성
chain = prompt | llm | StrOutputParser()
```

#### 메모리 시스템
- **ConversationBufferMemory**: 전체 대화 히스토리 보존
- **ConversationSummaryMemory**: 대화 요약을 통한 메모리 절약
- **ConversationTokenBufferMemory**: 토큰 수 기반 제한

#### 도구 및 에이전트
```python
@tool
def calculator(expression: str) -> float:
    """수학 계산을 수행합니다."""
    return eval(expression)

agent = initialize_agent(
    tools=[calculator], 
    llm=llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
```

### 3. RAG (Retrieval-Augmented Generation)

#### RAG 작동 원리
1. **문서 분할**: 텍스트를 적절한 크기로 청킹
2. **임베딩**: 문서를 벡터로 변환
3. **저장**: 벡터 데이터베이스에 저장
4. **검색**: 질문과 유사한 문서 조각 찾기
5. **생성**: 검색된 컨텍스트와 질문을 결합하여 답변 생성

#### 검색 전략
- **벡터 검색**: 의미적 유사도 기반 검색
- **키워드 검색**: 정확한 용어 매칭
- **하이브리드 검색**: 벡터 + 키워드 결합

```python
# RAG 체인 구성
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt 
    | llm 
    | StrOutputParser()
)
```

### 4. 성능 최적화

#### 캐싱 전략
- **메모리 캐싱**: 세션 내 결과 저장
- **디스크 캐싱**: 영구적 결과 저장
- **LLM 캐싱**: 동일 요청에 대한 응답 재사용

#### 비용 최적화
- **프롬프트 최적화**: 토큰 수 줄이기
- **배치 처리**: 여러 요청 묶어서 처리
- **스마트 캐싱**: 중복 요청 방지

## 🚀 실행 방법

### 개별 예제 실행

#### 1. 기본 콘솔 챗봇
```bash
# 가상환경 활성화
source .venv/bin/activate

# 단일 턴 대화
python 211.single-turn/01.single-turn.py

# 멀티 턴 대화
python 212.multi-turn/01.multi-turn.py
```

#### 2. 웹 인터페이스 챗봇
```bash
# Streamlit 앱 실행
uv run streamlit run 216.streamlit/01.streamlit.py

# 브라우저에서 http://localhost:8501 접속
```

#### 3. LangChain 챗봇
```bash
# 기본 LangChain 챗봇
python 221.chatbot-with-langchain/01.langchain.py

# 대화 히스토리 포함
python 221.chatbot-with-langchain/langchain_message_history_gemini.py
```

#### 4. RAG 시스템
```bash
cd 231.rag-chatbot/

# 1단계: 데이터 전처리
python fix_encoding.py

# 2단계: 벡터 데이터베이스 구축
python build_vector_db.py

# 3단계: RAG 챗봇 실행
python retrieve_final.py  # 권장 버전
```

### Jupyter 노트북 실행

```bash
# Jupyter Lab 실행
jupyter lab

# 또는 UV 환경에서
uv run jupyter lab

# 브라우저에서 .ipynb 파일 열기
```

### 전체 워크샵 순서대로 실행

```bash
# 1. 환경 확인
python 000.settings/01.test.py

# 2. 기본 챗봇 (10분씩)
python 211.single-turn/01.single-turn.py
python 212.multi-turn/01.multi-turn.py

# 3. 프롬프트 엔지니어링 (각 10분씩)
python 213.zero-shot\ Prompting/01.zero-shot.py
python 214.one-shot\ Prompting/01.one-shot.py
python 215.few-shot\ Prompting/01.few-shot.py

# 4. 웹 인터페이스
streamlit run 216.streamlit/01.streamlit.py

# 5. LangChain 기본
python 221.chatbot-with-langchain/01.langchain.py

# 6. RAG 시스템 (순서대로)
cd 231.rag-chatbot/
python fix_encoding.py
python build_vector_db.py
python retrieve_final.py
```

## ❗ 문제 해결

### 1. 환경 설정 문제

#### Python 버전 오류
```bash
# 현재 Python 버전 확인
python --version

# 3.10+ 버전 설치 필요
# Windows: Python.org에서 다운로드
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

#### 가상환경 활성화 실패
```bash
# 가상환경 재생성
uv venv --python 3.13 .venv

# 활성화 확인
which python  # 경로에 .venv가 포함되어야 함
```

### 2. API 키 관련 오류

#### Gemini API 키 오류
```
google.api_core.exceptions.PermissionDenied: 403 API_KEY_INVALID
```

**해결방법:**
1. [Google AI Studio](https://aistudio.google.com/app/apikey)에서 새 API 키 발급
2. `.env` 파일에 올바른 키 입력 (따옴표 없이)
3. 파일 저장 후 프로그램 재시작

#### 환경변수 로드 실패
```
AttributeError: NoneType object has no attribute 'strip'
```

**해결방법:**
```bash
# .env 파일 위치 확인
ls -la .env

# 내용 확인
cat .env

# 올바른 형식 예시
echo 'GOOGLE_API_KEY=your_actual_api_key_here' > .env
```

### 3. 패키지 설치 오류

#### UV 설치 실패
```bash
# UV 재설치
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

#### 패키지 의존성 충돌
```bash
# 가상환경 완전 재생성
rm -rf .venv
uv venv --python 3.13 .venv
source .venv/bin/activate

# 패키지 순서대로 설치
uv pip install python-dotenv
uv pip install google-generativeai
uv pip install streamlit
uv pip install langchain langchain-google-genai
```

### 4. 실행 시 오류

#### Streamlit 포트 충돌
```bash
# 다른 포트로 실행
streamlit run --server.port 8502 216.streamlit/01.streamlit.py
```

#### ChromaDB 데이터베이스 오류
```bash
# 데이터베이스 재생성
cd 231.rag-chatbot/
rm -rf database/
python build_vector_db.py
```

#### 인코딩 오류 (Windows)
```python
# 파일 상단에 추가
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 5. 성능 관련 이슈

#### 응답 속도 느림
- **원인**: 네트워크 연결, API 제한
- **해결**: 캐싱 활용, 배치 처리

#### 토큰 한도 초과
- **원인**: 긴 컨텍스트, 대화 히스토리 누적
- **해결**: 컨텍스트 길이 제한, 요약 기능 활용

## 📚 추가 자료

### 공식 문서
- [Gemini API 문서](https://ai.google.dev/gemini-api/docs)
- [LangChain 문서](https://python.langchain.com/docs/get_started/introduction)
- [Streamlit 문서](https://docs.streamlit.io/)
- [ChromaDB 문서](https://docs.trychroma.com/)

### 심화 학습 자료
- [프롬프트 엔지니어링 가이드](https://www.promptingguide.ai/)
- [RAG 시스템 설계 베스트 프랙티스](https://blog.langchain.dev/rag/)
- [LangSmith 추적 및 모니터링](https://docs.smith.langchain.com/)

### 커뮤니티
- [LangChain Discord](https://discord.gg/langchain)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Google AI 커뮤니티](https://discuss.ai.google.dev/)

## 🤝 기여하기

### 개선 제안
이슈나 개선 사항이 있다면 GitHub Issues를 통해 알려주세요.

### 코드 기여
1. Fork 후 브랜치 생성
2. 기능 추가 또는 버그 수정
3. 테스트 및 문서 업데이트
4. Pull Request 제출

---

## 📞 문의 및 지원

**워크샵 관련 문의**: GitHub Issues를 통해 질문해주세요.
**기술적 지원**: 각 단계별 README 파일을 참고하거나 코드 주석을 확인해주세요.

---

🎉 **Kosta 챗봇 개발 워크샵에서 AI의 세계를 탐험해보세요!**

**마지막 업데이트**: 2025년 9월 4일