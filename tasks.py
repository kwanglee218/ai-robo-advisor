### Agent들에게 내려주는 "업무 지시서(SOP)"
## "무슨 일을 시킬 것인가?"를 정의
## 업무 지시서, 결과물 양식을 만듬
# Description (지시사항): "테슬라의 최근 1주일 뉴스를 찾아서 요약해라."
# Expected Output (결과물 양식): "반드시 3줄 요약으로 작성하고, 마크다운(Markdown) 형식을 써라."
# Context (참고 자료): "앞에 김철수 직원이 조사한 내용을 보고 나서 이 일을 해라."
# 요약: Agent에게 '테슬라 분석 보고서 써와'라고 업무 지시 내린다.

from crewai import Task

class InvestmentTasks:

    def research_task(self, agent, stock_symbol):
        return Task(
            description=f"""
            '{stock_symbol}'의 최근 3일간 주요 뉴스, 호재/악재, 시장 분위기를 조사하세요. 미국 주식시장에 상장된 경쟁사 분석을 통해 향후 주가를 예측하세요."
            """,
            agent=agent,
            expected_output="뉴스 요약 및 시장 심리 보고서"
        )

    # 👇 [추가됨] 퀀트/기술적 분석 업무
    def quant_analysis_task(self, agent, stock_symbol):
        return Task(
            description=f"""
            '{stock_symbol}'에 대해 다음 정량적 분석을 수행하세요:
            
            1. **기술적 지표 계산:** - 도구(Technical Analysis Tool)를 사용하여 RSI, MACD, 현재 주가를 계산하세요.
               - 과매수/과매도 여부와 골든크로스/데드크로스를 판단하세요.
               - 추세전환 여부 판단하세요.

            2. **수급 분석 (Supply/Demand):**
               - 검색 도구를 사용하여 최근 외국인, 기관, 개인 투자자의 매수/매도 동향을 찾으세요.
               - 수급 분석을 통해 향후 주가 상승 예측하세요.
               
            3. **산업 분석 (Sector Analysis):**
               - 해당 종목이 속한 산업(예: 반도체, 2차전지)으로 자금이 들어오는지(순환매) 확인하세요.
            """,
            agent=agent,
            expected_output= "퀀트분석 보고서 "#"RSI/MACD 수치, 수급 주체별 동향, 산업 섹터 흐름이 포함된 분석 데이터"
        )
    
    def strategy_task(self, agent, context):
        return Task(
            description="""
            시장 조사(News), 퀀트 분석(Quant) 결과를 종합하여 최종적으로 현재 포트폴리오 전략을 제시하세요.
            
            포함 항목:
            1. [User Portfolio Retrieval] 도구를 사용하여 현재 보유 종목을 확인하세요. 
            2. 앞서 조사된 시장 상황과 퀀트 분석 결과를 바탕으로,
               보유 종목을 'Buy', 'Sell', 'Hold'로 결정하세요.
            3. 기술적 분석 (RSI, MACD 지표 해석), 수급 분석 (개인/외국인/기관)을 바탕으로 이유를 설명하세요.
            """,
            agent=agent,
            context=context, # 앞선 두 에이전트의 결과를 모두 받음
            expected_output="보유 종목별 매매 대응 전략 보고서"
        )
