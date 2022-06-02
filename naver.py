import FinanceDataReader as fdr
import pandas as pd
import time

def bull_market(ticker):
  pd.set_option('display.float_format', lambda x: '%.2f' % x)

  df = fdr.DataReader(ticker)
  df['middle'] = df['Close'].rolling(window=20).mean()
  std = df['Close'].rolling(20).std(ddof=0)
  df['upper'] = df['middle'] + 2 * std
  df['lower'] = df['middle'] - 2 * std
  print(df)
  last_df = df['lower'][-1]
  middle_df = df['middle'][-1]
  high_df = df['upper'][-1]
  cur_price = df['Close'][-1]
  b = (cur_price - last_df) / (high_df - last_df)

  # mfi 구하기
  df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
  df['PMF'] = 0
  df['NMF'] = 0

  for i in range(len(df['Close']) - 1):
    if df['TP'].values[i] < df['TP'].values[i + 1]:
      df['PMF'].values[i + 1] = df['TP'].values[i + 1] * df['Volume'].values[i + 1]
      df['NMF'].values[i + 1] = 0
    else:
      df['NMF'].values[i + 1] = df['TP'].values[i + 1] * df['Volume'].values[i + 1]
      df['PMF'].values[i + 1] = 0

  df['MFR'] = df['PMF'].rolling(window=10).sum() / df['NMF'].rolling(window=10).sum()
  df['MFI10'] = 100 - 100 / (1 + df['MFR'])
  mfi10 = df['MFI10'][-1]
  mfi10_week = df['MFI10'][-2]

  print('종목 코드:', ticker)
  print('현재 가격:', cur_price)
  print('상단선:', high_df)
  print('중심선:', middle_df)
  print('하단선:', last_df)
  print('%b:', b)
  print('전 주 MFI10:', mfi10_week)
  print('이번 주 MFI10:', mfi10)

  if b < 0.2 and mfi10 <= 20 and cur_price <= last_df:
    return True
  elif b > 0.8 and mfi10 >= 80 and cur_price >= middle_df:
    return False

tickers = fdr.StockListing('KOSPI')['Symbol']
print(tickers)

for ticker in tickers:
  is_bull = bull_market(ticker)

  if is_bull:
    print('매수하세요.')
    print('--------------------')
  else:
    print('매도하세요.')
    print('--------------------')