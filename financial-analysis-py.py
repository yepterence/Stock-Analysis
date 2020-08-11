import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import sklearn 
import datetime as dt
import pandas_datareader.data as web
import bs4 as bs
import pickle
import requests as req

style.use('ggplot')
start_date = input()
start = dt.datetime(2015,1,1)
end = dt.datetime(2020,8,1)
# Historical data of a single stock
df = web.DataReader('SHOP','yahoo',start,end)
print (df.tail(6))

df['Adj Close'].plot()










