import pandas as pd
import json


PATH_TO_DATA = "data/covid-19-all.csv"
PATH_TO_VACCINATION = "data/vaccination-data.csv"
PATH_TO_COUNTRIES = "data/countries.geojson"


def get_data(path_to_data, path_to_vaccination, path_to_countries):
    data = pd.read_csv(path_to_data, low_memory=False)
    vaccination = pd.read_csv(path_to_vaccination)
    with open(path_to_countries) as f:
        geojson = json.load(f)
    return data, vaccination, geojson


data, vaccination, geojson = get_data(
    PATH_TO_DATA, PATH_TO_VACCINATION, PATH_TO_COUNTRIES
)
