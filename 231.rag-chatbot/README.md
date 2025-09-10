# RAG 챗봇 시스템 테스트 가이드

Gemini API와 LangChain을 사용한 RAG(Retrieval-Augmented Generation) 챗봇 시스템의 완전한 설치 및 실행 가이드입니다.

## 📋 목차

1. [환경 설정](#-환경-설정)
2. [패키지 설치](#-패키지-설치)
3. [데이터 준비](#-데이터-준비)
4. [벡터 데이터베이스 구축](#-벡터-데이터베이스-구축)
5. [RAG 시스템 실행](#-rag-시스템-실행)
6. [테스트 방법](#-테스트-방법)
7. [문제 해결](#-문제-해결)

## 🔧 환경 설정

### 1. 가상환경 활성화

```bash
# 프로젝트 루트 디렉토리로 이동
cd /Users/devpeng/Documents/GitHub/Kosta-chatbot

# 가상환경 활성화 (이미 생성되어 있음)
source .venv/bin/activate
```

### 2. 환경변수 설정

`.env` 파일 생성 및 Gemini API 키 추가:

```bash
# .env 파일 생성
touch .env

# API 키 설정
echo "GOOGLE_API_KEY=your_gemini_api_key_here" >> .env
```

## 📦 패키지 설치

### 방법 1: pip 사용 (현재 설정에 맞음)

```bash
# 필수 패키지 설치
.venv/bin/pip3 install pandas
.venv/bin/pip3 install langchain-community
.venv/bin/pip3 install langchain-chroma
.venv/bin/pip3 install chromadb
```

### 방법 2: uv 사용 (선택사항)

```bash
# uv 프로젝트 초기화 후
uv add langchain-community
uv add langchain-chroma  
uv add chromadb
uv add pandas
```

## 📄 데이터 준비

### CSV 파일 인코딩 변환

```bash
# 인코딩 변환 스크립트 실행 (cp949 → UTF-8) - 어디서든 실행 가능
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/fix_encoding.py
```

**예상 출력:**
```
📄 CSV 파일 읽기 중 (cp949 인코딩)...
📊 총 202 개 행 읽기 완료
✅ UTF-8 파일 생성 완료!
🔍 '트레이딩' 관련 용어 검색:
📌 관련 용어 10개 발견:
  - 트레이딩포지션: 단기 매매차익 획득 등을 목적으로...
```

## 🗄️ 벡터 데이터베이스 구축

### 1. 데이터베이스 생성

```bash
# 벡터 데이터베이스 구축 스크립트 실행 - 어디서든 실행 가능
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/build_vector_db.py
```

**예상 출력:**
```
📄 로드된 문서 수: 202
🤖 Gemini 임베딩 모델 초기화 중...
🔍 벡터 데이터베이스 생성 중... (시간이 소요될 수 있습니다)
✅ 벡터 데이터베이스가 성공적으로 생성되었습니다!
📊 총 202개 문서가 임베딩되어 './database' 폴더에 저장되었습니다.
🎉 작업 완료!
```

### 2. 생성된 파일 확인

```bash
# 생성된 파일 확인
ls -la database/
ls -la *.csv
```

**예상 파일:**
- `database/` 폴더: Chroma 벡터 데이터베이스
- `한국산업은행_금융용어_utf8.csv`: UTF-8 변환된 CSV

## 🚀 RAG 시스템 실행

### 방법 1: 기본 RAG 시스템

```bash
# 기본 RAG 시스템 실행 - 어디서든 실행 가능
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/retrieve.py
```

### 방법 2: 하이브리드 RAG 시스템

```bash
# 키워드+벡터 하이브리드 검색 RAG 실행 - 어디서든 실행 가능
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/retrieve_hybrid.py
```

### 방법 3: 스마트 RAG 시스템 (권장)

```bash
# 최적화된 스마트 RAG 시스템 실행 - 어디서든 실행 가능
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/retrieve_final.py
```

## 🧪 테스트 방법

### 자동 테스트

스크립트를 실행하면 자동으로 다음 테스트가 진행됩니다:

1. **질문 1**: "짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?"
   - **예상 답변**: "트레이딩포지션입니다."

2. **질문 2**: "트레이딩 포지션이 뭐야?"
   - **예상 답변**: "단기 매매차익 획득 등을 목적으로 금융기관이 보유하는 포지션입니다."

### 수동 테스트

코드를 수정하여 다른 질문도 테스트할 수 있습니다:

```python
# retrieve_final.py 파일의 마지막 부분에 추가
print("💬 질문 3: 신용리스크가 뭐야?")
answer3 = chain.invoke("신용리스크가 뭐야?")
print(f"🤖 답변 3: {answer3}")
```

## 📊 시스템 구조

```
231.rag-chatbot/
├── 00.setting.md                           # 패키지 설치 가이드
├── README.md                               # 이 파일
├── 한국산업은행_금융 관련 용어_20151231.csv    # 원본 CSV (cp949)
├── 한국산업은행_금융용어_utf8.csv              # 변환된 CSV (UTF-8)
├── fix_encoding.py                         # 인코딩 변환 스크립트
├── build_vector_db.py                      # 벡터 DB 구축 스크립트
├── retrieve.py                             # 기본 RAG 시스템
├── retrieve_hybrid.py                      # 하이브리드 검색 RAG 시스템
├── retrieve_final.py                       # 스마트 RAG 시스템 (권장)
└── database/                               # 벡터 데이터베이스 저장소
    ├── chroma.sqlite3                      # ChromaDB 데이터베이스
    └── 2da4cdac-5d82-475c-8c19-1e26babdce96/ # 벡터 임베딩 저장소
```

## 🔍 실행 결과 예시

### 성공적인 실행 결과

```
🎯 스마트 RAG 시스템 테스트 시작!

============================================================
💬 질문 1: 짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?
🔍 스마트 검색: '짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?'
  📊 전체 문서: 202개
  🔑 키워드 검색: 5개
  📈 벡터 검색: 10개
  ✅ 최종 결과: 5개
🔍 검색된 문서 개수: 5
📄 문서 1: 단기금융시장
📄 문서 2: 트레이딩포지션
📄 문서 3: 여신유의업종 지정
📄 문서 4: 금리변경리스크
📄 문서 5: 펀드(주식형/채권형/혼합형/MMF)

📄 참조 문서 시작==>[
구분: 리스크
분류: 시장리스크
용어: 트레이딩포지션
설명: 단기 매매차익 획득 등을 목적으로 금융기관이 보유하는 포지션으로 상품채권  상품주식 및 파생상품 등을 말함
]<==참조 문서 끝

🤖 답변 1: 트레이딩포지션입니다.
```

## ❗ 문제 해결

### 1. API 키 오류

```
ValueError: GOOGLE_API_KEY not found. Please check .env file
```

**해결방법:**
- `.env` 파일에 올바른 API 키가 있는지 확인
- API 키에 따옴표 없이 입력되었는지 확인

### 2. 파일 경로 오류

```
FileNotFoundError: [Errno 2] No such file or directory
```

**해결방법:**
```bash
# 올바른 디렉토리에서 실행
cd 231.rag-chatbot
```

### 3. 패키지 설치 오류

```
ModuleNotFoundError: No module named 'langchain_chroma'
```

**해결방법:**
```bash
# 필요한 패키지 재설치
.venv/bin/pip3 install langchain-chroma chromadb
```

### 4. 검색 결과 0개

```
🔍 검색된 문서 개수: 0
```

**해결방법:**
```bash
# 벡터 데이터베이스 재구축
rm -rf database/
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python build_vector_db.py
```

### 5. API 할당량 초과

```
429 You exceeded your current quota
```

**해결방법:**
- Gemini API 결제 또는 일일 할당량 대기
- API 키 확인 및 결제 상태 점검

## 🎯 추천 테스트 플로우

1. **환경 확인**: `.env` 파일과 API 키 설정
2. **데이터 변환**: `fix_encoding.py` 실행
3. **DB 구축**: `build_vector_db.py` 실행  
4. **RAG 테스트**: `retrieve_final.py` 실행 (권장)
5. **커스텀 테스트**: 코드 수정하여 다른 질문 테스트

## 📚 참고 자료

- [Gemini API 문서](https://ai.google.dev/gemini-api/docs)
- [LangChain 문서](https://python.langchain.com/docs/get_started/introduction)
- [Chroma 벡터 데이터베이스](https://docs.trychroma.com/)
- [자세히 쓰는 Gemini API](https://wikidocs.net/262594)

---

🎉 **모든 설정이 완료되면 완전한 RAG 시스템으로 금융 용어 질의응답을 테스트할 수 있습니다!**

## 📈 RAG 시스템 버전별 특징

### 1. retrieve.py - 기본 RAG 시스템
- 벡터 유사도 검색만 사용
- 단순한 구조로 이해하기 쉬움
- 빠른 응답 속도

### 2. retrieve_hybrid.py - 하이브리드 RAG 시스템  
- 키워드 검색 + 벡터 검색 결합
- 더 정확한 검색 결과
- 중간 수준의 복잡도

### 3. retrieve_final.py - 스마트 RAG 시스템 (권장)
- 키워드 검색과 벡터 검색의 최적 결합
- 중복 제거 및 결과 최적화
- 가장 높은 검색 정확도
- 상세한 검색 과정 표시

## 🚀 빠른 실행 순서 (절대 경로 버전)

```bash
# 1. 환경 설정 (.env 파일 생성)
cd /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 2. 데이터 변환 (어디서든 실행 가능)
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/fix_encoding.py

# 3. 벡터 DB 구축 (어디서든 실행 가능)
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/build_vector_db.py

# 4. RAG 시스템 실행 (어디서든 실행 가능) - 권장: retrieve_final.py
/Users/devpeng/Documents/GitHub/Kosta-chatbot/.venv/bin/python /Users/devpeng/Documents/GitHub/Kosta-chatbot/231.rag-chatbot/retrieve_final.py
```

**✅ 모든 스크립트가 절대 경로로 수정되어 어느 디렉토리에서든 실행 가능합니다!**

