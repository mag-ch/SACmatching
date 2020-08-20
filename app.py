''' FIELDS:
0 Email (str)
1 Name (first last)
2 Location (str)
3 Does location matter? (bool)
4 Familiar cuisines (str list)
5 Learn cuisines (str list)
6 Comm platform (str)
'''
import pandas as pd
from difflib import SequenceMatcher
import numpy as np
import itertools
from fuzzywuzzy import process, fuzz
from pprint import pprint

data = pd.read_csv("responses.csv")
# data = data.head(10)

# person1 = ["johndoe@gmail.com", "John Doe", "New York", False, [1, 2, 9, 8, 6], [7, 2, 6, 0, 8], "Discord"]
# person2 = ["janesmith@gmail.com", "Jane Smith", "France", True, [7, 2, 0, 8, 6], [1], "Skype"]
# person3 = ["jerry@gmail.com", "Jerry Singh", "Boston", False, [7, 2, 0, 8, 6], [1, 2, 6, 7], "Discord"]
# person4 = ["jocho@gmail.com", "Joe Cho", "Paris, France", True, [7, 2, 0, 8, 6], [1], "Skype"]
# person5 = ["maggiec@gmail.com", "Maggie Chang", "Boston, USA", True, [2, 7, 4], [1, 0, 6, 7, 1], "Slack"]
#
# data = [person5, person1, person2, person3, person4]


# Takes in two people and returns a decimal representing physical proximity
# If both people don't factor in location, return None
# Both people must value location equally
def location_compat(person1, person2):
    def to_bool(st):
        if st == "No":
            return False
        else:
            return True

    loc1 = to_bool(person1[4])
    loc2 = to_bool(person2[4])

    if loc1 and loc2:
        # insert fuzzy string matching OR geographical comparison package
        location1 = person1[3]
        location2 = person2[3]
        match_ratio = fuzz.token_set_ratio(location1,location2) / 100
        return match_ratio
    elif loc1 or loc2:
        return .25
    else:
        return 1


def cuisine_compat(person1, person2):

    def list_process(str_cuisines):
        if isinstance(str_cuisines, float):
            return []
        else:
            return str_cuisines.split(', ')

    def similarity(l1, l2):
        if l1 == l2:
            return 1
        return len(set(l1) & set(l2)) / float(len(set(l1) | set(l2)))

    familiar_cuisines1 = list_process(person1[5])
    learn_cuisines1 = list_process(person1[6])
    familiar_cuisines2 = list_process(person2[5])
    learn_cuisines2 = list_process(person2[6])
    # similarity = lambda x: np.mean([SequenceMatcher(None, a, b).ratio() for a, b in itertools.combinations(x, 2)])
    return (similarity(familiar_cuisines1, learn_cuisines2) + similarity(familiar_cuisines2, learn_cuisines1)) / 2

def comm_platform_compat(person1, person2):
    if person1[7] == person2[7]:
        return 1.0
    else:
        return 0.0

matches = []
threshold = .9
while not data.empty:
    temp = len(data)
    for i, row1 in data.iterrows():
        for indx, row2 in data.iterrows():
            pair = []
            if not i <= indx:
                # potentially weigh certain fields more heavily than others
                def weights(x):
                    return {
                        'location': 0.8,
                        'cuisine': 0.1,
                        'communication': 0.1
                        }.get(x)
                print("\n\n", row1[2], row2[2])
                loc = float(location_compat(row1, row2)) * weights("location")
                com = comm_platform_compat(row1, row2) * weights("communication")
                cui = cuisine_compat(row1, row2) * weights("cuisine")
                compatibility = (loc + com + cui)
                if compatibility > threshold:
                    print("location: ", loc)
                    print("cuisine: ", cui)
                    print("communication: ", com)
                    print("COMPAT: ",compatibility)
                    # matches.append([row1[2], row2[2]])
                    pair.append([row1[2], row2[2]])
                    pair.append([row1[3], row2[3]])
                    pair.append([row1[4], row2[4]])
                    pair.append([row1[5], row2[6]])
                    pair.append([row1[6], row2[5]])
                    pair.append([row1[7], row2[7]])
                    matches.append(pair)
                    data.drop([i,indx], inplace=True)
                    break
                print(len(data))
                if len(data) == 1:
                    break

    if len(data) == temp:
        threshold = threshold - 0.05
    elif len(data) == 1:
        break


for i in matches:
    print("\n")
    for j in i:
        print("\n", j)