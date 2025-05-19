# test_maps.py

import pytest
import pandas as pd
from pages.map.charts import create_choropleth_mapbox, create_cluster_map

# Replace 'your_module' with the actual name of the Python file containing your map functions.


def test_create_choropleth_mapbox_with_none():
    result = create_choropleth_mapbox(None)
    assert result is None


def test_create_choropleth_mapbox_with_empty_df():
    empty_df = pd.DataFrame()
    result = create_choropleth_mapbox(empty_df)
    assert result is None


def test_create_cluster_map_with_none():
    result = create_cluster_map(None)
    assert result is None


def test_create_cluster_map_with_empty_df():
    empty_df = pd.DataFrame()
    result = create_cluster_map(empty_df)
    assert result is None
