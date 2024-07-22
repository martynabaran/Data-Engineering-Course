import pandas as pd
import numpy as np
import json
import re
#import csvp
import pickle


#####EXERCISE 1 ####
file_name1 = "proj1_ex01.csv"
data1 = pd.read_csv(file_name1, header=0, sep=",")
array = []
for col in data1.columns:
    name = col
    missing_values = data1[col].isnull().sum() / len(data1[col])
    typ = data1[col].dtype.name
    array.append({"name": name, "missing": missing_values, "type": typ})

with open("proj1_ex01_fields.json", "w") as f:
    json.dump(array, f, indent=4)

####EXERCISE 2####
array2 = dict()

for col in data1.columns:
    array2[col] = data1[col].describe().to_dict()

with open("proj1_ex02_stats.json", "w") as f:
    json.dump(array2, f, indent=4)

####EXERCISE 3 ####


data2 = data1
col_names = {}
for col in data2.columns:
    new_col = re.sub(r'[^A-Za-z0-9_ ]', "", col)
    new_col = "_".join(new_col.split(" "))
    new_col = new_col.lower()
    col_names[col] = new_col

data1 = data1.rename(columns=col_names)
data1.to_csv("proj1_ex03_columns.csv", index=False)

####EXERCISE 4####


data1.to_excel("proj1_ex04_excel.xlsx", index=False)

data1.to_json("proj1_ex04_json.json", orient="records",indent=4)

data1.to_pickle("proj1_ex04_pickle.pkl")

###EXERCISE 5 ####
data_from_pickle = pd.read_pickle("proj1_ex05.pkl")
chosen_data = data_from_pickle[data_from_pickle.columns[1:3]]
filtered_data = chosen_data[chosen_data.index.str.startswith('v')]

filtered_data = filtered_data.fillna('')
filtered_data.to_markdown("proj1_ex05_table.md")

#### EXERCISE 6 ####
with open("proj1_ex06.json") as f:
    nested_data = json.load(f)

normalized_data = pd.json_normalize(nested_data)

normalized_data.to_pickle("proj1_ex06_pickle.pkl")