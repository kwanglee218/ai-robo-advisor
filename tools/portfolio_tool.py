
# tools/portfolio_tool.py
from crewai.tools import tool

class PortfolioTools:
    
    # 1. 여기에 내 종목들을 '리스트'로 정의합니다.
    # (나중에 이 부분만 수정하면 분석 대상이 바뀝니다)
    MY_PORTFOLIO = [
        "Hanwha Solutions Corp",
        "Hotel Shilla Co Ltd",
        "Doosan Enerbility Co Ltd",
        "Hugel, Inc.",
        "LIG Nex1 Co., Ltd.", 
        "HD Hyundai Electric Co., Ltd." 
#         "ALTEOGEN Inc."  
    ]

    @tool("User Portfolio Retrieval")
    def get_current_portfolio():
        """
        사용자의 포트폴리오 목록을 문자열로 반환합니다.
        """
        # 위에 정의된 리스트를 가져와서 문자열로 만듭니다.
        return ", ".join(PortfolioTools.MY_PORTFOLIO)