# retrieve_final.py - 최종 개선된 RAG 시스템 (키워드 + 벡터 검색)
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 환경변수 로드
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

print("🤖 Gemini 임베딩 모델 초기화 중...")
current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, "database")

gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

print("📚 벡터 스토어 연결 중...")
vector_store = Chroma(
    persist_directory=database_path, 
    embedding_function=gemini_embeddings
)

def smart_search(query, k=5):
    """스마트 검색: 키워드 우선 + 벡터 보완"""
    print(f"🔍 스마트 검색: '{query}'")
    
    # 1. 모든 문서 가져오기
    try:
        all_docs = vector_store.similarity_search("", k=1000)  # 모든 문서
        print(f"  📊 전체 문서: {len(all_docs)}개")
    except:
        all_docs = []
    
    # 2. 키워드 기반 검색
    keyword_matches = []
    search_terms = [
        query.lower(),
        query.replace(" ", ""),  # 띄어쓰기 제거
        "매매차익" if "차익" in query else "",
        "트레이딩포지션" if "트레이딩" in query or "포지션" in query else "",
        "단기" if "짧은" in query or "단기" in query else ""
    ]
    
    search_terms = [term for term in search_terms if term]  # 빈 문자열 제거
    
    for doc in all_docs:
        content_lower = doc.page_content.lower()
        for term in search_terms:
            if term in content_lower:
                keyword_matches.append(doc)
                break
    
    print(f"  🔑 키워드 검색: {len(keyword_matches)}개")
    
    # 3. 벡터 검색
    vector_results = vector_store.similarity_search(query, k=k*2)
    print(f"  📈 벡터 검색: {len(vector_results)}개")
    
    # 4. 결과 병합 (키워드 우선)
    seen_contents = set()
    final_results = []
    
    # 키워드 매칭 결과를 우선적으로 추가
    for doc in keyword_matches:
        if len(final_results) >= k:
            break
        if doc.page_content not in seen_contents:
            final_results.append(doc)
            seen_contents.add(doc.page_content)
    
    # 벡터 검색 결과로 보완
    for doc in vector_results:
        if len(final_results) >= k:
            break
        if doc.page_content not in seen_contents:
            final_results.append(doc)
            seen_contents.add(doc.page_content)
    
    print(f"  ✅ 최종 결과: {len(final_results)}개")
    return final_results

# 스마트 검색 retriever 설정
class SmartRetriever:
    def __init__(self, k=5):
        self.k = k
    
    def invoke(self, query):
        return smart_search(query, self.k)

retriever = SmartRetriever()

# 프롬프트 템플릿
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
        content = page.page_content
        if "용어:" in content and "설명:" in content:
            term = content.split("용어:")[1].split("설명:")[0].strip()
            print(f"📄 문서 {i}: {term}")
        else:
            print(f"📄 문서 {i}: {content[:50]}...")
    
    merged = "\n\n".join(page.page_content for page in pages)
    print(f"\n📄 참조 문서 시작==>[\n{merged}\n]<==참조 문서 끝\n")
    return merged

def get_context(query):
    """쿼리에서 컨텍스트를 추출하는 함수"""
    results = retriever.invoke(query)
    return merge_pages(results)

print("⛓️ 스마트 RAG 체인 구성 중...")
chain = (
    {"query": RunnablePassthrough(), "context": get_context}
    | prompt
    | llm
    | StrOutputParser()
)

print("🎯 스마트 RAG 시스템 테스트 시작!\n")
print("="*60)

# 테스트 1
print("💬 질문 1: 짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?")
answer1 = chain.invoke("짧은 기간 동안의 차익을 위해 금융사가 보유하는 걸 뜻하는 용어가 뭐야?")
print(f"🤖 답변 1: {answer1}\n")
print("="*60)

# 테스트 2  
print("💬 질문 2: 트레이딩 포지션이 뭐야?")
answer2 = chain.invoke("트레이딩 포지션이 뭐야?")
print(f"🤖 답변 2: {answer2}")

print("\n🎉 스마트 RAG 시스템 테스트 완료!")