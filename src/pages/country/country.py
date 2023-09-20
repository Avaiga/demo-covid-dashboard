import numpy as np
import pandas as pd

from taipy.gui import Markdown

from data.data import data

selected_country = 'France'
data_country_date = None

representation_selector = ['Cumulative', 'Density']
selected_representation = representation_selector[0]

layout = {'barmode':'stack', "hovermode":"x"}
options = {"unselected":{"marker":{"opacity":0.5}}}


def initialize_case_evolution(data, selected_country='France'):
    # Aggregation of the dataframe to erase the regions that will not be used here
    data_country_date = data.groupby(["Country/Region",'Date'])\
                            .sum()\
                            .reset_index()
    
    # a country is selected, here France by default
    data_country_date = data_country_date.loc[data_country_date['Country/Region']==selected_country]
    return data_country_date

data_country_date = initialize_case_evolution(data)
pie_chart = pd.DataFrame({"labels": ["Deaths", "Recovered", "Confirmed"],"values": [data_country_date.iloc[-1, 6], data_country_date.iloc[-1, 5], data_country_date.iloc[-1, 4]]})



def convert_density(state):
    if state.selected_representation == 'Density':
        df_temp = state.data_country_date.copy()
        df_temp['Deaths'] = df_temp['Deaths'].diff().fillna(0)
        df_temp['Recovered'] = df_temp['Recovered'].diff().fillna(0)
        df_temp['Confirmed'] = df_temp['Confirmed'].diff().fillna(0)
        state.data_country_date = df_temp
    else:
        state.data_country_date = initialize_case_evolution(data, state.selected_country)

def on_change_country(state):
    # state contains all the Gui variables and this is through this state variable that we can update the Gui
    # state.selected_country, state.data_country_date, ...
    # update data_country_date with the right country (use initialize_case_evolution)
    print("Chosen country: ", state.selected_country)
    state.data_country_date = initialize_case_evolution(data, state.selected_country)
    state.pie_chart = pd.DataFrame({"labels": ["Deaths", "Recovered", "Confirmed"],
                                    "values": [state.data_country_date.iloc[-1, 6], state.data_country_date.iloc[-1, 5], state.data_country_date.iloc[-1, 4]]})
    
    convert_density(state)


country_md = Markdown("pages/country/country.md")
