#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import csv
import pandas as pd
import pickle
import os
with open(f"{os.getcwd()}/number_of_stocks.pkl", "rb") as f:
    number_of_stocks= pickle.load(f)
df = pd.read_csv("shared_df.csv")

first_price=pd.DataFrame()
for i in range(number_of_stocks):
    ticker = df.iloc[i, 0].strip()
    url = (
        f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        "?period1=1661261400&period2=1740099783&interval=1d"
    )
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
    
    # Extract the first closing price and check for a successful response
    if (
        not resp.get("chart") 
        or not resp["chart"].get("result") 
        or resp["chart"]["result"] is None
    ):
        print(f"⚠️ Skipping {ticker} — no valid chart data.")
        continue  # Skip this ticker and move to the next one
    try:
        close_prices = resp["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    except (IndexError, KeyError, TypeError) as e:
        continue
    first_price[f"{ticker}"] = close_prices


df = pd.DataFrame(list(first_price.columns), columns=["Symbol"])
df.to_csv("shared_df.csv", index=False)

for ticker, prices in first_price.items():
    filename = f"{ticker}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Close Price"])
        # Write each price on its own row
        for price in prices:
            writer.writerow([price])
