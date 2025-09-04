import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from datetime import datetime
import pytz
import google.generativeai as genai

# -----------------------------
# 1) 환경설정
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")
genai.configure(api_key=api_key)

# -----------------------------
# 2) Gemini 모델 초기화
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
)

print("✅ Gemini 모델이 초기화되었습니다.")

def test_basic_chat():
    """기본 채팅 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 1: 기본 채팅")
    print("="*50)
    
    response = llm.invoke([HumanMessage("잘 지냈어?")])
    print(f"🤖 Gemini 응답: {response.content}")
    return response

# -----------------------------
# 3) 커스텀 도구(Tool) 정의
# -----------------------------
@tool  # @tool 데코레이터를 사용하여 함수를 도구로 등록
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 llm 답변 생성에 사용됨
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        location_and_local_time = f'{timezone} ({location}) 현재시각 {now}'
        print(f"🕐 시간 조회: {location_and_local_time}")
        return location_and_local_time
    except Exception as e:
        error_msg = f"시간 조회 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def setup_tools():
    """도구 설정"""
    print("\n" + "="*50)
    print("📝 테스트 2: 도구 설정")
    print("="*50)
    
    # 도구를 tools 리스트에 추가하고, tool_dict에도 추가
    tools = [get_current_time]
    tool_dict = {"get_current_time": get_current_time}
    
    # 도구를 모델에 바인딩: 모델에 도구를 바인딩하면, 도구를 사용하여 llm 답변을 생성할 수 있음
    llm_with_tools = llm.bind_tools(tools)
    
    print("✅ 도구가 모델에 바인딩되었습니다.")
    print(f"📋 사용 가능한 도구: {[tool.name for tool in tools]}")
    
    return llm_with_tools, tool_dict

def test_tool_calling():
    """도구 호출 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 3: 도구 호출")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_tools()
    
    # 사용자의 질문과 tools 사용하여 llm 답변 생성
    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("부산은 지금 몇시야?"),
    ]
    
    print("💬 사용자 질문: 부산은 지금 몇시야?")
    
    # llm_with_tools를 사용하여 사용자의 질문에 대한 llm 답변 생성
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    
    print(f"🤖 AI 응답 (도구 호출 포함): {response.content}")
    
    # tool_calls가 있는지 확인
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
        
        # 각 도구 호출 처리
        for tool_call in response.tool_calls:
            selected_tool = tool_dict[tool_call["name"]]
            print(f"🛠️ 도구 호출: {tool_call['name']}")
            print(f"📥 전달된 인자: {tool_call['args']}")
            
            # 도구 함수를 호출하여 결과를 반환
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)
            
        # 도구 실행 결과를 포함한 최종 답변 생성
        print("\n🔄 도구 실행 결과를 바탕으로 최종 답변 생성 중...")
        final_response = llm_with_tools.invoke(messages)
        print(f"🎯 최종 답변: {final_response.content}")
        
        return final_response, messages
    else:
        print("ℹ️ 도구 호출이 없었습니다.")
        return response, messages

def test_multiple_locations():
    """여러 지역 시간 조회 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 4: 여러 지역 시간 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_tools()
    
    test_questions = [
        "서울은 지금 몇시야?",
        "도쿄의 현재 시간은?",
        "뉴욕은 지금 몇시지?",
        "런던의 현재 시간을 알려줘"
    ]
    
    for question in test_questions:
        print(f"\n💬 질문: {question}")
        
        messages = [
            SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
            HumanMessage(question),
        ]
        
        try:
            response = llm_with_tools.invoke(messages)
            messages.append(response)
            
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    selected_tool = tool_dict[tool_call["name"]]
                    tool_msg = selected_tool.invoke(tool_call)
                    messages.append(tool_msg)
                
                final_response = llm_with_tools.invoke(messages)
                print(f"🎯 답변: {final_response.content}")
            else:
                print(f"🤖 답변: {response.content}")
                
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")

def test_tool_without_calling():
    """도구 없이 일반 질문 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 5: 일반 질문 (도구 사용 불필요)")
    print("="*50)
    
    llm_with_tools, _ = setup_tools()
    
    general_questions = [
        "안녕하세요! 어떻게 지내세요?",
        "Python에서 리스트와 튜플의 차이점은?",
        "오늘 날씨가 좋네요",
        "LangChain이 뭐야?"
    ]
    
    for question in general_questions:
        print(f"\n💬 질문: {question}")
        
        messages = [
            SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다. 하지만 도구가 필요하지 않은 일반적인 질문에는 직접 답변해도 된다."),
            HumanMessage(question),
        ]
        
        try:
            response = llm_with_tools.invoke(messages)
            print(f"🤖 답변: {response.content}")
            
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print("🔧 도구 호출됨")
            else:
                print("💬 일반 답변")
                
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")

def show_available_timezones():
    """사용 가능한 타임존 예시"""
    print("\n" + "="*50)
    print("📝 사용 가능한 타임존 예시")
    print("="*50)
    
    sample_timezones = [
        ("Asia/Seoul", "서울"),
        ("Asia/Tokyo", "도쿄"),
        ("America/New_York", "뉴욕"),
        ("Europe/London", "런던"),
        ("America/Los_Angeles", "로스앤젤레스"),
        ("Australia/Sydney", "시드니"),
        ("Europe/Paris", "파리"),
        ("Asia/Shanghai", "상하이"),
    ]
    
    print("🌍 주요 도시별 타임존:")
    for timezone, city in sample_timezones:
        print(f"  {city}: {timezone}")

def main():
    """메인 실행 함수"""
    print("🛠️ LangChain Tools with Gemini API")
    print("="*50)
    
    try:
        # 모든 테스트 순차 실행
        test_basic_chat()
        test_tool_calling()
        test_multiple_locations()
        test_tool_without_calling()
        show_available_timezones()
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print("💡 해결방법:")
        print("  1. GOOGLE_API_KEY 환경변수가 설정되었는지 확인")
        print("  2. pytz 패키지가 설치되었는지 확인: pip install pytz")
        print("  3. 인터넷 연결 상태 확인")

if __name__ == "__main__":
    main()