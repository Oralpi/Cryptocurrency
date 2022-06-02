import pandas as pd
from pykrx import stock
import datetime

def bull_market(ticker):
  pd.set_option('display.float_format', lambda x: '%.2f' % x)

  first_day = '19910101'
  today = datetime.datetime.today()
  today_strftime = today.strftime('%Y%m%d')
  df = stock.get_market_ohlcv(first_day, today_strftime, ticker, 'm')
  df['middle'] = df['종가'].rolling(window=20).mean()
  std = df['종가'].rolling(20).std(ddof=0)
  df['upper'] = df['middle'] + 2 * std
  df['lower'] = df['middle'] - 2 * std
  cur_price = df['종가'][1]
  last_df = df['lower'][-1]
  middle_df = df['middle'][-1]
  upper_df = df['upper'][-1]
  b = (cur_price - last_df) / (upper_df - last_df)
  # mfi
  df['TP'] = (df['lower'] + df['upper'] + df['종가']) / 3
  df['PMF'] = 0
  df['NMF'] = 0

  for i in range(len(df['종가']) - 1):
    if df['TP'].values[i] < df['TP'].values[i + 1]:
      df['PMF'].values[i + 1] = df['TP'].values[i + 1].astype(int) * df['거래량'].values[i + 1]
      df['NMF'].values[i + 1] = 0
    else:
      df['NMF'].values[i + 1] = df['TP'].values[i + 1].astype(int) * df['거래량'].values[i + 1]
      df['PMF'].values[i + 1] = 0

  df['MFR'] = df['PMF'].rolling(window=10).sum() / df['NMF'].rolling(window=10).sum()
  df['MFI10'] = 100 - 100 / (1 + df['MFR'])
  mfi10 = df['MFI10'][-1]
  mfi10_month = df['MFI10'][-2]
  # mfi

  # for ticker in stock.get_market_ticker_list(market='KOSPI'):
  #   name = stock.get_market_ticker_name(ticker)
  #
  #   if ticker == name:
  #     print('종목명:', name)
  #   else:
  #     print('종목코드:', ticker)

  print('종목코드:', ticker)
  print('현재 가격:', cur_price, '원')
  print('상단선:', upper_df)
  print('중심선:', middle_df)
  print('하단선:', last_df)
  print('%b:', b)
  print('전 주 MFI10:', mfi10_month)
  print('이번 주 MFI10:', mfi10)

  if b < 0.2 and mfi10 <= 20 and mfi10 > mfi10_month:
    return True
  elif b > 0.8 and mfi10 >= 80 and mfi10 < mfi10_month:
    return False

  # if b > 0.8 and mfi10 > 80:
  #   return True
  # elif b < 0.2 and mfi10 < 20:
  #   return False

tickers = stock.get_market_ticker_list(market='KOSPI')

for ticker in tickers:
  is_bull = bull_market(ticker)

  if is_bull:
    print('매수하세요.')
    print('--------------------')
  else:
    print('매도하세요.')
    print('--------------------')