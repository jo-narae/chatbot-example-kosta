# Step 2: 기본 챗봇 구현

Gemini API를 사용하여 단일 턴과 멀티 턴 대화를 구현합니다.

## 📋 학습 목표

- Gemini API 기본 사용법 이해
- 단일 턴 vs 멀티 턴 대화의 차이점 파악
- 대화 히스토리 관리 방법 학습
- System Instruction으로 챗봇 페르소나 설정

## 📁 파일 구성

- `01_single_turn.py` - 단일 턴 대화 (독립적인 질문-응답)
- `02_multi_turn.py` - 멀티 턴 대화 (히스토리 유지)

## 🚀 실행 방법

### 1. 단일 턴 대화
```bash
uv run python 01_single_turn.py
```

**특징:**
- 각 질문은 독립적으로 처리
- 이전 대화를 기억하지 못함
- 간단한 질의응답에 적합

**예시 대화:**
```
사용자: 파이썬이 뭐야?
AI: 파이썬은 프로그래밍 언어입니다...

사용자: 그게 어떤 특징이 있어?  # ❌ "그게"가 무엇인지 모름
AI: 무엇에 대한 특징을 알고 싶으신가요?
```

### 2. 멀티 턴 대화
```bash
uv run python 02_multi_turn.py
```

**특징:**
- 대화 히스토리 유지
- 이전 맥락을 이해하고 답변
- 자연스러운 대화 가능

**예시 대화:**
```
사용자: 파이썬이 뭐야?
AI: 파이썬은 프로그래밍 언어입니다...

사용자: 그게 어떤 특징이 있어?  # ✅ "그게"가 파이썬을 의미함을 이해
AI: 파이썬의 주요 특징은...
```

**추가 명령어:**
- `reset`: 대화 히스토리 초기화
- `history`: 현재 대화 히스토리 확인
- `exit`: 프로그램 종료

## 💡 핵심 개념

### Single-turn vs Multi-turn

| 구분 | Single-turn | Multi-turn |
|------|-------------|------------|
| 대화 기억 | ❌ 없음 | ✅ 있음 |
| 맥락 이해 | ❌ 불가능 | ✅ 가능 |
| 구현 | `model.generate_content()` | `chat.send_message()` |
| 사용 예 | FAQ, 단순 질의응답 | 대화형 챗봇, 상담 |

### System Instruction

챗봇의 페르소나와 행동을 정의합니다:

```python
system_instruction = "너는 친절한 AI 어시스턴트입니다."

model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction=system_instruction
)
```

### Temperature 설정

응답의 창의성과 랜덤성을 조절합니다:

- `0.0`: 가장 결정론적 (항상 비슷한 답변)
- `0.7`: 균형잡힌 설정 (권장)
- `1.0`: 가장 창의적 (다양한 답변)

```python
generation_config={
    "temperature": 0.7,
    "max_output_tokens": 1000,
}
```

## 🎯 실습 과제

### 과제 1: Temperature 실험
`01_single_turn.py`의 temperature 값을 0.0, 0.5, 1.0으로 바꿔가며 같은 질문에 대한 답변 차이를 관찰하세요.

### 과제 2: 페르소나 변경
System Instruction을 변경하여 다른 성격의 챗봇을 만들어보세요:
- 예: "너는 친절한 여행 가이드야"
- 예: "너는 전문적인 프로그래밍 튜터야"

### 과제 3: 대화 흐름 관찰
`02_multi_turn.py`에서 다음 시나리오를 테스트하세요:
1. 여러 단계의 연속 질문
2. `reset` 후 같은 질문 (맥락이 사라짐 확인)
3. `history`로 대화 히스토리 확인

## 📝 주요 코드 패턴

### 단일 턴
```python
model = genai.GenerativeModel("gemini-2.0-flash-exp")
response = model.generate_content(user_input)
print(response.text)
```

### 멀티 턴
```python
chat = model.start_chat(history=[])
response = chat.send_message(user_input)
print(response.text)

# 히스토리 확인
print(len(chat.history))  # 메시지 수
```

## 🔍 문제 해결

### API 키 오류
```
ValueError: GOOGLE_API_KEY not found
```
→ 프로젝트 루트의 `.env` 파일 확인

### 응답이 너무 길거나 짧은 경우
`max_output_tokens` 값을 조절하세요:
```python
generation_config={"max_output_tokens": 500}  # 더 짧게
generation_config={"max_output_tokens": 2000}  # 더 길게
```

## 📌 다음 단계

프롬프트 엔지니어링 기법 학습:
```bash
cd ../step-03-prompt-engineering
uv run python 01_zero_shot.py
```
