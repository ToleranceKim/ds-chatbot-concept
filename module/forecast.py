import torch
import numpy as np

def iterative_forecast(model, last_window, forecast_steps, device):
    """
    model: 학습된 LSTM 모델
    last_window: numpy 배열, shape=(lookback, 1)
    forecast_steps: int, 예측할 일수
    device: torch.device
    반환: 예측값 numpy 배열, shape=(forecast_steps,)
    """
    model.eval()
    predictions = []
    input_seq = torch.tensor(last_window).float().unsqueeze(0).to(device)  # (1, lookback, 1)
    with torch.no_grad():
        for _ in range(forecast_steps):
            output = model(input_seq)  # (1,1)
            pred = output.cpu().numpy().item()
            predictions.append(pred)
            # 슬라이딩 윈도우 업데이트: 맨 앞 제거, 예측 결과 추가
            output_tensor = output.unsqueeze(0)  # (1,1,1)
            input_seq = torch.cat((input_seq[:, 1:, :], output_tensor), dim=1)
    return np.array(predictions)