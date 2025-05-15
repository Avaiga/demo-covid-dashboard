import numpy as np
import pandas as pd

import taipy.gui.builder as tgb

from utils import to_text
from data.data import data, vaccination

# selected_country = "France"
data_country_date = None

representation_selector = ["Cumulative", "Density"]
selected_representation = representation_selector[0]

layout = {"barmode": "stack", "hovermode": "x"}
options = {"unselected": {"marker": {"opacity": 0.5}}}

rate_first_vaccination = 0
total_first_vaccination = 0

pie_chart = None


def initialize_case_evolution(data, selected_country="France"):
    # Aggregation of the dataframe to erase the regions that will not be used here
    data_country_date = data.groupby(["Country/Region", "Date"]).sum().reset_index()

    # a country is selected, here France by default
    data_country_date = data_country_date.loc[
        data_country_date["Country/Region"] == selected_country
    ]
    return data_country_date


def country_on_init(state):
    on_change_country(state)


def convert_density(state):
    if state.selected_representation == "Density":
        df_temp = state.data_country_date.copy()
        df_temp["Deaths"] = df_temp["Deaths"].diff().fillna(0)
        df_temp["Recovered"] = df_temp["Recovered"].diff().fillna(0)
        df_temp["Confirmed"] = df_temp["Confirmed"].diff().fillna(0)
        state.data_country_date = df_temp
    else:
        state.data_country_date = initialize_case_evolution(
            data, state.selected_country
        )


def on_change_country(state):
    # state contains all the Gui variables and this is through this state variable that we can update the Gui
    # state.selected_country, state.data_country_date, ...
    # update data_country_date with the right country (use initialize_case_evolution)
    print("Chosen country: ", state.selected_country)
    state.data_country_date = initialize_case_evolution(data, state.selected_country)
    state.pie_chart = pd.DataFrame(
        {
            "labels": ["Deaths", "Recovered", "Confirmed"],
            "values": [
                state.data_country_date.iloc[-1, 6],
                state.data_country_date.iloc[-1, 5],
                state.data_country_date.iloc[-1, 4],
            ],
        }
    )

    convert_density(state)

    state.rate_first_vaccination = get_vaccination_stats(
        vaccination, state.selected_country
    )["Rate_First_Vaccination"]

    state.total_first_vaccination = get_vaccination_stats(
        vaccination, state.selected_country
    )["Total_First_Vaccination"]


def get_vaccination_stats(vaccination, selected_country):
    vaccination_stats = vaccination[vaccination["COUNTRY"] == selected_country]
    if len(vaccination_stats) == 0:
        return {"Total_First_Vaccination": 0, "Rate_First_Vaccination": 0}
    return vaccination_stats


with tgb.Page() as country_page:
    tgb.text("# **Country** Statistics", mode="md")
    tgb.text(
        "This page provides a view of the COVID-19 pandemic's impact in a selected country, with statistics on the number of confirmed cases, recoveries, vaccination and fatalities."
    )
    tgb.html("br")

    with tgb.layout(columns="1 1 1", columns__mobile="1"):
        tgb.selector(
            "{selected_country}",
            lov=lambda selector_country: selector_country,
            on_change=on_change_country,
            dropdown=True,
            label="Country",
        )

        tgb.toggle(
            "{selected_representation}",
            lov=representation_selector,
            on_change=convert_density,
        )

    tgb.html("br")

    with tgb.layout(columns="2 2 2 2 2 1", gap="25px", columns__mobile="1"):
        with tgb.part("card"):
            tgb.text("**Deaths**", mode="md")
            tgb.text(
                lambda data_country_date: to_text(data_country_date.iloc[-1]["Deaths"]),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Recovered**", mode="md")
            tgb.text(
                lambda data_country_date: to_text(
                    data_country_date.iloc[-1]["Recovered"]
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Confirmed**", mode="md")
            tgb.text(
                lambda data_country_date: to_text(
                    data_country_date.iloc[-1]["Confirmed"]
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Vaccinated Population**", mode="md")
            tgb.text(
                lambda total_first_vaccination: to_text(total_first_vaccination),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Vaccination Rate**", mode="md")
            tgb.text(
                lambda rate_first_vaccination: to_text(rate_first_vaccination) + "%",
                class_name="h3",
            )

    tgb.html("br")

    with tgb.layout(columns="2 1", columns__mobile="1"):
        tgb.chart(
            "{data_country_date}",
            type="bar",
            x="Date",
            y=["Deaths", "Recovered", "Confirmed"],
            layout=layout,
            options=options,
            title="Covid Evolution",
        )

        tgb.chart(
            "{pie_chart}",
            type="pie",
            values="values",
            labels="labels",
            title="Distribution between cases",
        )

    tgb.html("br")

    tgb.text(
        "The data reflects the period from the onset of the pandemic in March 2020 through November 2020, highlighting key metrics to gauge the public health response and the efficacy of measures taken to control the spread of the virus. For projections and additional insights, please navigate to the 'Predictions' tab."
    )
