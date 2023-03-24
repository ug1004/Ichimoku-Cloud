import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ichimoku(df):
    high_prices = df['High']
    close_prices = df['Close']
    low_prices = df['Low']

    # 전환선 (Tenkan-sen)
    tenkan_sen = (high_prices.rolling(9).max() + low_prices.rolling(9).min()) / 2

    # 기준선 (Kijun-sen)
    kijun_sen = (high_prices.rolling(26).max() + low_prices.rolling(26).min()) / 2

    # 선행스팬 1 (Senkou Span A)
    senkou_span_A = ((tenkan_sen + kijun_sen) / 2).shift(26)

    # 선행스팬 2 (Senkou Span B)
    senkou_span_B = ((high_prices.rolling(52).max() + low_prices.rolling(52).min()) / 2).shift(26)

    # 후행스팬 (Chikou Span)
    chikou_span = close_prices.shift(-26)

    return tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, chikou_span

# 데이터 다운로드
symbol = "BTC-USD"
data = yf.download(symbol, start="2020-01-01", end="2021-09-01")

# 일목균형표 계산
tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, chikou_span = ichimoku(data)

# 결과 시각화
plt.figure(figsize=(14, 8))
plt.plot(data.index, data['Close'], label='Close', color='black', linewidth=1)
plt.plot(data.index, tenkan_sen, label='Tenkan-sen', color='blue', linestyle='dotted', linewidth=1)
plt.plot(data.index, kijun_sen, label='Kijun-sen', color='red', linestyle='dotted', linewidth=1)
plt.plot(data.index, senkou_span_A, label='Senkou Span A', color='green', linestyle='dashed', linewidth=1)
plt.plot(data.index, senkou_span_B, label='Senkou Span B', color='orange', linestyle='dashed', linewidth=1)
plt.plot(data.index, chikou_span, label='Chikou Span', color='purple', linestyle='dotted', linewidth=1)
plt.fill_between(data.index, senkou_span_A, senkou_span_B, where=senkou_span_A >= senkou_span_B, color='lightgreen', alpha=0.25)
plt.fill_between(data.index, senkou_span_A, senkou_span_B, where=senkou_span_A < senkou_span_B, color='lightcoral', alpha=0.25)
plt.legend()
plt.title(f'{symbol} Ichimoku Kinko Hyo')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
