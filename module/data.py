# data.py
import pandas as pd

def load_actual_data(filepath=None, lookback_days=30):
    """
    filepath: 실제 데이터 CSV 파일 경로 (None이면 기본 경로 사용)
    lookback_days: 예측 입력에 사용할 최근 데이터 일수
    반환: (dates_actual, actual_ticket, actual_revenue)
    """

    # 2) CSV 파일을 읽고, 날짜 컬럼을 datetime으로 변환
    df = pd.read_csv(r'C:\Users\USER\Desktop\my_git\ds-chatbot-concept\db\기간별통계간별통계(평균티켓단가)201906~202502.csv', encoding='utf-8')  # 필요 시 encoding 변경
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d', errors='coerce') # 변환 실패 시 NaT 처리

    # 3) NaT(날짜 변환 실패)나 결측치가 있으면 제거
    df = df.dropna(subset=['날짜'])

    # 4) 날짜 오름차순 정렬
    df = df.sort_values('날짜')

    # 5) 전체 데이터 중 최근 lookback_days만 사용
    df_recent = df.tail(lookback_days)

    # 6) 반환할 데이터 준비
    dates_actual = df_recent['날짜']
    actual_ticket = df_recent['평균티켓단가'].values
    # 만약 CSV에 매출액이 있는 경우만 사용 (없다면 None 처리)
    actual_revenue = df_recent['매출액'].values if '매출액' in df_recent.columns else None

    return dates_actual, actual_ticket, actual_revenue
