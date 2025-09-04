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

# -----------------------------
# 4) Pydantic 모델 정의
# -----------------------------
class StockHistoryInput(BaseModel):
    """주식 조회를 위한 입력 모델"""
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: AAPL, TSLA, MSFT)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 5d, 1mo, 3mo, 6mo, 1y)")

def setup_pydantic_model():
    """Pydantic 모델 설정"""
    print("\n" + "="*50)
    print("📝 테스트 2: Pydantic 모델 정의")
    print("="*50)
    
    print("✅ StockHistoryInput 모델이 정의되었습니다.")
    print(f"📋 필수 필드:")
    for field_name, field in StockHistoryInput.model_fields.items():
        title = getattr(field, 'title', field_name)
        description = getattr(field, 'description', '설명 없음')
        print(f"  - {field_name}: {title} - {description}")
    
    return StockHistoryInput

# -----------------------------
# 5) 주식 조회 도구 (실제 yfinance 사용)
# -----------------------------
@tool
def get_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수 (실제 yfinance 사용)
    
    yfinance를 사용하여 실시간 주식 데이터를 가져옵니다.
    """
    try:
        import yfinance as yf
        
        ticker = stock_history_input.ticker.upper()
        period = stock_history_input.period
        
        print(f"📈 주식 조회: {ticker} ({period})")
        
        # yfinance로 주식 데이터 가져오기
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"❌ {ticker} 주식 데이터를 찾을 수 없습니다. 티커를 확인해주세요."
        
        # 최근 5개 데이터 포맷팅
        recent_data = hist.tail(5)
        
        # 결과 포맷팅
        result = f"📊 {ticker} 주식 데이터 ({period}):\n\n"
        result += "| Date       | Open   | High   | Low    | Close  | Volume     |\n"
        result += "|------------|--------|--------|--------|--------|------------|\n"
        
        for date, row in recent_data.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            open_price = f"${row['Open']:.2f}"
            high_price = f"${row['High']:.2f}"
            low_price = f"${row['Low']:.2f}"
            close_price = f"${row['Close']:.2f}"
            volume = f"{row['Volume']:,}"
            
            result += f"| {date_str} | {open_price:>7} | {high_price:>7} | {low_price:>7} | {close_price:>7} | {volume:>10} |\n"
        
        # 현재 가격 정보 추가
        current_price = stock.info.get('currentPrice', hist['Close'].iloc[-1])
        result += f"\n💰 현재 가격: ${current_price:.2f}"
        
        return result
        
    except ImportError:
        return "❌ yfinance 패키지가 설치되지 않았습니다. 'pip install yfinance'로 설치해주세요."
    except Exception as e:
        error_msg = f"주식 데이터 조회 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def setup_stock_tools():
    """주식 조회 도구 설정"""
    print("\n" + "="*50)
    print("📝 테스트 3: 주식 조회 도구 설정")
    print("="*50)
    
    # 도구 리스트 및 딕셔너리 구성
    tools = [get_current_time, get_stock_history]
    tool_dict = {
        "get_current_time": get_current_time,
        "get_stock_history": get_stock_history
    }
    
    # 도구를 모델에 바인딩
    llm_with_tools = llm.bind_tools(tools)
    
    print("✅ 도구들이 모델에 바인딩되었습니다.")
    print(f"📋 사용 가능한 도구: {[tool.name for tool in tools]}")
    
    return llm_with_tools, tool_dict

def test_time_query():
    """시간 조회 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 4: 시간 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_stock_tools()
    
    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("부산은 지금 몇시야?"),
    ]
    
    print("💬 사용자 질문: 부산은 지금 몇시야?")
    
    try:
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        print(f"🤖 AI 응답: {response.content}")
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
            
            for tool_call in response.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]
                print(f"🛠️ 도구 호출: {tool_call['name']}")
                print(f"📥 전달된 인자: {tool_call['args']}")
                
                tool_msg = selected_tool.invoke(tool_call)
                messages.append(tool_msg)
            
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
    print("📝 테스트 5: 주식 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_stock_tools()
    
    # 이전 대화 기록을 포함한 새로운 질문
    messages = [
        SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
        HumanMessage("테슬라는 한달 전에 비해 주가가 올랐나 내렸나?"),
    ]
    
    print("💬 사용자 질문: 테슬라는 한달 전에 비해 주가가 올랐나 내렸나?")
    
    try:
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        print(f"🤖 AI 응답: {response.content}")
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 호출된 도구 수: {len(response.tool_calls)}")
            
            for tool_call in response.tool_calls:
                selected_tool = tool_dict[tool_call["name"]]
                print(f"🛠️ 도구 호출: {tool_call['name']}")
                print(f"📥 전달된 인자: {tool_call['args']}")
                
                tool_msg = selected_tool.invoke(tool_call)
                messages.append(tool_msg)
                print(f"📤 도구 실행 결과 (일부): {tool_msg.content[:200]}...")
            
            final_response = llm_with_tools.invoke(messages)
            print(f"🎯 최종 답변: {final_response.content}")
        else:
            print("ℹ️ 도구 호출이 없었습니다.")
    
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
    
    return messages

def test_multiple_stocks():
    """여러 주식 조회 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 6: 여러 주식 조회")
    print("="*50)
    
    llm_with_tools, tool_dict = setup_stock_tools()
    
    stock_questions = [
        "애플 주식의 최근 1개월 성과는?",
        "마이크로소프트 1년 주가 변동은?",
        "구글 주식 정보를 알려줘",  # Mock 데이터 없는 경우 테스트
    ]
    
    for question in stock_questions:
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

def test_pydantic_validation():
    """Pydantic 모델 검증 테스트"""
    print("\n" + "="*50)
    print("📝 테스트 7: Pydantic 모델 검증")
    print("="*50)
    
    # 올바른 데이터
    print("✅ 올바른 데이터 테스트:")
    try:
        valid_input = StockHistoryInput(ticker="TSLA", period="1mo")
        print(f"  - 생성 성공: {valid_input}")
        print(f"  - 주식 코드: {valid_input.ticker}")
        print(f"  - 기간: {valid_input.period}")
    except Exception as e:
        print(f"  - 생성 실패: {e}")
    
    # 잘못된 데이터
    print("\n❌ 잘못된 데이터 테스트:")
    try:
        # 필수 필드 누락
        invalid_input = StockHistoryInput(ticker="AAPL")  # period 누락
        print(f"  - 생성 성공 (예상치 못함): {invalid_input}")
    except Exception as e:
        print(f"  - 생성 실패 (예상됨): {e}")

def show_usage_info():
    """사용법 정보"""
    print("\n" + "="*50)
    print("📝 사용법 및 정보")
    print("="*50)
    
    print("📈 지원하는 주식 코드 (Mock 데이터):")
    print("  - TSLA: 테슬라")
    print("  - AAPL: 애플")
    print("  - MSFT: 마이크로소프트")
    print("  - 기타: 기본 Mock 데이터 제공")
    
    print("\n📅 지원하는 기간:")
    print("  - 1d: 1일")
    print("  - 5d: 5일") 
    print("  - 1mo: 1개월")
    print("  - 3mo: 3개월")
    print("  - 6mo: 6개월")
    print("  - 1y: 1년")
    
    print("\n🔧 실제 사용을 위한 설정:")
    print("  1. yfinance 패키지 설치: pip install yfinance")
    print("  2. get_mock_stock_history를 실제 yfinance 함수로 교체")
    print("  3. Mock 데이터 대신 실제 API 호출로 변경")

def main():
    """메인 실행 함수"""
    print("🔥 Pydantic + LangChain Tools with Gemini API")
    print("="*60)
    
    try:
        # 모든 테스트 순차 실행
        test_basic_chat()
        setup_pydantic_model()
        test_time_query()
        test_stock_query()
        test_multiple_stocks()
        test_pydantic_validation()
        show_usage_info()
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print("💡 해결방법:")
        print("  1. GOOGLE_API_KEY 환경변수가 설정되었는지 확인")
        print("  2. 필요한 패키지들이 설치되었는지 확인:")
        print("     - pip install pytz pydantic")
        print("     - pip install yfinance  # 실제 주식 데이터용")
        print("  3. 인터넷 연결 상태 확인")

if __name__ == "__main__":
    main()