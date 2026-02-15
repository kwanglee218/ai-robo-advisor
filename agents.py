import os
from crewai import Agent
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.portfolio_tool import PortfolioTools # 👈 추가

# 1. 님이 만든 계산기 도구 가져오기
# (tools 폴더 안에 calculator_tool.py 파일이 있어야 합니다)
from tools.calculator_tool import StockTools

# 2. 환경변수 로드
load_dotenv()

# 3. 모델 및 검색 도구 설정
llm = ChatOpenAI(model="gpt-4o-mini")
search_tool = SerperDevTool()

class InvestmentAgents:
    
    # [1] 뉴스 조사원
    def market_researcher(self):
        return Agent(
            role='Market News Researcher',
            goal='주식 시장의 최신 뉴스와 트렌드를 수집',
            backstory="""당신은 월스트리트의 소식을 가장 빨리 접하는 뉴스/정보 수집가입니다.
            시장 분위기(Fear & Greed)와 주요 악재/호재를 파악하는 능력이 탁월합니다. 미국 증시를 분석하여 한국 증시를 예측하는 전문가 입니다.""",
            tools=[search_tool],
            llm=llm,
            verbose=True
        )

    # [2] 퀀트 분석가 (여기 줄 맞춤이 중요합니다!)
    def quant_analyst(self):
        return Agent(
            role='Quantitative Analyst',
            goal='기술적 지표(RSI, MACD) 계산 및 수급 분석',
            backstory="""당신은 차트와 데이터만 믿는 냉철한 퀀트 분석가입니다.
            기술적 지표를 계산하고, 외국인/기관 투자자의 수급 동향을 분석합니다. 산업별 수급을 분석하여 순환매를 분석하여 투자 전략을 제시합니다.""",
            # 계산기 도구(StockTools)와 검색 도구(search_tool) 둘 다 사용
            tools=[search_tool, StockTools.get_technical_indicators],
            llm=llm,
            verbose=True
        )
    
    # [3] 포트폴리오 전략가
    def chief_investment_officer(self):
        return Agent(
            role='Portfolio Manager',
            goal='수집된 정보를 바탕으로 현재 포트폴리오 전략 제시',
            backstory="""당신은 20년 경력의 포트폴리오 매니저입니다. 내 포트폴리오를 기반으로 매수/매도 전략 수립.
            전체적인 정보를 분석해서 현재 포트폴리오 매수/매도/보유 전략을 제시하고 냉철한 분석 보고서를 작성합니다.""",
            tools=[PortfolioTools.get_current_portfolio], # 이 사람은 도구 없이 머리로 판단함
            llm=llm,
            verbose=True
        )


# ---------------------------------------------------------
# [테스트용 코드] 이 파일을 직접 실행할 때만 작동
# ---------------------------------------------------------
# if __name__ == "__main__":
#     print("\n🧪 에이전트 테스트 시작...")
#     try:
#         agents = InvestmentAgents()
#         quant = agents.quant_analyst()
#         print("✅ 퀀트 에이전트 생성 성공!")
#         print(f"사용 도구: {[t.name for t in quant.tools]}")
#     except Exception as e:
#         print(f"❌ 에러 발생: {e}")  