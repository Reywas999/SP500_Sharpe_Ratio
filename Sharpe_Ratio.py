#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


# In[35]:


stock = pd.read_csv("S&P500.csv")


# In[36]:


stock_List = stock['Symbol'].tolist()


# In[28]:


SD = input("Enter the Start Date YYYY-MM-DD: ")
ED = input("Enter the End Date YYYY-MM-DD: ")


# In[ ]:





# In[24]:


def normalize_data(df):
    '''Normalizes datasets by dividing all values by the first'''
    return df/df.iloc[0, :]


# In[25]:


def work():
    '''Pulls and cleans data for the input list ticker symbols using yahoo finance adjusted close data'''
    Tickers = stock_List
    
    if 'SPY' not in Tickers: #Uses SPY as a reference, this is unnecessary
        Tickers.insert(0, 'SPY')
    
    #pulls data from yahoo finance and makes a table with ALL ticker data for your specified dates
    data = yf.download(Tickers, start = SD, end = ED)

    #Removes all columns aside from the Adjusted Close data
    data = data[["Adj Close"]]
    
    data_n1 = normalize_data(data)

    data_ns1 = data_n1.sort_values(data_n1.last_valid_index(), axis=1)
    
    data_nss1 = data_ns1.dropna(axis='columns', how ='all')

    data_nss1.columns = ['{}'.format(x[1]) for x in data_nss1.columns]

    return(data_nss1)


# In[ ]:





# In[34]:


def spyy():
    #pulls data from yahoo finance and makes a table with ALL ticker data for your specified dates
    data = yf.download("SPY", start = SD, end = ED)

    #Removes all columns aside from the Adjusted Close data
    data = data[["Adj Close"]]
    
    data_n1 = normalize_data(data)

    data_ns1 = data_n1.sort_values(data_n1.last_valid_index(), axis=1)
    
    data_nss1 = data_ns1.dropna(axis='columns', how ='all')

    data_nss1.columns = ['{}'.format(x[1]) for x in data_nss1.columns]

    return(data_nss1)


# In[ ]:





# In[31]:


def spy_sharpe():
    dfport_a = spyy()
    c = dfport_a.columns
    col_list = c.tolist()
    dic = {}
    for i in col_list:
        Daily_Return = dfport_a[i].diff()/dfport_a[i]
        avg_daily_return = np.mean(Daily_Return)
        sd_daily_return = np.std(Daily_Return)
        SR1 = avg_daily_return/sd_daily_return
        SR2 = (252**0.5) * SR1
        dic[i] = SR2
    dic = dict(dic.items(), key=lambda item: item[1])
    return(dic)


# In[ ]:





# In[42]:


def sharpe():
    dfport_a = work()
    c = dfport_a.columns
    col_list = c.tolist()
    dic = {}
    for i in col_list:
        Daily_Return = dfport_a[i].diff()/dfport_a[i]
        avg_daily_return = np.mean(Daily_Return)
        sd_daily_return = np.std(Daily_Return)
        SR1 = avg_daily_return/sd_daily_return
        SR2 = (252**0.5) * SR1
        dic[i] = SR2
    dic = dict(sorted(dic.items(), key=lambda item: item[1]))
    print("-------------------------\n", "Ticker : Sharpe Ratio (annualized)", "\n-------------------------")
    s = spy_sharpe()
    print("Benchmark (SPY): ", s['d'])
    for i in dic:
        print(i, ":", dic[i])


# In[ ]:





# In[41]:


sharpe()

