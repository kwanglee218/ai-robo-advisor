import yfinance as yf
import pandas as pd
from crewai.tools import tool

class StockTools:

    @tool("Technical Analysis Tool")
    def get_technical_indicators(ticker: str):
        """
        주식 티커(예: TSLA, 005930.KS)를 입력받아
        현재 주가, RSI(14), MACD, 이동평균선을 계산해서 반환합니다.
        """
        print(f"\n📈 {ticker} 기술적 지표 계산 중...")
        
        # 1. 데이터 가져오기 (최근 6개월)
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="6mo")
            
            if df.empty:
                return f"Error: {ticker} 데이터를 찾을 수 없습니다."

            # 2. RSI 계산 (14일 기준)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # 3. MACD 계산 (12, 26, 9)
            df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = df['EMA12'] - df['EMA26']
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # 4. 최신 데이터 추출
            latest = df.iloc[-1]
            prev = df.iloc[-2]

            # 5. MACD 신호 해석 (골든크로스/데드크로스)
            macd_signal = "중립"
            if latest['MACD'] > latest['Signal_Line'] and prev['MACD'] <= prev['Signal_Line']:
                macd_signal = "골든크로스 (매수 신호)"
            elif latest['MACD'] < latest['Signal_Line'] and prev['MACD'] >= prev['Signal_Line']:
                macd_signal = "데드크로스 (매도 신호)"

            report = f"""
            [기술적 분석 결과: {ticker}]
            - 현재 주가: {latest['Close']:.2f}
            - RSI (14): {latest['RSI']:.2f} (70이상 과매수, 30이하 과매도)
            - MACD: {latest['MACD']:.2f}
            - MACD Signal: {latest['Signal_Line']:.2f}
            - MACD 상태: {macd_signal}
            """
            return report

        except Exception as e:
            return f"계산 중 에러 발생: {str(e)}"