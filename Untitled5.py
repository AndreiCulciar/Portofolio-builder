#!/usr/bin/env python
# coding: utf-8

# In[12]:


b=list()


# In[13]:


import requests
import csv
import pandas as pd
import os
df = pd.read_csv("shared_df.csv")
val=pd.read_csv("valori_test.csv")
val3=pd.read_csv("portfolio_allocations.csv")   
first_price=pd.DataFrame()
for i in range(len(df)):
    ticker = df.iloc[i, 0].strip()
    url = (
        f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        "?err=1&period1=1752439165&period2=1752525462"
    )
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
    
    # Extract the first closing price
    close_prices = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    first_price[f"{ticker}"] = close_prices

val2=first_price.iloc[-1]
 
for i in range(len(val.columns)):
    old_val = val.iloc[0,i]
    new_val = val2.iloc[i]
    change = (new_val / old_val - 1) * 100
    all_val=val3.iloc[i,0]/val3["Allocation (%)"].abs().sum()*100
    print(f"{val2.index[i]}: {change:.2f}% {all_val:.2f}% Old: {old_val:.2f} → New: {new_val:.2f}")

for i in val3:
    print(i)
# if os.path.exists("valori_test.csv"):
#     os.remove("valori_test.csv")


# In[14]:


a=list()
for i in range(len(val.columns)):
    change = (val2.iloc[i] / val.iloc[0,i] - 1) * 100  
    all_val=val3.iloc[i,0]/val3["Allocation (%)"].abs().sum()*100
    if(change>0):
        a.append(abs(all_val)*(1+change/100))
    else:
        a.append(abs(all_val)*(1-change/100))
b.append(sum(a))


# In[15]:


b


# In[17]:


import pickle
with open(f"{os.getcwd()}/b.pkl", "wb") as f:
    pickle.dump(b, f)


# In[ ]:




