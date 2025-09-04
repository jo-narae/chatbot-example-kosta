# LangChain 챗봇 개발 및 LangSmith 추적 가이드

LangChain을 사용한 챗봇 개발과 LangSmith를 통한 애플리케이션 추적 및 모니터링 방법을 설명합니다.

## 📋 목차

1. [LangChain 챗봇 기본](#-langchain-챗봇-기본)
2. [LangSmith 소개](#-langsmith-소개)
3. [LangSmith 설정](#-langsmith-설정)
4. [추적 기능 활용](#-추적-기능-활용)
5. [실제 구현 예제](#-실제-구현-예제)
6. [문제 해결](#-문제-해결)

## 🤖 LangChain 챗봇 기본

### 프로젝트 구조
```
221.chatbot-with-langchain/
├── 00.setting.md                          # 환경 설정 가이드
├── 01.langchain.py                        # 기본 LangChain 챗봇
├── langchain_message_history_gemini.py    # 대화 히스토리 기능 포함
├── langchain_message_history_gemini.ipynb # Jupyter 노트북 버전
├── langchain_message_history.ipynb        # 대화 히스토리 기본 예제
├── jupyter_installation_guide.md          # Jupyter 설치 가이드
└── README.md                              # 이 파일
```

### 주요 파일 설명

- **01.langchain.py**: LangChain 기본 사용법
- **langchain_message_history_gemini.py**: Gemini API + 대화 히스토리 구현
- **langchain_message_history_gemini.ipynb**: 노트북으로 단계별 학습

## 📊 LangSmith 소개

### LangSmith란?
LangSmith는 LLM 애플리케이션 개발, 모니터링, 테스트를 위한 플랫폼입니다.

### 핵심 기능
- **실행 추적**: 모든 LLM 호출과 체인 실행 추적
- **성능 분석**: 응답 시간, 토큰 사용량 분석
- **에러 모니터링**: 실패 원인 분석 및 디버깅
- **비용 관리**: 토큰 사용량 기반 과금 정보 확인

## 🔧 LangSmith 설정

### 1. 계정 생성
1. [LangSmith 사이트](https://smith.langchain.com) 접속
2. 계정 생성 및 로그인
3. API 키 발급

### 2. 환경변수 설정

`.env` 파일에 다음 내용 추가:

```bash
# Gemini API (기본)
GOOGLE_API_KEY=your_gemini_api_key_here

# LangSmith 설정
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=my-chatbot-project
```

### 3. 코드에서 활성화

#### 방법 1: 환경변수 자동 로드
```python
from dotenv import load_dotenv
load_dotenv()

# LangSmith가 자동으로 활성화됩니다
```

#### 방법 2: 코드에서 직접 설정
```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your_api_key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

#### 방법 3: langchain-teddynote 패키지 사용
```python
from langchain_teddynote import logging

# 간편한 설정
logging.langsmith("my-project-name")
```

## 📈 추적 기능 활용

### 프로젝트 단위 모니터링
LangSmith 대시보드에서 확인 가능한 정보:

- **실행 횟수**: 총 체인 실행 횟수
- **성공/실패율**: 에러 발생률 모니터링
- **토큰 사용량**: 입력/출력 토큰 사용 현황
- **비용 추적**: 토큰 기반 과금 정보
- **응답 시간**: 평균/최대/최소 응답 시간

### 개별 실행 세부 추적
각 실행에 대해 다음 정보 제공:

1. **입력/출력 데이터**
   - 사용자 질문
   - AI 응답
   - 중간 처리 단계

2. **성능 메트릭**
   - 실행 시간
   - 토큰 사용량 (입력/출력)
   - 메모리 사용량

3. **체인 실행 흐름**
   - 각 체인 컴포넌트별 실행 상태
   - 에러 발생 지점 추적
   - 디버깅 정보

## 💻 실제 구현 예제

### 기본 챗봇 with LangSmith 추적

```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# LangSmith 추적 활성화
load_dotenv()

# Gemini 모델 초기화
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

# 질문 실행 (자동으로 LangSmith에 추적됨)
response = llm.invoke("안녕하세요! 파이썬에 대해 설명해주세요.")
print(response.content)
```

### 대화 히스토리 with LangSmith

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 메모리 설정
memory = ConversationBufferMemory()

# 대화 체인 생성
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # 추적 정보 출력
)

# 연속 대화 (모든 과정이 LangSmith에 기록됨)
print(conversation.predict(input="안녕하세요!"))
print(conversation.predict(input="파이썬이 뭔가요?"))
print(conversation.predict(input="파이썬의 장점은 무엇인가요?"))
```

## 🚀 실행 방법

### 1. 환경 설정
```bash
# 프로젝트 루트로 이동
cd /Users/devpeng/Documents/GitHub/Kosta-chatbot

# 가상환경 활성화
source .venv/bin/activate

# 221.chatbot-with-langchain 폴더로 이동
cd 221.chatbot-with-langchain
```

### 2. 기본 챗봇 실행
```bash
# 기본 LangChain 챗봇 실행
python 01.langchain.py
```

### 3. 대화 히스토리 챗봇 실행
```bash
# 대화 히스토리 기능 포함 챗봇 실행
python langchain_message_history_gemini.py
```

### 4. Jupyter 노트북 실행
```bash
# Jupyter Lab 실행
jupyter lab

# langchain_message_history_gemini.ipynb 파일 열기
```

## 📊 LangSmith 대시보드 활용

### 추적 결과 확인 방법

1. **LangSmith 웹 대시보드 접속**
   - https://smith.langchain.com 로그인

2. **프로젝트 선택**
   - 설정한 `LANGCHAIN_PROJECT` 이름으로 프로젝트 찾기

3. **실행 내역 확인**
   - 각 대화/질문별 세부 실행 과정
   - 토큰 사용량 및 비용
   - 에러 발생 시 상세 로그

### 주요 메트릭 해석

- **Latency**: 응답 지연 시간 (밀리초)
- **Total Tokens**: 총 토큰 사용량
- **Prompt Tokens**: 입력 토큰
- **Completion Tokens**: 출력 토큰
- **Cost**: 예상 비용 (USD)

## ❗ 문제 해결

### 1. LangSmith 추적이 안 되는 경우

```python
# 환경변수 확인
import os
print("LANGCHAIN_TRACING_V2:", os.environ.get("LANGCHAIN_TRACING_V2"))
print("LANGCHAIN_API_KEY:", os.environ.get("LANGCHAIN_API_KEY"))
print("LANGCHAIN_PROJECT:", os.environ.get("LANGCHAIN_PROJECT"))
```

### 2. API 키 오류
```
ValueError: LANGCHAIN_API_KEY not found
```

**해결방법:**
- `.env` 파일에 올바른 LangSmith API 키 설정 확인
- 키에 따옴표나 공백이 없는지 확인

### 3. 프로젝트가 생성되지 않는 경우
```
Project not found error
```

**해결방법:**
```python
# 프로젝트를 코드에서 명시적으로 설정
os.environ["LANGCHAIN_PROJECT"] = "my-new-project"
```

### 4. 추적 비활성화하고 싶은 경우
```python
# 일시적 비활성화
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# 또는 환경변수 삭제
del os.environ["LANGCHAIN_TRACING_V2"]
```

## 🎯 추천 워크플로

### 개발 단계
1. **로컬 개발**: LangSmith 추적 활성화하여 디버깅
2. **기능 테스트**: 다양한 시나리오로 실행 추적
3. **성능 분석**: 토큰 사용량 및 응답시간 최적화

### 배포 단계
1. **스테이징**: 실제 데이터로 성능 검증
2. **프로덕션**: 에러 모니터링 및 사용량 추적
3. **최적화**: LangSmith 데이터 기반 개선

## 📚 참고 자료

- [LangSmith 공식 문서](https://docs.smith.langchain.com/)
- [LangChain 공식 문서](https://python.langchain.com/docs/get_started/introduction)
- [Gemini API 문서](https://ai.google.dev/gemini-api/docs)
- [LangSmith 추적 설정 가이드](https://wikidocs.net/250954)

---

🎉 **LangSmith 추적을 활용하여 더 효율적인 LLM 애플리케이션을 개발하세요!**

## 💡 추가 팁

### 패키지 관리
```bash
# 필요한 패키지 설치
uv add langchain
uv add langchain-google-genai
uv add langsmith
uv add langchain-teddynote  # 선택사항
```

### 환경별 설정 관리
```python
# 개발/프로덕션 환경 분리
ENVIRONMENT = "development"  # or "production"
LANGCHAIN_PROJECT = f"chatbot-{ENVIRONMENT}"
```