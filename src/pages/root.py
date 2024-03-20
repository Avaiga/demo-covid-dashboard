from taipy.gui import Markdown 

import numpy as np

from data.data import data

selector_country = list(np.sort(data['Country/Region'].astype(str).unique()))
selected_country = 'France'

def to_text(val):
    return '{:,}'.format(int(val)).replace(',', ' ')

root = Markdown("pages/root.md")