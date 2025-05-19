import pandas as pd
import pytest
from taipy.gui import Gui
from taipy.gui.mock.mock_state import MockState

from pages.country.country import (
    initialize_case_evolution,
    convert_density,
    on_change_country,
    get_vaccination_stats,
)

# ---- Fixtures ----


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "Country/Region": ["France"] * 3 + ["Italy"] * 3 + ["Germany"] * 3,
            "Province/State": [None] * 3 + ["Lombardy"] * 3 + [None] * 3,
            "Longitude": [2.3522] * 3 + [9.19] * 3 + [10.45] * 3,
            "Latitude": [48.8566] * 3 + [45.46] * 3 + [51.16] * 3,
            "Date": pd.date_range("2020-01-01", periods=3).tolist() * 3,
            "Confirmed": [1000, 2000, 3000, 500, 1500, 2500, 50, 100, 150],
            "Recovered": [100, 200, 300, 50, 150, 250, 5, 10, 15],
            "Deaths": [10, 20, 30, 5, 15, 25, 5, 10, 15],
        }
    )


@pytest.fixture
def mock_vaccination():
    return pd.DataFrame(
        {
            "COUNTRY": ["France", "Italy"],
            "Total_First_Vaccination": [1000000, 200000],
            "Rate_First_Vaccination": [70, 50],
        }
    )


# ---- Tests ----


def test_initialize_case_evolution(mock_data):
    result = initialize_case_evolution(mock_data, selected_country="France")
    assert not result.empty
    assert (result["Country/Region"] == "France").all()


def test_convert_density_density(mock_data):
    ms = MockState(
        Gui(""),
        selected_country="France",
        selected_representation="Density",
        data_country_date=initialize_case_evolution(mock_data, "France"),
    )

    convert_density(ms)

    # Check that columns have been differenced
    assert ms.data_country_date["Deaths"].iloc[0] == 0
    assert len(ms.data_country_date) == 3


def test_convert_density_cumulative(mock_data):
    ms = MockState(
        Gui(""),
        selected_country="France",
        selected_representation="Cumulative",
        data_country_date=None,
    )

    convert_density(ms)
    assert ms.data_country_date is not None
    assert (ms.data_country_date["Country/Region"] == "France").all()


def test_on_change_country_sets_state(mock_data, mock_vaccination):
    ms = MockState(
        Gui(""),
        selected_country="France",
        data_country_date=None,
        pie_chart=None,
        rate_first_vaccination=0,
        total_first_vaccination=0,
    )

    # Monkeypatch global `data` and `vaccination`
    import pages.country.country as country_module

    country_module.data = mock_data
    country_module.vaccination = mock_vaccination

    on_change_country(ms)

    assert isinstance(ms.data_country_date, pd.DataFrame)
    assert not ms.pie_chart.empty
    assert ms.rate_first_vaccination == 70
    assert ms.total_first_vaccination == 1000000


def test_get_vaccination_stats_found(mock_vaccination):
    stats = get_vaccination_stats(mock_vaccination, "France")
    assert stats["Rate_First_Vaccination"] == 70


def test_get_vaccination_stats_not_found(mock_vaccination):
    stats = get_vaccination_stats(mock_vaccination, "Germany")
    assert stats == {"Total_First_Vaccination": 0, "Rate_First_Vaccination": 0}
