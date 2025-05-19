# Write tests that tests if data is available in the database

# (data_world, data_world_pie_absolute, data_world_pie_relative, data_world_evolution_absolute, data_world_evolution_relative
# ) = data_world()
#
# def test_data_world():     # Write tests that tests if data is available in the database

import pytest
import pandas as pd
import json
from data.data import PATH_TO_VACCINATION, PATH_TO_COUNTRIES, PATH_TO_DATA, get_data


def test_setup_data():
    data, vaccination, geojson = get_data(
        PATH_TO_DATA, PATH_TO_VACCINATION, PATH_TO_COUNTRIES
    )

    assert data is not None, "Data should be loaded successfully"
    assert not data.empty, "Data should not be empty"
    assert vaccination is not None, "Vaccination data should be loaded successfully"
    assert not vaccination.empty, "Vaccination data should not be empty"
    assert geojson is not None, "GeoJSON data should be loaded successfully"
    assert "features" in geojson, "GeoJSON should contain 'features' key"
    assert len(geojson["features"]) > 0, "GeoJSON should contain features"
