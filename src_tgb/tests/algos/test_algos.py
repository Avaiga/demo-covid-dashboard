import pandas as pd
import datetime as dt
import numpy as np
import pytest
from sklearn.linear_model import LinearRegression

import algos.algos  # replace with the actual module name where functions live

from algos.algos import (
    add_features,
    create_train_data,
    preprocess,
    train_arima,
    forecast,
    train_linear_regression,
    forecast_linear_regression,
    concat,
)

# ---- Fixtures ----


@pytest.fixture
def sample_dates():
    return pd.date_range("2020-01-01", periods=5)


@pytest.fixture
def sample_data(sample_dates):
    # Two countries, 5 dates each
    df = pd.DataFrame(
        {
            "Country/Region": ["A"] * 5 + ["B"] * 5,
            "Date": list(sample_dates) * 2,
            "Deaths": list(range(1, 6)) + list(range(6, 11)),
        }
    )
    return df


@pytest.fixture
def sample_final_data(sample_dates):
    # For concat: final_data with existing dates
    return pd.DataFrame({"Date": sample_dates, "Deaths": [1, 2, 3, 4, 5]})


@pytest.fixture
def sample_predictions():
    return np.array([10, 20, 30, 40, 50])


# ---- Tests ----


def test_add_features_creates_new_columns(sample_dates):
    df = pd.DataFrame({"Date": sample_dates})
    out = add_features(df.copy())
    # Check new columns
    assert "Months" in out.columns
    assert "Days" in out.columns
    assert "Week" in out.columns
    assert "Day of week" in out.columns
    # Verify one value
    assert out.loc[0, "Months"] == sample_dates[0].month


def test_create_train_data_filters_by_date(sample_dates):
    df = pd.DataFrame({"Date": sample_dates, "Deaths": range(5)})
    cutoff = dt.datetime(2020, 1, 3)
    train = create_train_data(df, cutoff)
    # should include dates <= Jan 3
    assert train["Date"].dt.date.max() == cutoff.date()
    assert len(train) == 3


def test_preprocess_returns_final_and_train(sample_data):
    # choose country "A" and cutoff Jan 3
    final, train = preprocess(sample_data, "A", dt.datetime(2020, 1, 3))
    # final contains only "A"
    assert "Deaths" in final.columns
    # train is subset by date
    assert train["Date"].dt.date.max() == dt.date(2020, 1, 3)


def test_train_arima_monkeypatched(monkeypatch, sample_data):
    # monkeypatch auto_arima to return a dummy model
    class DummyModel:
        def __init__(self):
            self.fitted = False

        def fit(self, series):
            self.fitted = True

        def predict(self, n_periods):
            return [1] * n_periods

    monkeypatch.setattr(algos.algos, "auto_arima", lambda *args, **kwargs: DummyModel())
    train = create_train_data(
        preprocess(sample_data, "A", dt.datetime(2020, 1, 5))[0],
        dt.datetime(2020, 1, 5),
    )
    model = train_arima(train)
    assert hasattr(model, "predict")
    preds = forecast(model)
    assert isinstance(preds, np.ndarray)
    assert len(preds) == 60


def test_train_linear_and_forecast_lr(sample_data):
    # prepare train_data
    _, train = preprocess(sample_data, "A", dt.datetime(2020, 1, 5))
    # train linear model
    lr_model = train_linear_regression(train)
    assert isinstance(lr_model, LinearRegression)
    # forecast for next date
    base_date = dt.datetime(2020, 1, 6)
    preds = forecast_linear_regression(lr_model, base_date)
    assert len(preds) == 60


def test_concat_merges_predictions(sample_final_data, sample_predictions):
    date0 = sample_final_data.loc[0, "Date"]
    df = concat(sample_final_data.copy(), sample_predictions, sample_predictions, date0)
    # result should have original + 60 new dates
    unique_dates = df["Date"].dt.date.unique()
    assert len(unique_dates) == len(sample_final_data)
    # check both prediction columns exist
    assert "ARIMA" in df.columns
    assert "Linear Regression" in df.columns
