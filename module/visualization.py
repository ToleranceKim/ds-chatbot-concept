import os
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm

def set_font():
    # 운영체제별 한글 폰트 설정 (명시적 TTF 파일 경로 사용)
    if platform.system() == 'Windows':
        # Windows 기본 폰트 (Malgun Gothic)
        font_path = r'C:\Windows\Fonts\malgun.ttf'
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = 'Malgun Gothic'
        else:
            plt.rcParams['font.family'] = 'sans-serif'
    elif platform.system() == 'Darwin':
        # macOS 기본 한글 폰트 (AppleGothic)
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        # Linux: 보통 NanumGothic이 설치되어 있음
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = 'NanumGothic'
        else:
            plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False

def plot_ticket(dates_actual, actual_ticket, dates_forecast, pred_ticket):
    """
    실제와 예측 결과를 하나의 subplot으로 시각화 (평균티켓단가만).
    """
    # 한글 폰트 설정 함수 호출 (주피터가 아닌 파이썬 파일에서도 동작)
    set_font()

    sns.set_style("whitegrid")
    sns.set_context("talk", font_scale=1.2)
    sns.set_palette("Set2")

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle("평균티켓단가 예측 결과", fontsize=18, fontweight='bold')

    # 실제 평균티켓단가 (C0, 원형 마커)
    ax.plot(dates_actual, actual_ticket, label='실제 평균티켓단가',
            color='C0', marker='o')
    # 예측 평균티켓단가 (C1, 점선, 원형 마커)
    ax.plot(dates_forecast, pred_ticket, label='예측 평균티켓단가',
            color='C1', linestyle='--', marker='o')

    ax.set_ylabel("평균티켓단가 (원)", fontsize=13)
    ax.set_title("평균티켓단가 (최근 vs. 예측)", fontsize=14)
    ax.legend()

    # 날짜 축 포맷팅: AutoDateLocator와 ConciseDateFormatter 사용
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    plt.xticks(rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
