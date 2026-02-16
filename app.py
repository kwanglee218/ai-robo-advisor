import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import InvestmentAgents
from tasks import InvestmentTasks
from tools.portfolio_tool import PortfolioTools
import yfinance as yf
import pandas as pd

if "ai_report" not in st.session_state:
    st.session_state["ai_report"] = None  # 처음엔 비어있음

# 1. 환경 변수 로드 (API 키 등)
load_dotenv()

# 2. 페이지 기본 설정 (제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="Personalized AI Robo Advisor", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded", #"collapsed"#"expanded
)

#all_tabs = ['Market Analysis','Quant Analysis','Robo Advisory']
#tabs = st.tabs(all_tabs)

my_stocks = PortfolioTools.MY_PORTFOLIO
selected_stock = st.sidebar
# with st.sidebar:
#     st.title('Portfolio')
#     category = st.radio("Stock",my_stocks)

# with tabs:
#     st.header(f"{my_stocks[i]} 분석")
# with st.radio:
#     for port_stock in st.sidebar:
#     with tabs:
#         stock_name = my_stocks[i]
#         st.header(f"{i+1}. {stock_name}")
#         st.subheader("💼 내 포트폴리오 분석")

# with tabs[0]:
#     st.title("📈 Personalized AI Robo Advisor")
#     st.markdown("---")
    
#    st.markdown(""" asdfas """)

# for i, tab in enumerate(tabs[1:]):
#     with tab:
#         stock_name = my_stocks[i]
#         st.header(f"{i+1}. {stock_name}")
#         st.subheader("💼 내 포트폴리오 분석")
        #st.button('Portfolio',['Market Research','Quant Analysis','Strategy'])
####### 

# 3. 헤더 및 사이드바 설정
#st.title("📈 Personalized AI Robo Advisor")
#st.markdown("---")

# for i, tab in enumerate(tabs[1:]):
#     with st.sidebar:
#         st.header("Your Portfolio")
#         mode = st.radio("Portfolio",["Market Research","Quant Analysis","Strategy"])
       # st.header("⚙️ 분석 설정")
        # 분석 모드 선택 (라디오 버튼)
        # mode = st.radio("분석 모드 선택", ["단일 종목 검색", "내 포트폴리오 전체 분석"])
        
        # st.info("💡 **팁:** 한국 주식은 티커 뒤에 반드시 **.KS**(코스피) 또는 **.KQ**(코스닥)를 붙이세요.")
        # st.markdown("---")
        # st.caption("Powered by CrewAI & GPT-4o")

# with st.sidebar:
#     st.header("⚙️ 분석 설정")
#     # 분석 모드 선택 (라디오 버튼)
#     mode = st.radio("분석 모드 선택", ["단일 종목 검색", "내 포트폴리오 전체 분석"])
    
#     st.info("💡 **팁:** 한국 주식은 티커 뒤에 반드시 **.KS**(코스피) 또는 **.KQ**(코스닥)를 붙이세요.")
#     st.markdown("---")
#     st.caption("Powered by CrewAI & GPT-4o")

# 4. 크루 실행 함수 (핵심 로직)
def run_crew(target_stock):
    """
    특정 종목(target_stock)을 분석하기 위해 에이전트들을 소집하고 일을 시킵니다.
    """
    # (1) 에이전트 & 태스크 클래스 가져오기
    agents = InvestmentAgents()
    tasks = InvestmentTasks()

    # (2) 에이전트(직원) 채용
    researcher = agents.market_researcher()  # 뉴스 담당
    quant = agents.quant_analyst()           # 숫자/수급 담당
    strategist = agents.chief_investment_officer()    # 최종 전략 담당

    # (3) 업무(Task) 배정
    task_research = tasks.research_task(researcher, target_stock)
    task_quant = tasks.quant_analysis_task(quant, target_stock)
    
    # 전략가에게는 앞선 두 명의 보고서를 모두 넘겨줍니다 (context)
    task_strategy = tasks.strategy_task(strategist, [task_research, task_quant])

    # (4) 팀(Crew) 결성
    crew = Crew(
        agents=[researcher, quant, strategist],
        tasks=[task_research, task_quant, task_strategy],
        process=Process.sequential, # 순서대로 실행
        verbose=True
    )

    # (5) 작업 시작!
    return crew.kickoff()

def run_crew_research(target_stock):
    """
    특정 종목(target_stock)을 분석하기 위해 에이전트들을 소집하고 일을 시킵니다.
    """
    # (1) 에이전트 & 태스크 클래스 가져오기
    agents = InvestmentAgents()
    tasks = InvestmentTasks()

    # (2) 에이전트(직원) 채용
    researcher = agents.market_researcher()  # 뉴스 담당

    # (3) 업무(Task) 배정
    task_research = tasks.research_task(researcher, target_stock)


    # (4) 팀(Crew) 결성
    crew_research = Crew(
        agents=[researcher],
        tasks=[task_research],
        process=Process.sequential, # 순서대로 실행
        verbose=True
    )

    # (5) 작업 시작!
    return crew_research.kickoff()

def run_crew_quant(target_stock):
    """
    특정 종목(target_stock)을 분석하기 위해 에이전트들을 소집하고 일을 시킵니다.
    """
    # (1) 에이전트 & 태스크 클래스 가져오기
    agents = InvestmentAgents()
    tasks = InvestmentTasks()

    # (2) 에이전트(직원) 채용
    quant = agents.quant_analyst()           # 숫자/수급 담당

    # (3) 업무(Task) 배정
    task_quant = tasks.quant_analysis_task(quant, target_stock)

    # (4) 팀(Crew) 결성
    crew_quant = Crew(
        agents=[quant],
        tasks=[task_quant],
        process=Process.sequential, # 순서대로 실행
        verbose=True
    )

    # (5) 작업 시작!
    return crew_quant.kickoff()

# ---------------------------------------------------------
# 5. 메인 화면 로직 (들여쓰기 주의!)
# ---------------------------------------------------------
    # 포트폴리오 도구에서 내 종목 리스트 가져오기
my_stocks = PortfolioTools.MY_PORTFOLIO
    
with st.sidebar:
    st.header("내 포트폴리오")
    selected_stock = st.radio(
        "분석할 종목을 선택하세요.", my_stocks
    )

font_css = """
<style>
    /* 탭 버튼 안의 글자 크기 조정 */
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
        font-size: 24px; /* 원하는 크기로 변경하세요 (기본: 16px 정도) */
        font-weight: bold; /* 굵게 */
    }
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

if "report_research" not in st.session_state:
    st.session_state["report_research"] = None
    st.session_state["stock_research"] = "" # 어떤 종목 결과인지 기록

if "report_quant" not in st.session_state:
    st.session_state["report_quant"] = None
    st.session_state["stock_quant"] = ""

if "report_final" not in st.session_state:
    st.session_state["report_final"] = None
    st.session_state["stock_final"] = ""

# ------------------------------------------------------------------

tabs_list = ['Market Analysis', 'Quant Analysis', 'Robo Advisory (종합)']
tab1, tab2, tab3 = st.tabs(tabs_list)

# ------------------------------------------------------------------
# 1번 탭: 시장 분석
# ------------------------------------------------------------------
with tab1:
#    st.header(f"🔍 {selected_stock}")
    st.markdown(f"### 🔍 {selected_stock}")    
    # [버튼 클릭 시] -> 결과를 계산하고 '저장'만 합니다.
    if st.button("🚀 AI 분석 실행하기", key="run_ai_1"):
        with st.spinner(f"AI가 '{selected_stock}' 시장 뉴스를 분석 중입니다..."):
            try:
                result = run_crew_research(selected_stock)
                
                # ⭐ 핵심: 결과와 종목명을 세션에 저장
                st.session_state["report_research"] = result
                st.session_state["stock_research"] = selected_stock
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

    # [화면 출력] -> 저장된 데이터가 있고, 현재 선택된 종목과 일치하면 보여줍니다.
    if st.session_state["report_research"] and st.session_state["stock_research"] == selected_stock:
        st.success("✅ 분석 완료!")
        st.markdown("---")
        st.markdown(st.session_state["report_research"])


# ------------------------------------------------------------------
# 2번 탭: 퀀트 분석
# ------------------------------------------------------------------
with tab2:
#    st.header(f"### 📈 {selected_stock}")
    st.markdown(f"### 📈 {selected_stock}")        
    if st.button("🚀 AI 분석 실행하기", key="run_ai_2"):
        with st.spinner(f"AI가 '{selected_stock}' 기술적 지표를 계산 중입니다..."):
            try:
                result = run_crew_quant(selected_stock)
                
                # ⭐ 핵심: 저장
                st.session_state["report_quant"] = result
                st.session_state["stock_quant"] = selected_stock
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

    # [화면 출력]
    if st.session_state["report_quant"] and st.session_state["stock_quant"] == selected_stock:
        st.success("✅ 분석 완료!")
        st.markdown("---")
        st.markdown(st.session_state["report_quant"])


# ------------------------------------------------------------------
# 3번 탭: 종합 전략 (Robo Advisory)
# ------------------------------------------------------------------
with tab3:
#    st.header("### 💰 AI 투자 전략 보고서")
    st.markdown("### 💰 AI 투자 전략 보고서")    
    if st.button("🚀 AI 분석 실행하기", key="run_ai_3"):
        with st.spinner("AI 위원회가 최종 전략을 수립하고 있습니다..."):
            try:
                result = run_crew(selected_stock)
                
                # ⭐ 핵심: 저장
                st.session_state["report_final"] = result
                st.session_state["stock_final"] = selected_stock

            except Exception as e:
                st.error(f"오류 발생: {e}")

    # [화면 출력]
    if st.session_state["report_final"] and st.session_state["stock_final"] == selected_stock:
        st.success("✅ 분석 완료!")
        st.markdown("---")
        st.markdown(st.session_state["report_final"])
# tabs_list = ['Market Analysis', 'Quant Analysis', 'Robo Advisory (종합)']

# tab1, tab2, tab3 = st.tabs(tabs_list)

# with tab1:
#     st.header(f"🤖 {selected_stock} AI 시장 분석")
    
#     # 버튼을 눌러야만 실행 (비용 절약 & 사용자 의도 확인)
#     if st.button("🚀 AI 분석 실행하기", key="run_ai_1"):
        
#         with st.spinner(f"AI 위원회가 '{selected_stock}'을(를) 분석 중입니다... (약 2분 소요)"):
#             try:
#                 # 위에서 만든 함수 호출
#                 final_research_report = run_crew_research(selected_stock)
#                 #st.markdown(f'### <span style="font-size: 20px;">{final_research_report}</span>',unsafe_allow_html=True)
#                 st.success("분석이 완료되었습니다!")
#                 st.markdown("---")
#                 st.markdown(final_research_report)
                
#             except Exception as e:
#                 st.error(f"오류가 발생했습니다: {e}")

# with tab2:
#     st.header(f"🤖 {selected_stock} AI 퀀트 분석")
    
#     # 버튼을 눌러야만 실행 (비용 절약 & 사용자 의도 확인)
#     if st.button("🚀 AI 분석 실행하기", key="run_ai_2"):
        
#         with st.spinner(f"AI 위원회가 '{selected_stock}'을(를) 분석 중입니다... (약 2분 소요)"):
#             try:
#                 # 위에서 만든 함수 호출
#                 final_quant_report = run_crew_quant(selected_stock)
                
#                 st.success("분석이 완료되었습니다!")
#                 st.markdown("---")
#                 st.markdown(final_quant_report)
                
#             except Exception as e:
#                 st.error(f"오류가 발생했습니다: {e}")

# with tab3:
#     st.header("AI 투자 전략 보고서")
# #    st.write(f"현재 선택된 종목: **{selected_stock}**")

# #     # 버튼을 눌러야만 실행 (비용 절약 & 사용자 의도 확인)
#     if st.button("🚀 AI 분석 실행하기", key="run_ai_3"):

#         with st.spinner("AI 위원회가 투자전략을 논의하고 있습니다."):
#             try:
#                  # 위에서 만든 함수 호출
#                 final_report = run_crew(selected_stock)

#                 st.success("분석이 완료되었습니다!")
#                 st.markdown("---")
#                 st.markdown(final_report)

#             except Exception as e:
#                 st.error(f"오류가 발생했습니다: {e}")
#                 st.warning("팁: agents.py나 tasks.py의 함수 이름이 일치하는지 확인해보세요.")










#     with tabs[0]:
#         if st.button("🔥 전체 포트폴리오 분석 시작"):
        
#         # 반복문으로 종목 하나씩 분석
#             for stock in my_stocks:
#                 with st.spinner(f"'{stock}' 분석 중...'"):
#                     try:
#                         # 크루 실행
#                         result = run_crew(stock)
#                         st.markdown(result) 
                        
#                     except Exception as e:
#                         st.error(f"'{stock}' 분석 중 에러 발생: {e}")

# elif mode == "단일 종목 검색":
#     # 사용자 입력 받기
#     stock_symbol = st.text_input("분석할 종목 티커 입력 (예: TSLA, 005930.KS, 247540.KQ)", "TSLA")
    
#     if st.button("🚀 분석 시작"):
#         if not stock_symbol:
#             st.warning("티커를 입력해주세요.")
#         else:
#             with st.spinner(f"AI 위원회가 '{stock_symbol}'을(를) 정밀 분석 중입니다..."):
#                 try:
#                     # 크루 실행
#                     result = run_crew(stock_symbol)
                    
#                     st.success("분석 완료!")
#                     st.markdown("---")
#                     st.subheader(f"📊 {stock_symbol} 최종 투자 리포트")
#                     st.markdown(result)
                    
#                 except Exception as e:
#                     st.error(f"에러 발생: {e}")
#                     st.error("팁: API Key가 올바르게 설정되었는지 확인하세요.")

        
#         st.success("✅ 모든 포트폴리오 분석이 완료되었습니다!")
#         st.balloons() # 성공 축하 풍선 효과























#################################
# if mode == "단일 종목 검색":
#     # 사용자 입력 받기
#     stock_symbol = st.text_input("분석할 종목 티커 입력 (예: TSLA, 005930.KS, 247540.KQ)", "TSLA")
    
#     if st.button("🚀 분석 시작"):
#         if not stock_symbol:
#             st.warning("티커를 입력해주세요.")
#         else:
#             with st.spinner(f"AI 위원회가 '{stock_symbol}'을(를) 정밀 분석 중입니다..."):
#                 try:
#                     # 크루 실행
#                     result = run_crew(stock_symbol)
                    
#                     st.success("분석 완료!")
#                     st.markdown("---")
#                     st.subheader(f"📊 {stock_symbol} 최종 투자 리포트")
#                     st.markdown(result)
                    
#                 except Exception as e:
#                     st.error(f"에러 발생: {e}")
#                     st.error("팁: API Key가 올바르게 설정되었는지 확인하세요.")

# elif mode == "내 포트폴리오 전체 분석":
#     # 포트폴리오 도구에서 내 종목 리스트 가져오기
#     my_stocks = PortfolioTools.MY_PORTFOLIO
     
# #    st.subheader("💼 내 포트폴리오 분석")
    
#     if st.button("🔥 전체 포트폴리오 분석 시작"):
        
#         # 반복문으로 종목 하나씩 분석
#         for stock in my_stocks:
#             with st.spinner(f"'{stock}' 분석 중...'"):
#                 try:
#                     # 크루 실행
#                     result = run_crew(stock)
#                     st.markdown(result) 
                    
#                 except Exception as e:
#                     st.error(f"'{stock}' 분석 중 에러 발생: {e}")
        
#         st.success("✅ 모든 포트폴리오 분석이 완료되었습니다!")
#         st.balloons() # 성공 축하 풍선 효과