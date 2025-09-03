import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLangChainSingleton:
    """Gemini LangChain 모델을 위한 싱글턴 클래스"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiLangChainSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """모델 초기화"""
        # 환경설정
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")
        
        genai.configure(api_key=api_key)
        
        # LangChain Gemini 모델 초기화
        self._model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        print("✅ Gemini LangChain 모델이 초기화되었습니다.")
    
    def get_model(self):
        """초기화된 모델 반환"""
        return self._model
    
    def chat(self, prompt: str) -> str:
        """채팅 응답 생성"""
        if not self._model:
            raise RuntimeError("모델이 초기화되지 않았습니다.")
        
        response = self._model.invoke(prompt)
        return response.content


def main():
    """메인 실행 함수"""
    try:
        # 싱글턴 인스턴스 생성
        gemini_chat = GeminiLangChainSingleton()
        
        # 테스트 프롬프트들
        prompts = [
            "우주의 생태계는?",
            "인공지능의 미래는?",
            "파이썬 프로그래밍의 장점은?"
        ]
        
        print("\n" + "="*50)
        print("🚀 Gemini LangChain 싱글턴 테스트")
        print("="*50)
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📝 질문 {i}: {prompt}")
            print("-" * 40)
            
            response = gemini_chat.chat(prompt)
            print(f"🤖 응답: {response}")
        
        # 싱글턴 테스트 - 같은 인스턴스인지 확인
        another_instance = GeminiLangChainSingleton()
        print(f"\n🔍 싱글턴 테스트: {gemini_chat is another_instance}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()