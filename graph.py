import csv
import pandas as pd

data = pd.read_csv("responses.csv")
user_graph = dict.fromkeys(data['Email address'], set())
def edge_overlap_cuisine(row_1, row_2):
    return True
def edge_overlap_teach(row_1, row_2):
    if (type(row_1[5]) == float or type(row_2[5]) == float) or (type(row_1[6]) == float or type(row_2[6]) == float):
        return False
    teach_1 = set(row_1[5].split(','))
    teach_2 = set(row_2[5].split(','))
    learn_1 = set(row_1[6].split(','))
    learn_2 = set(row_2[6].split(','))
    return len(teach_1.intersection(learn_2)) > 0 or len(teach_2.intersection(learn_1)) > 0 
    
for i, row_1 in data.iterrows():
    for indx, row_2 in data.iterrows():
        if edge_overlap_teach(row_1, row_2):
            user_graph[row_1['Email address']].add(row_2['Email address'])
            user_graph[row_2['Email address']].add(row_1['Email address'])

print(user_graph)
