# retrieve.py
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 환경변수 로드
load_dotenv()

# 환경변수 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

print("🤖 Gemini 임베딩 모델 초기화 중...")
# Gemini 임베딩 모델 설정 (build_vector_db.py와 동일)
gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # gemini-embedding-001 모델
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

print("📚 벡터 스토어 연결 중...")
# 기존에 생성된 벡터 데이터베이스 로드 (절대 경로 사용)
current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, "database")
vector_store = Chroma(
    persist_directory=database_path, 
    embedding_function=gemini_embeddings
)

print("🔍 검색기 설정 중...")
# 유사도 검색기 설정 (MMR 대신 similarity로 변경)
retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 5}
)

# 프롬프트 템플릿 정의
template = """
[context]: {context}
---
[질의]: {query}
---
[예시]
신용 환산율입니다.
---
위의 [context] 정보 내에서 [질의]에 대해 답변 [예시]와 같이 술어를 붙여서 답하세요.
"""
prompt = ChatPromptTemplate.from_template(template)

print("🧠 Gemini LLM 모델 초기화 중...")
# Gemini LLM 모델 설정
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0,
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

def merge_pages(pages):
    """검색된 문서들을 하나의 컨텍스트로 합치는 함수"""
    print(f"🔍 검색된 문서 개수: {len(pages)}")
    
    if not pages:
        print("⚠️ 검색된 문서가 없습니다!")
        return "관련 문서를 찾을 수 없습니다."
    
    # 각 문서 내용 출력
    for i, page in enumerate(pages, 1):
        print(f"📄 문서 {i}: {page.page_content[:100]}...")
    
    merged = "\n\n".join(page.page_content for page in pages)
    print(f"\n📄 참조 문서 시작==>[\n{merged}\n]<==참조 문서 끝\n")
    return merged

print("⛓️ RAG 체인 구성 중...")
# RAG 체인 구성
chain = (
    {"query": RunnablePassthrough(), "context": retriever | merge_pages}
    | prompt
    | llm
    | StrOutputParser()
)

print("🎯 RAG 시스템 테스트 시작!\n")
print("="*60)

# 테스트 1
print("💬 질문 1: 짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?")
answer1 = chain.invoke(
    "짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?"
)
print(f"🤖 답변 1: {answer1}\n")
print("="*60)

# 테스트 2  
print("💬 질문 2: 트레이딩 포지션이 뭐야?")
answer2 = chain.invoke("트레이딩 포지션이 뭐야?")
print(f"🤖 답변 2: {answer2}")

print("\n🎉 RAG 시스템 테스트 완료!")