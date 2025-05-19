import pandas as pd
import numpy as np
import pytest
from taipy.gui import Gui
from taipy.gui.mock.mock_state import MockState


from pages.map.map import initialize_map, on_change

# ---- Fixtures ----


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "Country/Region": ["US", "US", "IT"],
            "Province/State": [None, "California", "Lombardy"],
            "Longitude": [-120.0, -118.0, 9.0],
            "Latitude": [37.0, 36.0, 45.0],
            "Deaths": [50, 200, 30],
        }
    )


@pytest.fixture
def mock_vaccination():
    return pd.DataFrame(
        {
            "COUNTRY": ["US", "IT"],
            "Total_First_Vaccination": [1000000, 800000],
            "Rate_First_Vaccination": [65.0, 50.0],
        }
    ).set_index("COUNTRY")


@pytest.fixture
def mock_state(mock_data, mock_vaccination):
    Gui("")  # Required to register MockState
    return MockState(
        Gui(""),
        data_province_displayed=initialize_map(mock_data.copy()),
        vaccination=mock_vaccination,
        sum_deaths=0,
        mean_rate_of_vaccination=0,
        sum_vaccination=0,
    )


# ---- Tests ----


def test_initialize_map_filters_and_scales(mock_data):
    result = initialize_map(mock_data.copy())
    assert not result.empty
    assert "Size" in result.columns
    assert (result["Deaths"] > 10).all()


def test_on_change_country_selection(mock_state):
    # simulate user selecting "US"
    on_change(mock_state, "countries_selected", [["US"]])
    assert mock_state.mean_rate_of_vaccination == 65.0
    assert mock_state.sum_vaccination == 1000000


def test_on_change_empty_country_selection(mock_state):
    on_change(mock_state, "countries_selected", [])
    assert mock_state.mean_rate_of_vaccination == np.mean(
        mock_state.vaccination["Rate_First_Vaccination"]
    )
    assert (
        mock_state.sum_vaccination
        == mock_state.vaccination["Total_First_Vaccination"].sum()
    )


def test_on_change_cluster_selection(mock_state):
    # Get valid index for selected clusters

    selected_indexes = mock_state.data_province_displayed.index[:2].tolist()
    selected = [selected_indexes]
    on_change(mock_state, "cluster_selected", selected)
    expected_sum = mock_state.data_province_displayed.loc[
        selected_indexes, "Deaths"
    ].sum()
    assert mock_state.sum_deaths == expected_sum


def test_on_change_empty_cluster_selection(mock_state):
    on_change(mock_state, "cluster_selected", [])
    expected_sum = mock_state.data_province_displayed["Deaths"].sum()
    assert mock_state.sum_deaths == expected_sum
