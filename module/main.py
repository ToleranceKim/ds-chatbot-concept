import os
import torch
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import MinMaxScaler
from module.data import load_actual_data
from module.model import load_model
from module.forecast import iterative_forecast
from module.visualization import plot_ticket

def main(forecast_mode="1개월"):
    """
    forecast_mode: "1개월" 또는 "1주일" (다른 경우 확장 가능)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = r"C:\Users\USER\Desktop\my_git\ds-chatbot-concept\module\pretrained_price_lstm_model.pt"  # 평균티켓단가 예측 모델

    # 모델 불러오기
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 파일이 없습니다: {model_path}")
    model = load_model(model_path, device, input_size=1, hidden_size=50, num_layers=1)
    print("모델을 성공적으로 로드했습니다.")

    # 실제 데이터 불러오기 (최근 30일치 사용)
    actual_filepath = r"C:\Users\USER\Desktop\my_git\ds-chatbot-concept\db\기간별통계간별통계(평균티켓단가)201906~202502.csv"  
    dates_actual, actual_ticket, _ = load_actual_data(actual_filepath, lookback_days=30)

    # 실제 데이터는 스케일링되지 않은 원본 값이므로, 예측을 위해 MinMaxScaler 적용
    scaler = MinMaxScaler()
    # 실제 데이터를 2차원 배열로 변환 후 스케일링
    ticket_scaled = scaler.fit_transform(actual_ticket.reshape(-1, 1))

    # 마지막 lookback window: 예측 입력으로 사용할 데이터 (스케일된 값)
    lookback = 30  # 학습 시 사용한 lookback window와 동일
    last_window_ticket_scaled = ticket_scaled[-lookback:]
    last_date = dates_actual.iloc[-1]

    # 예측 기간 결정
    if forecast_mode == "1개월":
        horizon_days = 30
    elif forecast_mode == "1주일":
        horizon_days = 7
    else:
        raise ValueError("forecast_mode는 '1개월' 또는 '1주일'만 지원합니다.")

    forecast_start = last_date + pd.Timedelta(days=1)
    print(f"예측 기간: {horizon_days}일, 시작: {forecast_start.date()}")

    # 평균티켓단가 예측 수행 (스케일된 데이터를 사용)
    pred_ticket_scaled = iterative_forecast(model, last_window_ticket_scaled, horizon_days, device)
    
    # 예측값 역변환: 스케일된 예측 결과를 원래 단위(원)로 복원
    pred_ticket_values = scaler.inverse_transform(pred_ticket_scaled.reshape(-1,1)).flatten()

    # 예측 날짜 생성
    dates_forecast = pd.date_range(forecast_start, periods=horizon_days, freq='D')

    # 시각화 (평균티켓단가만)
    plot_ticket(
        dates_actual, actual_ticket,
        dates_forecast, pred_ticket_values
    )

if __name__ == "__main__":
    mode = input("예측 모드를 선택하세요 ('1개월' 또는 '1주일'): ").strip()
    main(forecast_mode=mode)
