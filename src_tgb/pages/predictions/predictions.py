import datetime as dt
import taipy.gui.builder as tgb
from taipy.gui import notify

selected_data_node = None
selected_scenario = None
selected_date = None
results = {
    "Date": [dt.datetime(2020, 10, 1)],
    "Deaths": [0],
    "ARIMA": [0],
    "Linear Regression": [0],
}


def get_result(scenario):
    if (
        scenario is None
        or isinstance(scenario, str)
        or not scenario.result.is_ready_for_reading
    ):
        return results
    return scenario.result.read()


def on_submission_change(state, submitable, details):
    if details["submission_status"] == "COMPLETED":
        state.results = get_result(state.selected_scenario)
        notify(state, "success", "Predictions ready!")
        print("Predictions ready!")
    elif details["submission_status"] == "FAILED":
        notify(state, "error", "Submission failed!")
        print("Submission failed!")


def on_change_params(state):
    if state.selected_date.year < 2020 or state.selected_date.year > 2021:
        notify(state, "error", "Invalid date! Must be between 2020 and 2021")
        state.selected_date = dt.datetime(2020, 10, 1)
        return

    state.selected_scenario.date.write(state.selected_date)
    state.selected_scenario.country.write(state.selected_country)
    notify(state, "success", "Scenario parameters changed!")

    state["Country"].on_change_country(state)


def on_change(state, var_name, var_value):
    if var_name == "selected_scenario" and var_value:
        state.selected_date = state.selected_scenario.date.read()
        state.selected_country = state.selected_scenario.country.read()
        state.results = get_result(state.selected_scenario)


with tgb.Page() as predictions_page:
    with tgb.layout(columns="2 9", gap="50px", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.text("**Scenario** Creation", mode="md")
            tgb.scenario_selector("{selected_scenario}")

        with tgb.part("scenario"):
            tgb.text("# **Prediction** page", mode="md")
            tgb.text(
                "Create a scenario, choose a date in 2020 and a country and simulate predictions with this information."
            )

            with tgb.part(
                render=lambda selected_scenario: selected_scenario is not None
            ):
                with tgb.layout(columns="1 1"):
                    with tgb.part("date"):
                        tgb.text("#### First **day** of prediction", mode="md")
                        tgb.date("{selected_date}", on_change=on_change_params)
                    with tgb.part("country"):
                        tgb.text("#### **Country** of prediction", mode="md")
                        tgb.selector(
                            "{selected_country}",
                            lov="{selector_country}",
                            dropdown=True,
                            on_change=on_change_params,
                            label="Country",
                        )

                tgb.scenario(
                    "{selected_scenario}",
                    on_submission_change=on_submission_change,
                    expanded=False,
                )

                tgb.html("hr")

                tgb.text("## **Predictions** and explorer of data nodes", mode="md")

                tgb.chart(
                    "{results}",
                    x="Date",
                    y=["Deaths", "Linear Regression", "ARIMA"],
                    type=["bar", "line", "line"],
                    title="Predictions",
                )

                with tgb.expandable("Data Nodes"):
                    with tgb.layout(columns="1 5"):
                        tgb.data_node_selector("{selected_data_node}")
                        tgb.data_node("{selected_data_node}")
