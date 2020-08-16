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

data = pd.read_csv("excel sheet.csv")


# Takes in two people and returns a decimal representing physical proximity
# If both people don't factor in location, return None
# If ONE factors in location, return arbitrary decimal
def location_compat(person1, person2):
    if person1[3] and person2[3]:
        # insert fuzzy string matching OR geographical comparison package
        # location1: person1[2]
        # location2: person2[2]
        pass
    elif person2[3] or person1[3]:
        return .25
    else:
        return None


def cuisine_compat(person1, person2):
    familiar_cuisines1 = person1[4]
    learn_cuisines1 = person1[5]
    familiar_cuisines2 = person2[4]
    learn_cuisines2 = person2[5]
    pass


def comm_platform_compat(person1, person2):
    if person1[6] == person2[6]:
        return 1.0
    else:
        return 0.0


for row1 in data.iterrows():
    person1 = row1
    for row2 in data.iterrows():
        person2 = row2

        # potentially weigh certain fields more heavily than others
        def weights(x):
            return {
                'location': 0.2,
                'cuisine': 0.7,
                'communication': 0.1
                }.get(x)

        location_compat()
        cuisine_compat()
        comm_platform_compat(person1, person2)
    