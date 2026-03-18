"""
출력 파서 - AIMessage를 원하는 형태로 변환

01에서 결과가 AIMessage 객체라 .content로 꺼내야 했습니다.
파서를 체인 끝에 붙이면 원하는 형태로 자동 변환됩니다.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# 환경변수 로드
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
prompt = ChatPromptTemplate.from_template("{food}의 칼로리를 한 줄로 알려줘.")

# ══════════════════════════════════════════════════
# 비교 1: 파서 없음 → AIMessage 객체
# ══════════════════════════════════════════════════
print("=" * 50)
print("파서 없음: prompt | llm")
print("=" * 50)

chain_no_parser = prompt | llm
result = chain_no_parser.invoke({"food": "김치찌개"})
print(f"결과: {result}")
print(f"타입: {type(result)}")
print(f"텍스트 꺼내기: {result.content}")

# ══════════════════════════════════════════════════
# 비교 2: StrOutputParser → 바로 문자열
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("StrOutputParser: prompt | llm | StrOutputParser()")
print("=" * 50)

chain_str = prompt | llm | StrOutputParser()
result = chain_str.invoke({"food": "김치찌개"})
print(f"결과: {result}")
print(f"타입: {type(result)}")
print("→ 바로 문자열! .content 안 꺼내도 됩니다")

# ══════════════════════════════════════════════════
# 비교 3: JsonOutputParser → 바로 dict
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("JsonOutputParser: JSON으로 구조화")
print("=" * 50)

chain_json = (
    ChatPromptTemplate.from_template(
        "다음 음식의 정보를 JSON으로 답해줘. "
        "키는 name, calories, category로 해줘.\n\n"
        "음식: {food}"
    )
    | llm
    | JsonOutputParser()
)

result = chain_json.invoke({"food": "김치찌개"})
print(f"결과: {result}")
print(f"타입: {type(result)}")

# dict이니까 코드에서 바로 활용 가능!
print(f"  이름: {result.get('name')}")
print(f"  칼로리: {result.get('calories')}")
print(f"  카테고리: {result.get('category')}")

# ══════════════════════════════════════════════════
# batch() - 여러 개 한번에 처리
# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("batch() - 여러 개 한번에 처리")
print("=" * 50)

foods = [{"food": "비빔밥"}, {"food": "떡볶이"}, {"food": "삼겹살"}]
results = chain_json.batch(foods)

for r in results:
    print(f"  {r.get('name', '?'):>6} | {str(r.get('calories', '?')):>10} | {r.get('category', '?')}")

# ══════════════════════════════════════════════════
print()
print("=" * 50)
print("핵심 정리")
print("=" * 50)
print()
print("prompt | llm                        → AIMessage (객체)")
print("prompt | llm | StrOutputParser()     → str (문자열)")
print("prompt | llm | JsonOutputParser()    → dict (딕셔너리)")
print()
print("체인 실행 방법:")
print("  .invoke()  → 1개 처리")
print("  .batch()   → 여러 개 한번에")
print("  .stream()  → 실시간 스트리밍 (뒤에서 배움)")
