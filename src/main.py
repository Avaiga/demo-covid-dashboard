import numpy as np

from taipy.gui import Gui
import taipy as tp

from pages.country.country import country_md, on_change_country,\
                          selected_representation, data_country_date, pie_chart
from pages.world.world import world_md
from pages.map.map import map_md
from pages.predictions.predictions import predictions_md, selected_scenario, result, scenario_country
from pages.root import root

from data.data import data

selector_country = list(np.sort(data['Country/Region'].astype(str).unique()))
selected_country = 'France'

pages = {
    '/':root,
    "Country":country_md,
    "World":world_md,
    "Map":map_md,
    "Predictions":predictions_md
}


gui_multi_pages = Gui(pages=pages)

if __name__ == '__main__':
    tp.Core().run()
    gui_multi_pages.run(title="Covid Dashboard",
    		            dark_mode=False,
                        use_reloader=False,
                        port=5039)