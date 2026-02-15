import streamlit as st
from main import InvestmentCrew  # 님이 만든 CrewAI 클래스 가져오기

# 1. 페이지 설정
st.set_page_config(page_title="AI 투자 위원회", page_icon="📈")

st.title("📈 AI Investment Committee")
st.markdown("당신의 주식 투자를 돕는 **AI 전문가 팀**입니다.")

# 2. 사용자 입력
ticker = st.text_input("분석할 주식 티커를 입력하세요 (예: NVDA, TSLA)", "AAPL")

# # 3. 버튼 클릭 시 실행
# if st.button("투자 분석 시작 🚀"):
#     with st.spinner('AI 위원회가 데이터를 분석하고 회의 중입니다... (약 1분 소요)'):
#         try:
#             # CrewAI 실행
#             crew = InvestmentCrew(ticker)
#             result = crew.kickoff()
            
#             # 4. 결과 출력
#             st.success("분석 완료!")
#             st.markdown("### 📊 최종 투자 리포트")
#             st.markdown(result) # CrewAI 결과는 보통 Markdown이라 아주 예쁘게 나옵니다.
            
#         except Exception as e:
#             st.error(f"오류가 발생했습니다: {e}")

# # 사이드바 (옵션)
# with st.sidebar:
#     st.header("About")
#     st.info("이 앱은 CrewAI와 LangChain을 사용하여 만들어졌습니다.")