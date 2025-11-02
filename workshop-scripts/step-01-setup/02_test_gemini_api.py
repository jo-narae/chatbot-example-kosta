"""
Step 1-2: Gemini API 키 테스트

환경변수에서 API 키를 로드하고 Gemini API 연결을 테스트합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

print("=" * 60)
print("Gemini API 키 테스트")
print("=" * 60)
print()

# 1. 환경변수 확인
print("1. 환경변수 확인")
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("   ❌ GOOGLE_API_KEY를 찾을 수 없습니다.")
    print()
    print("해결 방법:")
    print(f"   1. 프로젝트 루트에 .env 파일 생성: {project_root}")
    print("   2. 다음 내용 추가:")
    print("      GOOGLE_API_KEY=your_api_key_here")
    print()
    print("API 키 발급:")
    print("   https://aistudio.google.com/app/apikey")
    sys.exit(1)

print(f"   ✅ API 키 확인: {api_key[:10]}...{api_key[-4:]}")
print()

# 2. Gemini API 연결 테스트
print("2. Gemini API 연결 테스트")

try:
    import google.generativeai as genai

    # API 설정
    genai.configure(api_key=api_key)

    # 모델 초기화
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    print("   ✅ Gemini API 초기화 성공")
    print()

    # 3. 간단한 테스트 질문
    print("3. 테스트 질문 실행")
    print("   질문: '안녕하세요'라고 짧게 인사해주세요")
    print()

    response = model.generate_content("'안녕하세요'라고 짧게 인사해주세요")

    print("   🤖 Gemini 응답:")
    print(f"   {response.text}")
    print()

    print("=" * 60)
    print("✅ Gemini API 테스트 성공!")
    print()
    print("다음 단계:")
    print("   cd ../step-02-basic-chatbot")
    print("   uv run python 01_single_turn.py")
    print("=" * 60)

except Exception as e:
    print(f"   ❌ API 연결 실패: {str(e)}")
    print()
    print("문제 해결:")
    print("   1. API 키가 올바른지 확인")
    print("   2. 인터넷 연결 확인")
    print("   3. google-generativeai 패키지 설치 확인:")
    print("      uv add google-generativeai")
    sys.exit(1)
