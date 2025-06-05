#!/usr/bin/env python
# coding: utf-8

# In[40]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
df = pd.read_csv("shared_df.csv")


# In[48]:


def scraper(STOCK):
    
    # Define URL of the Webpage
    url = f'https://finance.yahoo.com/quote/{STOCK}/history/?period1=1661261400&period2=1740099783&filter=history'
    
    
    # Define the URL and headers to avoid bot detection
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Fetch the webpage content
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the table (Yahoo Finance uses tables for historical data)
    table = soup.find("table")  # First table on the page
    
    # Extract headers
    headers = [th.text.strip() for th in table.find("thead").find_all("th")]
    
    # Extract rows
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = [td.text.strip() for td in tr.find_all("td")]
        if len(cols) == len(headers):  # Ensure it matches the number of columns in headers
            rows.append(cols)
    
    # Ensure DataFrame is created only if rows exist
    if rows:
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Clean up and drop rows with missing values
        df.dropna(inplace=True)
        
        # Keep only the first two columns (Date and Open)
        df = df.iloc[:, :2]
        
        # Optionally, save to CSV
        df.to_csv(f"{os.getcwd()}/{STOCK}.csv", index=False)
    else:
        print(f"No valid data found for {STOCK}. Skipping.")


# In[49]:


for i in range(len(df)):
    Stock = df.iloc[i, 0].replace(" ", "")
    scraper(Stock)

