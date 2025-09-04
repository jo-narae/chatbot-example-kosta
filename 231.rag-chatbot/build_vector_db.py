# build_vector_db.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 환경변수 로드
load_dotenv()

# 환경변수 확인
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check .env file")

# CSV 파일 로드 (UTF-8 변환된 파일 사용)
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "한국산업은행_금융용어_utf8.csv")

loader = CSVLoader(
    file_path=csv_path, 
    encoding="utf-8"
)
pages = loader.load()
print(f"📄 로드된 문서 수: {len(pages)}")
print("📋 첫 번째 문서 샘플:")
print(pages[0] if pages else "문서가 없습니다.")
print("\n" + "="*50 + "\n")

# Gemini 임베딩 모델 설정
print("🤖 Gemini 임베딩 모델 초기화 중...")
gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # gemini-embedding-001 모델
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

# 벡터 데이터베이스 생성
print("🔍 벡터 데이터베이스 생성 중... (시간이 소요될 수 있습니다)")
database_path = os.path.join(current_dir, "database")
try:
    vector_db = Chroma.from_documents(
        documents=pages, 
        embedding=gemini_embeddings, 
        persist_directory=database_path
    )
    print("✅ 벡터 데이터베이스가 성공적으로 생성되었습니다!")
    print(f"📊 총 {len(pages)}개 문서가 임베딩되어 './database' 폴더에 저장되었습니다.")
    
except Exception as e:
    print(f"❌ 벡터 데이터베이스 생성 실패: {str(e)}")
    raise

# 생성된 벡터 데이터베이스 간단 테스트
print("\n🧪 벡터 데이터베이스 테스트 중...")
try:
    # 유사도 검색 테스트
    test_query = "금융"
    similar_docs = vector_db.similarity_search(test_query, k=3)
    print(f"'{test_query}' 검색 결과 ({len(similar_docs)}개):")
    for i, doc in enumerate(similar_docs, 1):
        print(f"  {i}. {doc.page_content[:100]}...")
        
except Exception as e:
    print(f"⚠️ 테스트 검색 실패: {str(e)}")

print("\n🎉 작업 완료!")