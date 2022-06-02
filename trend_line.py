# import matplotlib.pyplot as plt
# import FinanceDataReader as fdr
# import datetime
# import numpy as np
# from scipy.stats import linregress
#
# def my_trend(source='N', ticker='BTC/KRW', df_period=300, step=10):
#   end_day0 = str(datetime.date.today())
#   start0 = str(datetime.date.today() - datetime.timedelta(weeks=df_period))
#
#   if source == 'N':
#     df = fdr.DataReader(ticker, start0, end_day0)
#
#   # 트릭
#   df['index1'] = df.reset_index().index
#   df0 = df.copy()
#   df_len = len(df)
#   # 고점 추세선
#   df1 = df0.copy()
#   df1['High1'] = np.where(df1['index1'] >= df_len-step, df['High'].iloc[df_len-step], df['High'])
#   # 트릭: 지정한 스텝 구간 고가를 직전 고가 수준으로 멈추게 함.
#
#   while len(df1) > 3:
#     reg = linregress(x=df1['index1'], y=df1['High1'])
#     df1 = df1.loc[df1['High1'] > reg[0] * df1['index1'] + reg[1]]
#
#   reg = linregress(x=df1['index1'], y=df1['High1'])
#   df0['high_trend'] = reg[0] * df0['index1'] + reg[1]
#   # 저점 추세선
#   df1 = df0.copy()
#   df1['Low1'] = np.where(df1['index1'] >= df_len-step, df['Low'].iloc[df_len-step], df['Low'])
#   # 트릭: 지정한 스텝 구간 저가를 직전 저가 수준으로 멈추게 함.
#
#   while len(df1) > 3:
#     reg = linregress(x=df1['index1'], y=df1['Low1'])
#     df1 = df1.loc[df1['Low1'] < reg[0] * df1['index1'] + reg[1]]
#
#   reg = linregress(x=df1['index1'], y=df1['Low1'])
#   df0['low_trend'] = reg[0] * df0['index1'] + reg[1]
#
#   plt.figure(figsize=(12.2, 6.5))
#   plt.plot(df0['Close'], label='TREND')
#   plt.plot(df0['high_trend'], linestyle='--', color='gray')
#   plt.plot(df0['low_trend'], linestyle='--', color='orange')
#   plt.show()
#
# my_trend('N', 'BTC/KRW', 300, 6)

import matplotlib.pyplot as plt
import FinanceDataReader as fdr
import datetime
import numpy as np
from scipy.stats import linregress
import pyupbit
import time

def my_trend(ticker, step=10):
  df = pyupbit.get_ohlcv(ticker, interval='week')
  df['index1'] = df.reset_index().index
  df0 = df.copy()
  df_len = len(df)
  # 고점 추세선
  df1 = df0.copy()
  df1['high1'] = np.where(df1['index1'] >= df_len-step, df['high'].iloc[df_len-step], df['high'])

  print(df1['high1'])
  # while len(df1) > 3:
  #   reg = linregress(x=df1['index1'], y=df1['high1'])
  #   df1 = df1.loc[df1['high1'] > reg[0] * df1['index1'] + reg[1]]
  #
  # reg = linregress(x=df1['index1'], y=df1['high1'])
  # df0['high_trend'] = reg[0] * df0['index1'] + reg[1]
  # # print(df0['high_trend'])
  # # 하락 추세선
  # df1 = df0.copy()
  # df1['low1'] = np.where(df1['index1'] >= df_len-step, df['low'].iloc[df_len-step], df['low'])
  #
  # while len(df1) > 3:
  #   reg = linregress(x=df1['index1'], y=df1['low1'])
  #   df1 = df1.loc[df1['low1'] < reg[0] * df1['index1'] + reg[1]]
  #
  # reg = linregress(x=df1['index1'], y=df1['low1'])
  # df0['low_trend'] = reg[0] * df0['index1'] + reg[1]
  # # print(df0['low_trend'])

  time.sleep(0.2)

tickers = pyupbit.get_tickers(fiat='KRW')

for ticker in tickers:
  is_my_trend = my_trend(ticker, 10)

  if is_my_trend:
    print('암호화폐: ', ticker, '상승추세')
    print('----------')
  else:
    print('암호화폐: ', ticker, '하락추세')
    print('----------')