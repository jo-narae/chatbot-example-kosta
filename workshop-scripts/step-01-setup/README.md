# Step 1: 환경 설정 및 확인

워크샵을 시작하기 전에 개발 환경이 올바르게 설정되었는지 확인합니다.

## 📋 학습 목표

- Python 환경 확인
- 필수 패키지 설치 검증
- Gemini API 키 테스트
- 개발 환경 준비 완료

## 🚀 실행 방법

### 1. 환경 확인
```bash
uv run python 01_test_environment.py
```

**확인 사항:**
- Python 버전 (3.10 이상)
- 운영체제 정보
- 필수 패키지 설치 여부

### 2. Gemini API 테스트
```bash
uv run python 02_test_gemini_api.py
```

**확인 사항:**
- `.env` 파일에 API 키 설정
- Gemini API 연결 테스트
- 간단한 질문-응답 동작 확인

## 📝 사전 준비

### 1. `.env` 파일 생성

프로젝트 루트 폴더에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 2. Gemini API 키 발급

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. 생성된 키를 복사하여 `.env` 파일에 붙여넣기

### 3. 패키지 설치

```bash
# 프로젝트 루트로 이동
cd ../../..

# uv 사용
uv sync

# 또는 pip 사용
pip install -r requirements.txt
```

## ✅ 성공 기준

두 스크립트가 모두 성공적으로 실행되면:
- ✅ 환경 설정 완료
- ✅ API 연결 확인
- ✅ 다음 단계 진행 가능

## 🔍 문제 해결

### Python 버전이 낮은 경우
```bash
python --version  # 3.10 미만인 경우
```
→ Python 3.10 이상을 설치하세요

### 패키지 설치 오류
```bash
# 가상환경 재생성
uv venv
uv sync
```

### API 키 오류
- `.env` 파일이 프로젝트 루트에 있는지 확인
- API 키에 따옴표가 없는지 확인
- 키에 불필요한 공백이 없는지 확인

## 📌 다음 단계

환경 설정이 완료되었다면:
```bash
cd ../step-02-basic-chatbot
uv run python 01_single_turn.py
```
