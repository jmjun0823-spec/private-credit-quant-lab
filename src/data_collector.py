import yfinance as yf
import pandas as pd
import numpy as np

def fetch_market_data():
    """
    블로그 포스팅 입증에 필요한 거시경제 및 크레딧/메자닌/부동산 관련 지표 수집
    - SOFR/CD 프락시: 미국 단기채(SHY), 10년물 국채(^TNX)
    - 크레딧 스프레드 및 메자닌 지표: HYG(하이일드), BKLN(선순위 대출/Bank Loan)
    - 시장 변동성(Tail Risk): ^VIX
    - 리츠 및 부동산 PF 프락시: VNQ
    """
    tickers = {
        "TNX_10Y": "^TNX",      # 10년물 금리
        "VIX": "^VIX",          # Tail Risk
        "HYG": "HYG",            # 하이일드 채권 (Private Credit 대리 지표)
        "BKLN": "BKLN",          # Bank Loan/Senior Debt (변동금리 대출)
        "VNQ": "VNQ",            # 부동산 리츠 (부동산 PF 대체 지표)
        "SPY": "SPY"             # 전통 주식 시장
    }
    
    print("[1/4] yfinance를 통한 크레딧 및 거시경제 데이터 수집 시작...")
    raw_data = {}
    for name, ticker in tickers.items():
        try:
            df = yf.download(ticker, period="3y", interval="1d", progress=False)
            if 'Adj Close' in df.columns:
                raw_data[name] = df['Adj Close'].iloc[:, 0] if isinstance(df['Adj Close'], pd.DataFrame) else df['Adj Close']
            else:
                raw_data[name] = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
        except Exception as e:
            print(f"  - {name} ({ticker}) 수집 실패: {e}")
            
    df_market = pd.DataFrame(raw_data).ffill().dropna()
    
    # 파생 지표 계산
    # 1. SOFR / Base Rate 추정 (%)
    df_market['Base_Rate'] = df_market['TNX_10Y'] * 0.45  # SOFR/CD91일물 프락시
    
    # 2. Credit Spread 추정 (HYG 수익률 역산)
    df_market['Credit_Spread_bps'] = (np.maximum(0, (100 - df_market['HYG']) * 15)).rolling(5).mean()
    
    print("✓ 거시경제 및 크레딧 시장 데이터 수집 완료.")
    return df_market

if __name__ == "__main__":
    data = fetch_market_data()
    print(data.tail())
