import pandas as pd
import json 


path_to_data = "data/covid-19-all.csv"
data = pd.read_csv(path_to_data, low_memory=False)

vaccination = pd.read_csv("data/vaccination-data.csv")

with open("data/countries.geojson") as f:
    geojson = json.load(f)
