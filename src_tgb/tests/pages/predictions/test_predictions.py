import datetime as dt
import pytest
from taipy.gui import Gui
from taipy.gui.mock.mock_state import MockState
import pandas as pd

from unittest.mock import MagicMock

from pages.predictions.predictions import (
    get_result,
    on_submission_change,
    on_change_params,
    on_change,
    results as default_results,
)

# ---- Fixtures ----


class FakeScenario:
    def __init__(self, ready=True, result_data=None):
        self.result = MagicMock()
        self.result.is_ready_for_reading = ready
        self.result.read.return_value = result_data or {
            "Date": [dt.datetime(2020, 10, 1)],
            "Deaths": [10],
            "ARIMA": [5],
            "Linear Regression": [6],
        }
        self.date = MagicMock()
        self.country = MagicMock()
        self.date.read.return_value = dt.datetime(2020, 10, 1)
        self.country.read.return_value = "France"


@pytest.fixture
def state():
    return MockState(
        Gui(""),
        selected_date=dt.datetime(2020, 10, 1),
        selected_country="France",
        selected_scenario=FakeScenario(),
        results={},
    )


# ---- Tests ----


def test_get_result_none_returns_default():
    assert get_result(None) == default_results


def test_get_result_string_returns_default():
    assert get_result("invalid") == default_results


def test_get_result_not_ready_returns_default():
    scenario = FakeScenario(ready=False)
    assert get_result(scenario) == default_results


def test_get_result_ready_returns_data():
    scenario = FakeScenario()
    result = get_result(scenario)
    assert result["Deaths"] == [10]


def test_on_submission_change_success(monkeypatch):
    ms = MockState(Gui(""), selected_scenario=FakeScenario(), results={})

    notify_called = []
    monkeypatch.setattr(
        "pages.predictions.predictions.notify",
        lambda s, t, m: notify_called.append((t, m)),
    )

    on_submission_change(ms, None, {"submission_status": "COMPLETED"})

    assert "Deaths" in ms.results
    assert notify_called[-1][0] == "success"


def test_on_submission_change_failed(monkeypatch):
    ms = MockState(Gui(""))
    notify_called = []
    monkeypatch.setattr(
        "pages.predictions.predictions.notify",
        lambda s, t, m: notify_called.append((t, m)),
    )

    on_submission_change(ms, None, {"submission_status": "FAILED"})
    assert notify_called[-1][0] == "error"


def test_on_change_params_valid(monkeypatch, state):
    call_log = []

    monkeypatch.setattr(
        "pages.predictions.predictions.notify", lambda s, t, m: call_log.append((t, m))
    )
    state.selected_scenario.date.write = lambda x: call_log.append(("date_written", x))
    state.selected_scenario.country.write = lambda x: call_log.append(
        ("country_written", x)
    )

    state["Country"].on_change_country = lambda s: call_log.append(
        "called_on_change_country"
    )

    on_change_params(state)

    assert ("success", "Scenario parameters changed!") in call_log
    assert "called_on_change_country" in call_log


def test_on_change_params_invalid(monkeypatch, state):
    call_log = []
    monkeypatch.setattr(
        "pages.predictions.predictions.notify", lambda s, t, m: call_log.append((t, m))
    )

    state.selected_date = dt.datetime(2019, 12, 31)
    on_change_params(state)

    assert state.selected_date == dt.datetime(2020, 10, 1)
    assert ("error", "Invalid date! Must be between 2020 and 2021") in call_log


def test_on_change_sets_fields():
    from config.config import scenario_cfg
    import taipy as tp

    tp.Orchestrator().run()
    scenario = tp.create_scenario(scenario_cfg)
    scenario.submit(wait=True)
    ms = MockState(
        Gui(""),
        selected_scenario=scenario,
        selected_date=None,
        selected_country=None,
        results={},
    )

    on_change(ms, "selected_scenario", scenario)
    assert ms.selected_date == dt.datetime(2020, 10, 1)
    assert ms.selected_country == "France"
    assert isinstance(ms.results, pd.DataFrame)
    assert "Deaths" in ms.results
