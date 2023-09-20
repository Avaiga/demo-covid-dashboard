from taipy.gui import Markdown
import taipy as tp 
import pandas as pd

import datetime as dt

from config.config import scenario_cfg

selected_data_node = None
selected_scenario = None
selected_date = dt.datetime(2020,10,1)

scenario_country = "No selected scenario"

result = pd.DataFrame({"Date":[dt.datetime(2020,1,1)],
                       "Deaths_x":[0],"Deaths_y":[0],
                       "Predictions_x":[0],"Predictions_y":[0]})

def on_change_country_scenario(state):
    state['Country'].on_change_country_scenario(state)

    state.selected_scenario.country.write(state.selected_country)


predictions_md = Markdown("pages/predictions/predictions.md")