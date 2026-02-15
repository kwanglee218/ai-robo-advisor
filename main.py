import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import InvestmentAgents
from tasks import InvestmentTasks
# 1. 포트폴리오 도구 가져오기
from tools.portfolio_tool import PortfolioTools 

load_dotenv()

agents = InvestmentAgents()
tasks = InvestmentTasks()

print("\n\n######################################################")
print("## 🚀 AI 투자 심의 위원회 (자동 포트폴리오 분석 모드) ##")
print("######################################################\n")

# 2. 사용자 입력 제거 (input 삭제)
# 대신 도구에서 내 종목 리스트를 직접 가져옵니다.
my_stocks = PortfolioTools.MY_PORTFOLIO

print(f"📋 분석 대상 포트폴리오: {my_stocks}")

# 3. 에이전트 채용
researcher = agents.market_researcher()
quant = agents.quant_analyst()
strategist = agents.chief_investment_officer()

# 4. 업무(Task) 리스트 만들기 (반복문 사용!)
# 종목이 3개면, 업무도 3세트(총 9개)가 자동으로 만들어집니다.
crew_tasks = []

for stock in my_stocks:
    print(f"\n➕ '{stock}' 분석 업무를 추가하는 중...")
    
    # (1) 뉴스 조사
    task_research = tasks.research_task(researcher, stock)
    
    # (2) 퀀트 분석
    task_quant = tasks.quant_analysis_task(quant, stock)
    
    # (3) 최종 전략 (이 종목에 대한)
    task_strategy = tasks.strategy_task(strategist, [task_research, task_quant])
    
    # 만든 업무들을 리스트에 담기
    crew_tasks.append(task_research)
    crew_tasks.append(task_quant)
    crew_tasks.append(task_strategy)

# 5. 크루 결성 (tasks 리스트를 통째로 넘김)
crew = Crew(
    agents=[researcher, quant, strategist],
    tasks=crew_tasks, # <--- 여기가 핵심! (동적으로 생성된 업무들)
    process=Process.sequential,
    verbose=True
)

# 6. 작업 시작
print(f"\n\n🚀 총 {len(my_stocks)}개 종목에 대한 대규모 분석을 시작합니다...\n")
result = crew.kickoff()

print("\n\n########################")
print("## 📊 포트폴리오 종합 리포트 ##")
print("########################\n")
print(result)