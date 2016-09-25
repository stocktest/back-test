#coding:utf-8
import  pandas as pd
import numpy as np

'''
验证了股社区用ma20对创业板指数的回测
http://www.imaibo.net/longweibo/detail/56eaa8e2cdef879f2b8b59b9
'''

data = pd.read_csv('./SZ#399006.csv',sep=',',encoding='gbk')
data.drop([u'开盘',u'最高',u'最低',u'成交量',u'成交额'],axis=1,inplace=True)
data['ma20'] = float('inf')
for tick in data[u'收盘'].index:
    if tick >= 19:
        data.at[tick,'ma20'] = data[u'收盘'][tick::-1][:20].sum()/20.0

#data['ma20'] = np.round(data['ma20'],2)
data = data.round({'ma20':2})
data[u'操作'] = 'NA'
for tick in data[u'操作'].index:
    if tick >= 19 and (data.at[tick,u'收盘'] > data.at[tick,'ma20']) and (data.at[tick-1,u'收盘'] < data.at[tick-1,'ma20']):
        data.at[tick,u'操作'] = 'buy'
        
    if tick >= 19 and (data.at[tick,u'收盘'] < data.at[tick,'ma20']) and (data.at[tick-1,u'收盘'] > data.at[tick-1,'ma20']):
        data.at[tick,u'操作'] = 'sell'

#data['ma20'] = data['ma20'].apply(lambda x:round(x,2))
data = data[data[u'操作'].isin(['buy','sell'])]
data[u'净值'] = 100.0
data.reset_index(inplace=True,drop=True)
for tick in data.index:
    print tick
    if 0!=tick and data.at[tick,u'操作'] == 'buy':
        data.at[tick,u'净值'] = data.at[tick-1,u'净值']  #buy等于上一次卖
    elif data.at[tick,u'操作'] == 'sell':
        data.at[tick,u'净值'] = data.at[tick-1,u'净值'] * (data.at[tick,u'收盘']/data.at[tick-1,u'收盘'])

data.to_csv('./ma20.csv',encoding='gbk')
