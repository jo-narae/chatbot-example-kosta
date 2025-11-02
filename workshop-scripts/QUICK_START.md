# 워크샵 빠른 시작 가이드

## 🎯 5분 안에 시작하기

### 1. 환경 확인
```bash
cd workshop-scripts/step-01-setup
uv run python 01_test_environment.py
uv run python 02_test_gemini_api.py
```

### 2. 첫 챗봇 실행
```bash
cd ../step-02-basic-chatbot
uv run python 01_single_turn.py
```

대화 입력 후 `exit`로 종료

### 3. 대화 기록 유지 챗봇
```bash
uv run python 02_multi_turn.py
```

이전 대화를 기억하는 것을 확인

## 📚 전체 워크샵 진행 순서

### Phase 1: 기초 (1시간)
```bash
cd step-01-setup
uv run python 01_test_environment.py
uv run python 02_test_gemini_api.py

cd ../step-02-basic-chatbot
uv run python 01_single_turn.py
uv run python 02_multi_turn.py

cd ../step-03-prompt-engineering
uv run python 01_zero_shot.py
uv run python 02_one_shot.py
uv run python 03_few_shot.py
```

### Phase 2: 웹 UI (30분)
```bash
cd ../step-04-web-ui
uv run streamlit run 01_streamlit_chatbot.py
```

### Phase 3: LangChain (1시간)
```bash
cd ../step-05-langchain-basic
uv run python 01_langchain_intro.py
uv run python 02_message_history.py
uv run python 03_langsmith_tracing.py

cd ../step-06-langchain-advanced
uv run python 01_lcel_chain.py
uv run python 02_custom_tools.py
uv run python 03_streaming_output.py
```

### Phase 4: RAG 시스템 (1시간)
```bash
cd ../step-07-rag-system
uv run python 01_prepare_data.py
uv run python 02_build_vectordb.py
uv run python 03_rag_chatbot.py
```

## 💡 각 단계별 주요 학습 내용

| 단계 | 폴더 | 학습 내용 | 시간 |
|------|------|-----------|------|
| 1 | step-01-setup | 환경 설정 확인 | 10분 |
| 2 | step-02-basic-chatbot | Single/Multi-turn 대화 | 20분 |
| 3 | step-03-prompt-engineering | Zero/One/Few-shot | 30분 |
| 4 | step-04-web-ui | Streamlit UI | 30분 |
| 5 | step-05-langchain-basic | LangChain 기본 | 30분 |
| 6 | step-06-langchain-advanced | LCEL, Tool, Streaming | 30분 |
| 7 | step-07-rag-system | RAG 구축 | 40분 |

## 🔑 사전 준비

### 1. API 키 설정
프로젝트 루트에 `.env` 파일:
```
GOOGLE_API_KEY=your_api_key_here
```

### 2. 패키지 설치
```bash
cd ../../..  # 프로젝트 루트로
uv sync
```

## ❓ 자주 묻는 질문

**Q: 어떤 파일부터 시작하나요?**
A: `step-01-setup/01_test_environment.py`부터 순서대로 진행하세요.

**Q: 에러가 발생하면?**
A: 각 폴더의 `README.md`에 문제 해결 방법이 있습니다.

**Q: 시간이 부족하면?**
A: Step 1, 2, 5만 집중하세요 (핵심 개념)

**Q: 기존 폴더(211.single-turn 등)와의 차이는?**
A: workshop-scripts는 교육용으로 재구성된 버전입니다. 더 깔끔하고 설명이 자세합니다.

## 🎓 학습 팁

1. **순서대로 진행**: 각 단계가 이전 내용을 기반으로 합니다
2. **코드 수정 실험**: 직접 값을 바꿔보며 학습하세요
3. **README 정독**: 각 폴더의 README에 핵심 개념이 있습니다
4. **에러 두려워하지 않기**: 에러 메시지를 읽고 해결하는 것도 학습입니다

## 📞 도움말

- 각 단계별 상세 가이드: 각 폴더의 `README.md`
- 전체 프로젝트 문서: `../README.md`
- 실행 가이드: `../EXECUTION_GUIDE.md`

---

**시작하세요! 🚀**

```bash
cd step-01-setup
uv run python 01_test_environment.py
```
