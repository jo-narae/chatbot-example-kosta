# 표준 라이브러리 -------------------------------------------------------------
import os  # 운영체제 환경변수 읽기/쓰기 등 시스템 관련 기능

# 외부 라이브러리 -------------------------------------------------------------
# python-dotenv: 프로젝트 루트의 .env 파일을 읽어 환경변수로 로드해줌
from dotenv import load_dotenv

# google-genai (신 SDK): Gemini API를 Python에서 사용하기 위한 클라이언트
from google import genai
# 타입 힌트 및 구성 객체(요청 설정)를 제공하는 서브모듈
from google.genai import types

# 1) .env 파일 로드 -----------------------------------------------------------
# - 기본적으로 현재 작업 디렉토리(프로젝트 루트)의 .env 파일을 찾습니다.
# - .env가 없거나 일부 키만 있어도 오류는 아니며, 이후 os.getenv() 결과가 None일 수 있습니다.
load_dotenv()

# 2) 환경변수에서 API 키 읽기 -------------------------------------------------
# - GOOGLE_API_KEY 라는 이름으로 .env 또는 셸 환경에 저장된 값을 읽습니다.
# - 보안상 API 키는 코드에 하드코딩하지 않고 환경변수로 주입하는 것이 원칙입니다.
api_key = os.getenv("GOOGLE_API_KEY")

# - 필수값 검증: 키가 없으면 명확한 예외를 발생시켜 빠르게 문제를 발견하도록 합니다.
if not api_key:
    raise ValueError(
        "환경변수 GOOGLE_API_KEY 가 설정되지 않았습니다. "
        "프로젝트 루트의 .env 파일(또는 셸 환경)에 GOOGLE_API_KEY=... 를 추가하세요."
    )

# 3) 클라이언트 초기화 --------------------------------------------------------
# - genai.Client 는 Google AI Studio용 클라이언트입니다.
# - Vertex AI(구글 클라우드) 경로를 쓰려면 별도 파라미터(vertexai, project, location)를 사용합니다.
client = genai.Client()

# 4) 모델 호출 준비/실행 ------------------------------------------------------
# - model: 사용할 Gemini 모델 ID. (예: "gemini-2.0-flash", "gemini-2.5-flash" 등)
# - contents:
#     * 간단히 문자열을 넘기면 user 메시지 1개로 취급됩니다.
#     * 복잡한 대화/멀티모달은 types.Content/parts 구조를 사용합니다.

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="AI에 대해 1줄로 설명해줘",
)

# 5) 응답 출력 ---------------------------------------------------------------
# - response.text 는 가장 대표 후보(candidates[0])의 텍스트 본문을 편의상 꺼내주는 속성입니다.
# - 고급 제어가 필요하면 response.candidates[*].content.parts 를 직접 순회하세요.
print(response.text)