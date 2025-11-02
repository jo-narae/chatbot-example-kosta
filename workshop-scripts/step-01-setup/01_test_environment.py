"""
Step 1-1: 환경 설정 확인

Python 버전, 필요한 패키지 설치 여부를 확인합니다.
"""

import sys
import platform

print("=" * 60)
print("환경 설정 확인")
print("=" * 60)
print()

# Python 버전 확인
print("1. Python 버전")
print(f"   - 버전: {sys.version}")
print(f"   - 실행 경로: {sys.executable}")
print()

# 운영체제 정보
print("2. 운영체제")
print(f"   - 시스템: {platform.system()}")
print(f"   - 버전: {platform.version()}")
print(f"   - 아키텍처: {platform.machine()}")
print()

# 필수 패키지 확인
print("3. 필수 패키지 설치 확인")
required_packages = [
    "dotenv",
    "google.generativeai",
    "streamlit",
    "langchain",
    "langchain_google_genai",
]

missing_packages = []

for package in required_packages:
    package_name = package.replace(".", "_")  # dotenv 처리
    try:
        if package == "dotenv":
            import dotenv
            print(f"   ✅ {package}: {dotenv.__version__}")
        elif package == "google.generativeai":
            import google.generativeai as genai
            print(f"   ✅ {package}: 설치됨")
        elif package == "streamlit":
            import streamlit as st
            print(f"   ✅ {package}: {st.__version__}")
        elif package == "langchain":
            import langchain
            print(f"   ✅ {package}: {langchain.__version__}")
        elif package == "langchain_google_genai":
            import langchain_google_genai
            print(f"   ✅ {package}: 설치됨")
    except ImportError:
        print(f"   ❌ {package}: 설치되지 않음")
        missing_packages.append(package)

print()

# 결과 요약
if missing_packages:
    print("⚠️ 누락된 패키지가 있습니다:")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    print()
    print("다음 명령어로 설치하세요:")
    print("   uv sync")
    print("   또는")
    print("   pip install -r requirements.txt")
else:
    print("✅ 모든 필수 패키지가 설치되어 있습니다!")
    print()
    print("다음 단계:")
    print("   python 02_test_gemini_api.py")

print()
print("=" * 60)
