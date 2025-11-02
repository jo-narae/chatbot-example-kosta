"""
Step 3-1: Zero-shot 프롬프팅

예시 없이 작업 설명만으로 LLM이 작업을 수행하도록 하는 기법입니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# 환경 설정
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / ".env")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

genai.configure(api_key=api_key)

print("=" * 60)
print("Zero-shot 프롬프팅")
print("=" * 60)
print()
print("예시 없이 작업 설명만으로 수행")
print()

# 모델 초기화
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Zero-shot 예제: 감정 분석
print("🎯 예제: 감정 분석")
print("-" * 60)

prompt = """
다음 문장의 감정을 분석하여 긍정, 부정, 중립 중 하나로 분류하세요.

문장: "이 제품은 정말 마음에 들어요! 추천합니다."

분류:
"""

response = model.generate_content(prompt)
print(f"프롬프트:\n{prompt}")
print(f"\n🤖 AI 응답:\n{response.text}")
print()

# Zero-shot 예제: 언어 번역
print("🎯 예제: 언어 번역")
print("-" * 60)

prompt = """
다음 영어 문장을 한국어로 번역하세요.

English: "The weather is beautiful today."

Korean:
"""

response = model.generate_content(prompt)
print(f"프롬프트:\n{prompt}")
print(f"\n🤖 AI 응답:\n{response.text}")
print()

# Zero-shot 예제: 요약
print("🎯 예제: 텍스트 요약")
print("-" * 60)

prompt = """
다음 글을 한 문장으로 요약하세요.

글: 인공지능 기술은 최근 몇 년간 급속도로 발전했습니다. 특히 대규모 언어 모델의 등장으로 자연어 처리 능력이 크게 향상되었으며, 이는 다양한 산업 분야에 혁신을 가져오고 있습니다.

요약:
"""

response = model.generate_content(prompt)
print(f"프롬프트:\n{prompt}")
print(f"\n🤖 AI 응답:\n{response.text}")
print()

print("=" * 60)
print("💡 Zero-shot의 특징:")
print("  ✅ 예시 불필요 - 작업 설명만으로 충분")
print("  ✅ 빠른 적용 - 즉시 사용 가능")
print("  ❌ 정확도 한계 - 복잡한 작업에는 부족할 수 있음")
print()
print("다음 단계: uv run python 02_one_shot.py")
print("=" * 60)
