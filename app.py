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

# data = pd.read_csv("excel sheet.csv")

person1 = ["johndoe@gmail.com", "John Doe", "New York", False, [1, 2, 9, 8, 6], [7, 2, 6, 0, 8], "Discord"]
person2 = ["janesmith@gmail.com", "Jane Smith", "France", True, [7, 2, 0, 8, 6], [1], "Skype"]
person3 = ["jerry@gmail.com", "Jerry Singh", "Boston", False, [7, 2, 0, 8, 6], [1, 2, 6, 7], "Discord"]
person4 = ["jocho@gmail.com", "Joe Cho", "Paris, France", True, [7, 2, 0, 8, 6], [1], "Skype"]

data = [person1, person2, person3, person4]


# Takes in two people and returns a decimal representing physical proximity
# If both people don't factor in location, return None
# Both people must value location equally
def location_compat(person1, person2):
    if person1[3] != person2[3]:
        return 0
    if person1[3] and person2[3]:
        # insert fuzzy string matching OR geographical comparison package
        location1 = person1[2]
        location2 = person2[2]
        match_ratio = fuzz.token_set_ratio(location1,location2) / 100
        return match_ratio
    elif person2[3] or person1[3]:
        return .25
    else:
        return 1


def cuisine_compat(person1, person2):
    familiar_cuisines1 = person1[4]
    learn_cuisines1 = person1[5]
    familiar_cuisines2 = person2[4]
    learn_cuisines2 = person2[5]

    def similarity(l1, l2):
        return len(set(l1) & set(l2)) / float(len(set(l1) | set(l2)))

    # similarity = lambda x: np.mean([SequenceMatcher(None, a, b).ratio() for a, b in itertools.combinations(x, 2)])
    # print((similarity(familiar_cuisines1, learn_cuisines2) + similarity(familiar_cuisines2, learn_cuisines1)) / 2)
    return (similarity(familiar_cuisines1, learn_cuisines2) + similarity(familiar_cuisines2, learn_cuisines1)) / 2

def comm_platform_compat(person1, person2):
    if person1[6] == person2[6]:
        return 1.0
    else:
        return 0.0

matches = []
threshold = .9
while data:
    temp = len(data)
    for row1 in data:
        person1 = row1
        for row2 in data:
            if not row1 == row2:
                # potentially weigh certain fields more heavily than others
                def weights(x):
                    return {
                        'location': 0.2,
                        'cuisine': 0.7,
                        'communication': 0.1
                        }.get(x)
                print("\n\n", row1[1], row2[1])
                loc = float(location_compat(row1, row2))
                com = comm_platform_compat(row1, row2)
                cui = cuisine_compat(row1, row2)
                print(loc)
                print(com)
                print(cui)
                compatibility = (loc + com + cui) / 3
                print(compatibility)
                if compatibility > threshold:
                    data.remove(row1)
                    data.remove(row2)
                    matches.append([row1[1], row2[1]])
                print(threshold, data)
        if len(data) == temp:
            threshold = threshold - 0.05

print("MATCHES: ", matches)