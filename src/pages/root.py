from taipy.gui import Markdown 

import numpy as np

from data.data import data

selector_country = list(np.sort(data['Country/Region'].astype(str).unique()))
selected_country = 'France'

def to_text(val):
    try:
        return '{:,}'.format(int(val)).replace(',', ' ')
    except:
        print("Error trying to format value: ", val)
        if val:
            return val
        else:
            return 'No information'

root = Markdown("pages/root.md")