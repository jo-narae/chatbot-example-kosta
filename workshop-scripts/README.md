# 워크샵 Python 스크립트 모음

VSCode Jupyter Notebook 호환 문제 해결을 위해 모든 예제를 Python 스크립트로 재구성한 폴더입니다.

## 📂 폴더 구조

```
workshop-scripts/
├── step-01-setup/              # 환경 설정 및 확인
├── step-02-basic-chatbot/      # Gemini API 기본 사용
├── step-03-prompt-engineering/ # 프롬프트 엔지니어링
├── step-04-web-ui/             # Streamlit 웹 인터페이스
├── step-05-langchain-basic/    # LangChain 기본
├── step-06-langchain-advanced/ # LangChain 고급 (LCEL, Tool, 스트리밍)
└── step-07-rag-system/         # RAG 시스템
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 프로젝트 루트로 이동
cd c:\Users\jo-ceo\Downloads\chatbot-ex-1

# 가상환경 활성화 (이미 되어 있으면 생략)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 의존성 설치
uv sync
```

### 2. 환경변수 설정
`.env` 파일 생성 (프로젝트 루트에):
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. 단계별 실행

#### Step 1: 환경 설정 확인
```bash
cd workshop-scripts/step-01-setup
uv run python 01_test_environment.py
uv run python 02_test_gemini_api.py
```

#### Step 2: 기본 챗봇
```bash
cd ../step-02-basic-chatbot
uv run python 01_single_turn.py
uv run python 02_multi_turn.py
```

#### Step 3: 프롬프트 엔지니어링
```bash
cd ../step-03-prompt-engineering
uv run python 01_zero_shot.py
uv run python 02_one_shot.py
uv run python 03_few_shot.py
```

#### Step 4: 웹 인터페이스
```bash
cd ../step-04-web-ui
uv run streamlit run 01_streamlit_chatbot.py
```

#### Step 5: LangChain 기본
```bash
cd ../step-05-langchain-basic
uv run python 01_langchain_intro.py
uv run python 02_message_history.py
uv run python 03_langsmith_tracing.py
```

#### Step 6: LangChain 고급
```bash
cd ../step-06-langchain-advanced
uv run python 01_lcel_chain.py
uv run python 02_custom_tools.py
uv run python 03_streaming_output.py
```

#### Step 7: RAG 시스템
```bash
cd ../step-07-rag-system
uv run python 01_prepare_data.py
uv run python 02_build_vectordb.py
uv run python 03_rag_chatbot.py
```

## 📝 각 단계별 학습 목표

### Step 1: 환경 설정
- Python 환경 확인
- Gemini API 키 테스트
- 기본 설정 검증

### Step 2: 기본 챗봇
- 단일 턴 대화 구현
- 멀티 턴 대화 및 히스토리 관리
- Gemini API 기본 사용법

### Step 3: 프롬프트 엔지니어링
- Zero-shot: 예시 없이 작업 수행
- One-shot: 하나의 예시로 학습
- Few-shot: 여러 예시로 정확도 향상

### Step 4: 웹 인터페이스
- Streamlit 기본 사용법
- session_state를 활용한 상태 관리
- 채팅 UI 구현

### Step 5: LangChain 기본
- LangChain 소개 및 기본 개념
- 메시지 히스토리 관리
- LangSmith를 활용한 추적

### Step 6: LangChain 고급
- LCEL(LangChain Expression Language)
- 커스텀 도구 생성 및 활용
- 스트리밍 출력 구현

### Step 7: RAG 시스템
- 문서 전처리 및 청킹
- 벡터 데이터베이스 구축
- RAG 기반 질의응답 시스템

## 💡 사용 팁

### 빠른 테스트
각 폴더의 파일들을 순서대로 실행하세요:
```bash
# 예: Step 2의 모든 예제 실행
cd step-02-basic-chatbot
uv run python 01_single_turn.py
uv run python 02_multi_turn.py
```

### 특정 단계만 실습
```bash
# LangChain만 집중 학습
cd step-05-langchain-basic
uv run python 01_langchain_intro.py
uv run python 02_message_history.py
uv run python 03_langsmith_tracing.py
```

### 전체 워크샵 진행
각 step 폴더를 순서대로 진행하면 됩니다.

## 🔗 관련 문서

- [전체 실행 가이드](../EXECUTION_GUIDE.md)
- [프로젝트 README](../README.md)
- [Claude 작업 가이드](../CLAUDE.md)

## 📦 필요한 패키지

모든 필요한 패키지는 프로젝트 루트의 `pyproject.toml`에 정의되어 있습니다.

```bash
# 의존성 설치
uv sync

# 특정 패키지만 추가
uv add <package_name>
```

## ❓ 문제 해결

### API 키 오류
```bash
# .env 파일 확인
cat ../.env  # macOS/Linux
type ..\.env  # Windows
```

### 패키지 없음 오류
```bash
# 프로젝트 루트로 이동 후
uv sync
```

### 포트 충돌 (Streamlit)
```bash
# 다른 포트 사용
uv run streamlit run app.py --server.port 8502
```

---

**Happy Learning! 🎉**
