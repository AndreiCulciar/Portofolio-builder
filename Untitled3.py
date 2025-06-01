#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
df = pd.read_csv("shared_df.csv")
inputs=0.002
global q, a
a=[]
# In[2]:


def pregatire(a):
    for name in a:
        globals()[name] = pd.read_csv(f"C:/Users/andre/Proiect stocuri/{name}.csv")
        globals()[name].rename(columns={"Open": f"{name}"}, inplace=True)
    dataframes = [globals()[name] for name in a]
    merged = pd.concat(dataframes, axis=1)
    merged.drop(columns=['Date'], inplace=True)
    merged_df=merged.iloc[::-1].reset_index(drop=True)
    return merged_df


# In[5]:



for i in range(len(df)):
    a.append(df.iloc[i, 0].replace(" ", ""))

merged_df=pregatire(a)
merged_df = merged_df.replace(',', '', regex=True)
merged_df = merged_df.apply(pd.to_numeric, errors='coerce')
merged_df = merged_df.dropna(thresh=len(merged_df), axis=1)


# In[7]:


def find_non_numeric_locations(df):
    
    # Convert the DataFrame to numeric, turning non-numeric values to NaN
    non_numeric_df = df.apply(pd.to_numeric, errors='coerce')

    # Find the locations of NaN values (non-numeric)
    non_numeric_locations = non_numeric_df.isna()

    # Stack the DataFrame to get non-numeric locations (True values)
    non_numeric_indices = non_numeric_locations.stack()

    # Check if there are any non-numeric values
    if non_numeric_indices.any():
        # Get the row and column indices of non-numeric values (True locations)
        rows, cols = zip(*non_numeric_indices[non_numeric_indices].index)
        return list(rows), list(cols)
    else:
        # If no non-numeric values are found, return empty lists
        return [], []


# In[8]:


# Call the function and print the result
rows, cols = find_non_numeric_locations(merged_df)
print(merged_df)

# In[9]:


def Frontiera_Eficienta(merged_df,a):
    
    #Standardizare
    ln_merged_df=np.log(merged_df)
    
    #Medii
    Medii_EI = pd.DataFrame()
    Medii_EI=ln_merged_df.mean()
    
    #Abaterii
    Sigma_i = pd.DataFrame()
    Sigma_i=ln_merged_df.std()
    
    #Sigma (tabel var cov)
    Sigma=ln_merged_df.cov()
    
    #Omega
    e=[1] * len(merged_df.columns)
    R=Medii_EI
    Omega=2*Sigma
    Omega['R']=R
    Omega['e']=e
    Omega.loc['R', :] = Omega['R']
    Omega.loc['e', :] = Omega['e']
    Omega.fillna(0, inplace=True)
    
    #OMEGA^(-1)
    Omega_1=np.linalg.inv(Omega)
    
    #K
    K=[0] * len(merged_df.columns) + [a, 1]
    K = np.array(K, dtype=np.float64)
    
    
    #Sigma^(-1)
    Sigma_1=np.linalg.inv(Sigma)

    #e_tr*sigma
    E_tr = np.ones((1, len(merged_df.columns)))
    E_tr2=np.ones((len(merged_df.columns), 1))
    ESigma= np.dot(E_tr,Sigma_1)

    #Structura portofoliu
    X=np.dot(Omega_1, K)
    return X


# In[10]:
q = Frontiera_Eficienta(merged_df, inputs)


q = q[:-2]

with open("C:/Users/andre/Proiect stocuri/q.pkl", "wb") as f:
    pickle.dump(q, f)
with open("C:/Users/andre/Proiect stocuri/a.pkl", "wb") as f:
    pickle.dump(a, f)

