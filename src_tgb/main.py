from taipy.gui import Gui
import taipy as tp

from pages.country.country import country_page, country_on_init
from pages.world.world import *
from pages.map.map import map_page
from pages.predictions.predictions import predictions_page, selected_scenario
from pages.root import root, selected_country, selector_country
from utils import to_text

from config.config import Config


pages = {
    "/": root,
    "Country": country_page,
    "World": world_page,
    "Map": map_page,
    "Predictions": predictions_page,
}


def on_init(state):
    country_on_init(state)


if __name__ == "__main__":
    gui_multi_pages = Gui(pages=pages)

    tp.Core().run()

    gui_multi_pages.run(title="Covid Dashboard", margin="0px")
