#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import runpy


# In[33]:


def Lista_stocuri():
    url = 'https://finance.yahoo.com/markets/stocks/most-active/?start=0&count=25'
    print("Generated URL:", url)
# Define the URL and headers
    headers = {"User-Agent": "Mozilla/5.0"}  # Helps bypass bot detection
    
    # Fetch the webpage content
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        exit()
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the table (Yahoo Finance uses tables for historical data)
    table = soup.find("table")  # First table on the page
    
    # Extract headers
    headers = [th.text for th in table.find("thead").find_all("th")]
    
    # Extract rows
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = [td.text for td in tr.find_all("td")]
        if cols:  # Ensure it's not an empty row
            rows.append(cols)
    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=headers)
    df=df[[df.columns[0]]]
    return df
df=Lista_stocuri()


# In[34]:


df.to_csv("shared_df.csv", index=False)

