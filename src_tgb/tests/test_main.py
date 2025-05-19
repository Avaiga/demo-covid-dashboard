import pytest
from unittest.mock import patch, MagicMock
from taipy.gui import Gui
from taipy.gui.mock.mock_state import MockState
import pandas as pd
import main


def test_pages_dict_contains_all_expected_routes():
    assert "/" in main.pages
    assert "Country" in main.pages
    assert "World" in main.pages
    assert "Map" in main.pages
    assert "Predictions" in main.pages


def test_on_init_calls_country_on_init_with_cumulative():
    mock_state = MockState(
        Gui(""),
        selected_country="France",
        data_country_date=None,
        pie_chart=None,
        rate_first_vaccination=0,
        total_first_vaccination=0,
        selected_representation="Cumulative",
    )

    main.on_init(mock_state)

    assert mock_state.selected_country == "France"
    assert mock_state.data_country_date is not None
    assert mock_state.pie_chart is not None
    assert mock_state.rate_first_vaccination != 0
    assert mock_state.total_first_vaccination != 0
    assert isinstance(mock_state.pie_chart, pd.DataFrame)


def test_on_init_calls_country_on_init_with_density():
    mock_state = MockState(
        Gui(""),
        selected_country="France",
        data_country_date=None,
        pie_chart=None,
        rate_first_vaccination=0,
        total_first_vaccination=0,
        selected_representation="Density",
    )

    main.on_init(mock_state)

    assert mock_state.selected_country == "France"
    assert mock_state.data_country_date is not None
    assert mock_state.pie_chart is not None
    assert mock_state.rate_first_vaccination != 0
    assert mock_state.total_first_vaccination != 0
    assert isinstance(mock_state.pie_chart, pd.DataFrame)
