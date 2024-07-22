######### Exercise 1 ##############
import json

import pandas as pd
import numpy as np
data = []
for i in range(1,4):
    f = open(f"proj3_data{i}.json")
    data.append(pd.DataFrame.from_dict(json.load(f), orient='columns'))

data = pd.concat(data, ignore_index=True)
#print(data)
#df1 = pd.DataFrame.from_dict()

########## ZADANIE2 ############

missing_val = [f"{col},{data[col].isna().sum()}" for col in data.columns if data[col].isna().sum() >0]
#print(missing_val)

######## ZADANIE 3 #############
data3 = data.copy()
with open("proj3_params.json") as f:
    requirements = json.load(f)

#print(requirements)

ex3_req = requirements['concat_columns']


def ex3_fun(row, required_columns):
    desc =""
    for i in range(len(required_columns)):
        desc+=f"{row[ex3_req[i]]}"
        if i!= len(ex3_req)-1:
            desc+=" "
    return desc

data3["description"] = data3.apply(lambda row: ex3_fun(row, ex3_req), axis=1)

#print(data3)

############ ZADANIE 4 #########

with open("proj3_more_data.json") as f:
    more_data = pd.DataFrame.from_dict(json.load(f))

#print(more_data)
ex4_req = requirements["join_column"]
#print(ex4_req)
data4 = pd.merge(data3, more_data, on=ex4_req, how='outer')

######### ZADANIE 5 ###############
data5 = data4.drop('description', axis=1)
names = [f'proj3_ex_05_{d.lower().replace(" ", "_")}.json' for d in data4['description']]

#print(desc)
i=0
for count, row in data5.iterrows():
    #with open(names[i], 'w') as json_file:
        #json.dump(row.to_dict(), json_file, indent=4)
    i+=1


req5 = requirements['int_columns']
di = {}

def toInt(c):
    return int(c)

print(req5)
data6 = data5.fillna(0)
data7 = pd.DataFrame()
for id, col in enumerate(data6.columns):
    if col in req5:
        data7[col] = data6[col].apply(toInt)
    else:
        data7[col]= data6[col]

names2 = [f'proj3_ex_05_int_{d.lower().replace(" ", "_")}.json' for d in data4['description']]
i=0
for count, row in data5.iterrows():
    #with open(names2[i], 'w') as json_file:
        #json.dump(row.to_dict(), json_file, indent=4)
    i+=1


############# ZADANIE 6
req6 = requirements['aggregations']
#print(req6)

answer_to_6 = {}
for item in req6:
    col_name, func = item
    answer_to_6[f'{func}_{col_name}'] = data4[col_name].agg(func)
#print(answer_to_6)
########## zrob plik json!!!!!!!!!!!!!!!!!!!!!!!!!!


########ZADANIE 7
req7 = requirements['grouping_column']
print(data4.groupby(req7))