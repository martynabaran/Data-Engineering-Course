#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import re
import pickle


# In[3]:


with open('proj2_data.csv', 'r') as file:
    for line in file:
        if re.search(r'\d+\.\d+', line):
            first_line = line
            break
    else:
        raise ValueError("No line with floating-point numbers found in the file")


separator_pattern = r'[|;,]'


match = re.search(separator_pattern, first_line)
if match:
    separator = match.group()
else:
    raise ValueError("Separator not found in the first line of the file")

if separator==',':
    decimal_separator='.'
else:
    decimal_separator_pattern = r'[.,]'
    decimal_match = re.search(decimal_separator_pattern, first_line)
    if decimal_match:
        decimal_separator = decimal_match.group()
    else:
        raise ValueError("Decimal separator not found in the first line of the file")


initial_df = pd.read_csv("proj2_data.csv", sep=separator, decimal=decimal_separator)

#print(f"Initial df: {initial_df}")

initial_df.to_pickle("proj2_ex01.pkl")




names = {}
i=1
with open('proj2_scale.txt', 'r') as f:
    for line in f:
        names[line.strip()] = i
        i+=1
df = initial_df.copy()
columns = [col for col in df.columns if df[col].isin(names.keys()).any()]

for col in columns:
    df[col] = df[col].map(names)
#print(f"zadanie 2 {df}")
df.to_pickle("proj2_ex02.pkl")


# In[6]:


df2 = initial_df.copy()
for column in columns:
    df2[column] = pd.Categorical(df2[column], categories=names.keys())

# Save the resulting DataFrame to proj2_ex03.pkl
#print(f"Zadanie 3: {df2}")
df2.to_pickle('proj2_ex03.pkl')



non_numeric_data = initial_df.select_dtypes(exclude=np.number)
def contains_number(text):
    pattern = r'[-+]?\d*[\.,]?\d+'
    match = re.search(pattern, str(text))
    if match:
        return float(match.group().replace(",", "."))
    else:
        return None

df_4 = pd.DataFrame()
for col in non_numeric_data:
    df_4[col] = non_numeric_data[col].apply(contains_number)

df_4 = df_4.dropna(axis=1, how='all')

df_4.to_pickle('proj2_ex04.pkl')




chosen = initial_df.select_dtypes(exclude=np.number)
columns5 =[]
for col in chosen:
    if len(chosen[col].unique()) <10 and chosen[col].apply(lambda x: re.match("[a-z]",x)).notnull().all() and not chosen[col].isin(names).all():
        columns5.append(col)
#print(f'columns: {columns5}')


# In[39]:

index = 1
for col in columns5:
    data = pd.get_dummies(initial_df[col].copy(), prefix="", prefix_sep="", columns=[col])
    data.to_pickle(f'proj2_ex05_{index}.pkl')
    index+=1
    #print(data)






