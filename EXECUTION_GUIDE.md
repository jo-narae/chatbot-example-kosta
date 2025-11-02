# 실행 가이드 (Python 스크립트 방식)

VSCode 최신 버전에서 Jupyter Notebook 호환 문제로 인해, 모든 예제를 Python 스크립트(.py)로 제공합니다.

## 🚀 빠른 시작

### 1. 환경 설정 확인
```bash
# Python 버전 확인 (3.10 이상 필요)
python --version

# 가상환경 활성화
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# 또는 uv 사용:
uv venv
```

### 2. 환경변수 설정
`.env` 파일 생성:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. 의존성 설치
```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -r requirements.txt
```

## 📚 단계별 실행 방법

### Phase 1: 기초 (Gemini API 직접 사용)

#### 000. 환경 설정 확인
```bash
# 기본 테스트
uv run python 000.settings/01.test.py

# Google API 키 테스트
uv run python 000.settings/googleApiKeyTest.py
```

#### 211. 단일 턴 대화
```bash
uv run python 211.single-turn/01.single-turn.py
```

#### 212. 멀티 턴 대화
```bash
uv run python 212.multi-turn/01.multi-turn.py
```

#### 213-215. 프롬프트 엔지니어링
```bash
# Zero-shot
uv run python 213.zero-shot-prompting/01.zero-shot.py

# One-shot
uv run python 214.one-shot-prompting/01.one-shot.py

# Few-shot
uv run python 215.few-shot-prompting/01.few-shot.py
```

#### 216. Streamlit 웹 인터페이스
```bash
uv run streamlit run 216.streamlit/01.streamlit.py
```

### Phase 2: LangChain 기본

#### 221. LangChain 챗봇
```bash
# 기본 LangChain 사용법
uv run python 221.chatbot-with-langchain/01.langchain.py

# 대화 히스토리 관리
uv run python 221.chatbot-with-langchain/langchain_message_history_gemini.py

# LangSmith 추적 예제
uv run python 221.chatbot-with-langchain/02.langsmith_example.py
```

**LangSmith 설정 (선택사항)**
```bash
# .env 파일에 추가
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=kosta-chatbot-workshop
```

#### 222. LCEL 체인
```bash
# 기본 LCEL 사용법
uv run python 222.lcel-chain/01.lcel_basic.py

# Gemini와 LCEL
uv run python 222.lcel-chain/lcel_gemini.py
```

#### 223. 도구와 에이전트
```bash
# 기본 Tool 사용법
uv run python 223.langchain-agent-tools/01.tool_basic.py

# Gemini Tool 호출
uv run python 223.langchain-agent-tools/langchain_tool_gemini.py

# Pydantic 스키마
uv run python 223.langchain-agent-tools/pydantic_gemini.py
```

#### 224. 스트리밍 출력
```bash
# 기본 스트리밍
uv run python 224.stream-output/01.stream_basic.py

# Gemini 스트리밍 + Tool
uv run python 224.stream-output/langchain_tool_stream_gemini.py
```

### Phase 3: RAG 시스템

#### 231. RAG 챗봇
```bash
cd 231.rag-chatbot

# 1단계: 데이터 전처리
uv run python fix_encoding.py

# 2단계: 벡터 데이터베이스 구축
uv run python build_vector_db.py

# 3단계: RAG 챗봇 실행
uv run python retrieve_final.py  # 권장 버전

# 또는 다른 검색 전략
uv run python retrieve.py         # 기본 검색
uv run python retrieve_hybrid.py  # 하이브리드 검색
```

## 🛠️ UV 명령어 가이드

### 기본 명령어
```bash
# 패키지 추가
uv add package_name

# 최신 버전으로 업그레이드
uv add --upgrade package_name

# 의존성 동기화
uv sync

# 모든 패키지 최신화
uv sync --upgrade

# Python 스크립트 실행
uv run python script.py

# 특정 명령어 실행
uv run streamlit run app.py
```

### 자주 사용하는 패키지
```bash
# 기본 패키지
uv add python-dotenv
uv add google-generativeai

# 웹 인터페이스
uv add streamlit

# LangChain 생태계
uv add langchain
uv add langchain-google-genai
uv add langchain-core
uv add langchain-community

# RAG 관련
uv add langchain-chroma
uv add chromadb
uv add pandas

# 모니터링 (선택사항)
uv add langsmith
uv add langchain-teddynote
```

## 📝 실행 순서 요약

### 1일 워크샵 진행 순서
```bash
# 1. 환경 확인 (10분)
uv run python 000.settings/01.test.py

# 2. 기본 챗봇 (30분)
uv run python 211.single-turn/01.single-turn.py
uv run python 212.multi-turn/01.multi-turn.py

# 3. 프롬프트 엔지니어링 (40분)
uv run python 213.zero-shot-prompting/01.zero-shot.py
uv run python 214.one-shot-prompting/01.one-shot.py
uv run python 215.few-shot-prompting/01.few-shot.py

# 4. 웹 인터페이스 (30분)
uv run streamlit run 216.streamlit/01.streamlit.py

# ===== 점심 식사 =====

# 5. LangChain 기본 (45분)
uv run python 221.chatbot-with-langchain/01.langchain.py
uv run python 221.chatbot-with-langchain/langchain_message_history_gemini.py
uv run python 221.chatbot-with-langchain/02.langsmith_example.py

# 6. LCEL과 체인 (30분)
uv run python 222.lcel-chain/01.lcel_basic.py
uv run python 222.lcel-chain/lcel_gemini.py

# 7. 도구와 에이전트 (45분)
uv run python 223.langchain-agent-tools/01.tool_basic.py
uv run python 223.langchain-agent-tools/langchain_tool_gemini.py

# 8. 스트리밍 (30분)
uv run python 224.stream-output/01.stream_basic.py
uv run python 224.stream-output/langchain_tool_stream_gemini.py

# 9. RAG 시스템 (60분)
cd 231.rag-chatbot
uv run python fix_encoding.py
uv run python build_vector_db.py
uv run python retrieve_final.py
```

## 🔍 문제 해결

### API 키 오류
```bash
# .env 파일 확인
cat .env  # macOS/Linux
type .env  # Windows

# API 키 형식 확인 (따옴표 없이 작성)
GOOGLE_API_KEY=AIzaSy...
```

### 패키지 설치 오류
```bash
# 가상환경 재생성
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows

uv venv
uv sync
```

### Streamlit 포트 충돌
```bash
# 다른 포트로 실행
uv run streamlit run app.py --server.port 8502
```

### ChromaDB 오류
```bash
# 데이터베이스 재생성
cd 231.rag-chatbot
rm -rf database/  # macOS/Linux
rmdir /s database  # Windows

uv run python build_vector_db.py
```

## 💡 추가 팁

### 빠른 테스트
각 폴더에 `*Test.py` 파일이 있습니다:
```bash
uv run python 211.single-turn/singleturnTest.py
uv run python 216.streamlit/streamlitTest.py
```

### 로그 확인
```bash
# 상세 로그 출력
uv run python script.py --verbose

# 디버그 모드
export DEBUG=1  # macOS/Linux
set DEBUG=1     # Windows
```

### 성능 최적화
```bash
# 캐시 사용
export LANGCHAIN_CACHE=true

# 병렬 처리
export LANGCHAIN_PARALLEL=true
```

## 📊 학습 체크리스트

- [ ] 환경 설정 완료
- [ ] Gemini API 키 발급 및 테스트
- [ ] 단일/멀티 턴 대화 이해
- [ ] 프롬프트 엔지니어링 3가지 방식 실습
- [ ] Streamlit 웹 인터페이스 구현
- [ ] LangChain 기본 개념 이해
- [ ] LCEL 체인 구성 방법 학습
- [ ] Tool과 Agent 사용법 습득
- [ ] 스트리밍 출력 구현
- [ ] RAG 시스템 구축 및 실행
- [ ] LangSmith 모니터링 (선택사항)

---

**모든 예제는 uv run python으로 실행 가능합니다!**

궁금한 점이 있으면 각 폴더의 README.md를 참고하세요.
