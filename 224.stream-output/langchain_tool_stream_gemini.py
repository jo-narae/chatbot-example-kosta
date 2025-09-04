import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from datetime import datetime
import pytz
import google.generativeai as genai
from pydantic import BaseModel, Field

# -----------------------------
# 1) 환경설정
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("환경변수 GOOGLE_API_KEY가 설정되지 않았습니다.")
genai.configure(api_key=api_key)

print("✅ 환경변수가 성공적으로 로드되었습니다.")

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
# 3) 기본 도구: 시간 조회
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

print("✅ 시간 조회 도구가 정의되었습니다.")

# -----------------------------
# 4) Pydantic 모델 정의
# -----------------------------
class StockHistoryInput(BaseModel):
    """주식 조회를 위한 입력 모델"""
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: AAPL, TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 1mo, 1y)")

print("✅ StockHistoryInput 모델이 정의되었습니다.")

# -----------------------------
# 5) 주식 조회 도구
# -----------------------------
@tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수"""
    try:
        import yfinance as yf
        
        ticker = stock_history_input.ticker
        period = stock_history_input.period
        
        print(f"📈 주식 조회: {ticker} ({period})")
        
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        
        if history.empty:
            return f"❌ {ticker} 주식 데이터를 찾을 수 없습니다."
        
        history_md = history.to_markdown()
        return f"📊 {ticker} 주식 데이터:\n{history_md}"
        
    except ImportError as e:
        error_msg = f"❌ yfinance 패키지가 설치되지 않았습니다: {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"주식 데이터 조회 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

print("✅ 주식 조회 도구가 정의되었습니다.")

def setup_tools():
    """도구 설정"""
    print("\n" + "="*50)
    print("📝 테스트 2: 도구 설정")
    print("="*50)
    
    # 도구를 tools 리스트에 추가하고, tool_dict에도 추가
    tools = [get_current_time, get_yf_stock_history]
    tool_dict = {
        "get_current_time": get_current_time, 
        "get_yf_stock_history": get_yf_stock_history
    }

    # 도구를 모델에 바인딩: 모델에 도구를 바인딩하면, 도구를 사용하여 llm 답변을 생성할 수 있음
    llm_with_tools = llm.bind_tools(tools)
    
    print("✅ 도구들이 모델에 바인딩되었습니다.")
    print(f"📋 사용 가능한 도구: {[tool.name for tool in tools]}")
    
    return llm_with_tools, tool_dict

def test_time_query():
    """시간 조회 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 3: 시간 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_tools()
    
    # 사용자의 질문과 tools 사용하여 llm 답변 생성
    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("부산은 지금 몇시야?"),
    ]
    
    print("💬 사용자 질문: 부산은 지금 몇시야?")
    
    try:
        # llm_with_tools를 사용하여 사용자의 질문에 대한 llm 답변 생성
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        print(f"🤖 AI 응답: {response.content}")
        print(f"📋 메시지 수: {len(messages)}")
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
            
            for tool_call in response.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]  # tool_dict를 사용하여 도구 함수를 선택
                print(f"🛠️ 도구 호출: {tool_call['name']}")
                print(f"📥 전달된 인자: {tool_call['args']}")  # 도구 호출 시 전달된 인자 출력
                
                # LangChain 도구 호출 패턴: tool_call dict를 직접 전달
                from langchain_core.messages import ToolMessage
                
                tool_result = selected_tool.invoke(tool_call["args"])
                # 결과를 ToolMessage로 감싸기
                tool_msg = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
                messages.append(tool_msg)
            
            # 최종 답변 생성
            final_response = llm_with_tools.invoke(messages)
            print(f"🎯 최종 답변: {final_response.content}")
        else:
            print("ℹ️ 도구 호출이 없었습니다.")
    
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
    
    return messages

def test_stock_query():
    """주식 조회 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 4: 주식 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_tools()
    
    # 이전 대화 기록을 포함한 새로운 질문
    messages = [
        SystemMessage("너는 사용자의 질문에 답변하기 위해 tools를 사용할 수 있다. 주식 관련 질문이 나오면 get_yf_stock_history 도구를 사용해 실제 데이터를 조회해야 한다."),
        HumanMessage("테슬라(TSLA) 주식의 최근 1개월(1mo) 데이터를 조회해서 주가 변화를 알려줘"),
    ]
    
    print("💬 사용자 질문: 테슬라(TSLA) 주식의 최근 1개월(1mo) 데이터를 조회해서 주가 변화를 알려줘")
    
    try:
        response = llm_with_tools.invoke(messages)
        print(f"🤖 AI 응답: {response.content}")
        messages.append(response)
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
            
            for tool_call in response.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]
                print(f"🛠️ 도구 호출: {tool_call['name']}")
                print(f"📥 전달된 인자: {tool_call['args']}")
                
                # LangChain 도구 호출 패턴: tool_call dict를 직접 전달
                from langchain_core.messages import ToolMessage
                
                tool_result = selected_tool.invoke(tool_call["args"])
                # 결과를 ToolMessage로 감싸기
                tool_msg = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
                messages.append(tool_msg)
                print(f"📤 도구 실행 결과 (일부): {tool_result[:200]}...")
            
            final_response = llm_with_tools.invoke(messages)
            print(f"🎯 최종 답변: {final_response.content}")
        else:
            print("ℹ️ 도구 호출이 없었습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
    
    return messages

def test_basic_stream():
    """기본 스트림 출력 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 5: 기본 스트림 출력")
    print("="*50)
    
    print("💬 사용자 질문: 잘 지냈어? 한국 사회의 문제점에 대해 이야기해줘.")
    print("🔄 스트림 응답:")
    
    try:
        for chunk in llm.stream([HumanMessage("잘 지냈어? 한국 사회의 문제점에 대해 이야기해줘.")]):
            print(chunk.content, end='', flush=True)
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

def test_tool_stream():
    """도구 사용 스트림 출력 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 6: 도구 사용 스트림 출력")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_tools()
    
    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("부산은 지금 몇시야?"),
    ]
    
    print("💬 사용자 질문: 부산은 지금 몇시야?")
    print("🔄 도구 호출 스트림:")
    
    try:
        response = llm_with_tools.stream(messages)

        # 파편화된 tool_call 청크를 하나로 합치기 
        is_first = True
        for chunk in response:    
            print(f"청크 타입: {type(chunk).__name__}")
            
            if is_first:
                is_first = False
                gathered = chunk
            else:
                gathered += chunk
            
            print(f"내용: '{gathered.content}', 도구 호출: {len(gathered.tool_calls) if gathered.tool_calls else 0}개")

        messages.append(gathered)
        
        print(f"\n🔧 통합된 응답: {gathered}")
        
        # 도구 실행
        if hasattr(gathered, 'tool_calls') and gathered.tool_calls:
            for tool_call in gathered.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]  # tool_dict를 사용하여 도구 이름으로 도구 함수를 선택
                print(f"🛠️ 도구 호출: {tool_call['name']}")
                print(f"📥 전달된 인자: {tool_call['args']}")  # 도구 호출 시 전달된 인자 출력
                
                # LangChain 도구 호출 패턴: tool_call dict를 직접 전달
                from langchain_core.messages import ToolMessage
                
                tool_result = selected_tool.invoke(tool_call["args"])
                # 결과를 ToolMessage로 감싸기
                tool_msg = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
                messages.append(tool_msg)

        print(f"📋 총 메시지 수: {len(messages)}")
        
        # 최종 답변 스트림
        print("\n🎯 최종 답변 스트림:")
        for chunk in llm_with_tools.stream(messages):
            print(chunk.content, end='', flush=True)
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
    
    return messages

def show_usage_info():
    """사용법 정보"""
    print("\n" + "="*50)
    print("📝 사용법 및 정보")
    print("="*50)
    
    print("🔧 스트림 출력의 특징:")
    print("  - 실시간으로 응답을 받을 수 있음")
    print("  - 긴 응답의 경우 사용자 경험 향상")
    print("  - 도구 호출 시 청크들이 파편화되어 전달됨")
    print("  - 파편화된 청크를 하나로 합쳐야 함")
    
    print("\n🛠️ 필요한 패키지:")
    print("  - pip install yfinance (주식 데이터용)")
    print("  - pip install pytz (시간대 처리용)")
    print("  - pip install pydantic (데이터 검증용)")
    
    print("\n⚠️ 주의사항:")
    print("  - 스트림 모드에서는 도구 호출이 여러 청크로 나뉘어 전달")
    print("  - gathered 객체로 청크를 누적해야 완전한 도구 호출 정보 확보")
    print("  - 인터넷 연결이 필요한 기능들 (yfinance)")

def main():
    """메인 실행 함수"""
    print("🔥 LangChain Tool Stream with Gemini API")
    print("="*60)
    
    try:
        # 모든 테스트 순차 실행
        test_basic_chat()
        test_time_query()
        test_stock_query()
        test_basic_stream()
        test_tool_stream()
        show_usage_info()
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print("💡 해결방법:")
        print("  1. GOOGLE_API_KEY 환경변수가 설정되었는지 확인")
        print("  2. 필요한 패키지들이 설치되었는지 확인:")
        print("     - pip install pytz pydantic yfinance")
        print("  3. 인터넷 연결 상태 확인")

if __name__ == "__main__":
    main()