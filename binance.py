import ccxt
import pandas as pd
import time
import re

binance = ccxt.binance()

def bull_market(ticker):
  pd.set_option('display.float_format', lambda x: '%.2f' % x)

  lists = binance.fetch_ohlcv(ticker, timeframe='1w')
  df = pd.DataFrame(lists)
  df['middle'] = df[4].rolling(window=20).mean()
  std = df[4].rolling(20).std(ddof=0)
  df['upper'] = df['middle'] + 2 * std
  df['lower'] = df['middle'] - 2 * std
  last_df = df['lower'].iloc[-1]
  fetch_ticker = binance.fetch_ticker(ticker)
  cur_price = fetch_ticker['close']
  high_df = df['upper'].iloc[-1]
  middle_df = df['middle'].iloc[-1]
  b = (cur_price - last_df) / (high_df - last_df)

  # mfi 구하기
  df['TP'] = (df[2] + df[3] + df[4]) / 3
  df['PMF'] = 0
  df['NMF'] = 0

  for i in range(len(df[4]) - 1):
    if df['TP'].values[i] < df['TP'].values[i + 1]:
      df['PMF'].values[i + 1] = df['TP'].values[i + 1] * df[5].values[i + 1]
      df['NMF'].values[i + 1] = 0
    else:
      df['NMF'].values[i + 1] = df['TP'].values[i + 1] * df[5].values[i + 1]
      df['PMF'].values[i + 1] = 0

  df['MFR'] = df['PMF'].rolling(window=10).sum() / df['NMF'].rolling(window=10).sum()
  df['MFI10'] = 100 - 100 / (1 + df['MFR'])
  mfi10 = df['MFI10'].iloc[-1]
  mfi10_week = df['MFI10'].iloc[-2]

  print('암호화폐:', ticker)
  print('현재 가격:', cur_price, '유로')
  print('상단선:', high_df)
  print('중심선:', middle_df)
  print('하단선:', last_df)
  print('%b:', b)
  print('전 주 MFI10:', mfi10_week)
  print('이번 주 MFI10:', mfi10)

  if b < 0.2 and mfi10 <= 20 and mfi10 > mfi10_week:
    return True
  elif b > 0.8 and mfi10 >= 80 and mfi10 < mfi10_week:
    return False

  # if b > 0.8 and mfi10 > 80:
  #   return True
  # elif b < 0.2 and mfi10 < 20:
  #   return False

  time.sleep(0.5)

ticker = list(binance.fetch_tickers().keys())
tickers = []
p = re.compile(r'\w+[/]EUR')

for i in ticker:
  if p.match(i) and 'UP' not in i and 'DOWN' not in i:
    tickers.append(i)

for ticker in tickers:
  is_bull = bull_market(ticker)

  if is_bull:
    print('매수하세요.')
    print('--------------------')
  else:
    print('매도하세요.')
    print('--------------------')