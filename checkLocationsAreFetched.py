import pandas as pd
import json

user_data = pd.read_csv("responses_clean_locations.csv")
locationStrings = user_data.iloc[:, 3].tolist()
with open('locationData.json') as json_file:
    location_data = json.load(json_file)
    for locationString in locationStrings:
        if not locationString in location_data:
            print(locationString)
