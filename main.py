import sys
from src.data_collector import fetch_market_data
from src.simulator import run_mdd_simulation, calculate_expected_return
from src.report_generator import generate_visualizations, generate_markdown_report

def main():
    print("==================================================")
    print("   사모대출 블로그 데이터 입증 파이프라인 실행   ")
    print("==================================================")
    
    # 1. 크레딧 및 거시경제 데이터 수집
    market_df = fetch_market_data()
    
    # 2. 정량 모델 계산 및 몬테카를로 시뮬레이션
    print("[2/4] 사모대출 E(R) 및 Venture Debt MDD 시뮬레이션 실행 중...")
    er_res = calculate_expected_return()
    mdd_res = run_mdd_simulation()
    
    # 3. 차트 시각화 및 마크다운 리포트 생성
    print("[3/4] 시각화 차트 이미지 및 마크다운 보고서 생성 완료...")
    generate_visualizations()
    generate_markdown_report(market_df)
    
    print("[4/4] 모든 데이터 분석 및 입증 보고서 작업 완료!")
    print("      생성 파일 위치: outputs/generated_report.md 및 outputs/*.png")
    print("==================================================")

if __name__ == "__main__":
    main()
