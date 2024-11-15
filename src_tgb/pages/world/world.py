import taipy.gui.builder as tgb

import numpy as np
import json

from data.data import data, vaccination
from utils import to_text

type_selector = ["Absolute", "Relative"]
selected_type = type_selector[0]
np_sum = np.sum
np_mean = np.mean


def initialize_world(data):
    data_world = data.groupby(["Country/Region", "Date"]).sum().reset_index()

    with open("data/pop.json", "r") as f:
        pop = json.load(f)

    data_world["Population"] = data_world["Country/Region"].map(
        lambda x: pop.get(x, [None, 0])[1]
    )

    data_world = data_world.dropna().reset_index()
    data_world["Deaths/100k"] = (
        data_world.loc[:, "Deaths"] / data_world.loc[:, "Population"] * 100000
    )

    data_world_pie_absolute = (
        data_world[["Country/Region", "Deaths", "Recovered", "Confirmed"]]
        .groupby(["Country/Region"])
        .max()
        .sort_values(by="Deaths", ascending=False)[:20]
        .reset_index()
    )

    data_world_pie_relative = (
        data_world[["Country/Region", "Deaths/100k"]]
        .groupby(["Country/Region"])
        .max()
        .sort_values(by="Deaths/100k", ascending=False)[:20]
        .reset_index()
    )

    country_absolute = data_world_pie_absolute["Country/Region"].unique().tolist()
    country_relative = (
        data_world_pie_relative.loc[:, "Country/Region"].unique().tolist()
    )

    data_world_evolution_absolute = data_world[
        data_world["Country/Region"].str.contains(
            "|".join(country_absolute), regex=True
        )
    ]
    data_world_evolution_absolute = data_world_evolution_absolute.pivot(
        index="Date", columns="Country/Region", values="Deaths"
    ).reset_index()

    data_world_evolution_relative = data_world[
        data_world["Country/Region"].str.contains(
            "|".join(country_relative), regex=True
        )
    ]
    data_world_evolution_relative = data_world_evolution_relative.pivot(
        index="Date", columns="Country/Region", values="Deaths/100k"
    ).reset_index()
    return (
        data_world,
        data_world_pie_absolute,
        data_world_pie_relative,
        data_world_evolution_absolute,
        data_world_evolution_relative,
    )


(
    _,
    data_world_pie_absolute,
    data_world_pie_relative,
    data_world_evolution_absolute,
    data_world_evolution_relative,
) = initialize_world(data)


data_world_evolution_absolute_properties = {"x": "Date"}
cols = [col for col in data_world_evolution_absolute.columns if col != "Date"]
for i in range(len(cols)):
    data_world_evolution_absolute_properties[f"y[{i}]"] = cols[i]


data_world_evolution_relative_properties = {"x": "Date"}
cols = [col for col in data_world_evolution_relative.columns if col != "Date"]
for i in range(len(cols)):
    data_world_evolution_relative_properties[f"y[{i}]"] = cols[i]


with tgb.Page() as world_page:
    tgb.text("# **World** Statistics", mode="md")
    tgb.text("Tracking the Global Reach and Trends of the COVID-19 Pandemic.")
    tgb.html("br")

    with tgb.layout(columns="2 2 2 2 2 1", gap="15px", columns__mobile="1"):
        with tgb.part("card"):
            tgb.text("**Deaths**", mode="md")
            tgb.text(
                lambda data_world_pie_absolute: to_text(
                    np_sum(data_world_pie_absolute["Deaths"])
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Recovered**", mode="md")
            tgb.text(
                lambda data_world_pie_absolute: to_text(
                    np_sum(data_world_pie_absolute["Recovered"])
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Confirmed**", mode="md")
            tgb.text(
                lambda data_world_pie_absolute: to_text(
                    np_sum(data_world_pie_absolute["Confirmed"])
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Total vaccination**", mode="md")
            tgb.text(
                lambda vaccination: to_text(
                    np_sum(vaccination["Total_First_Vaccination"])
                ),
                class_name="h3",
            )

        with tgb.part("card"):
            tgb.text("**Vaccination rate**", mode="md")
            tgb.text(
                lambda vaccination: to_text(
                    np_mean(vaccination["Rate_First_Vaccination"])
                )
                + " %",
                class_name="h3",
            )

    tgb.html("br")

    tgb.toggle("{selected_type}", lov=type_selector)

    with tgb.part(render=lambda selected_type: selected_type == "Absolute"):
        with tgb.layout(columns="1 2", columns__mobile="1"):
            tgb.chart(
                "{data_world_pie_absolute}",
                type="pie",
                labels="Country/Region",
                values="Deaths",
                title="Distribution around the World",
            )

            tgb.chart(
                "{data_world_evolution_absolute}",
                properties="{data_world_evolution_absolute_properties}",
                title="Evolution around the World",
            )

        tgb.chart(
            lambda vaccination: vaccination.sort_values(
                "Total_First_Vaccination", ascending=False
            ),
            type="bar",
            x="COUNTRY",
            y="Total_First_Vaccination",
        )

    with tgb.part(render=lambda selected_type: selected_type == "Relative"):
        with tgb.layout(columns="1 2", columns__mobile="1"):
            tgb.chart(
                "{data_world_pie_relative}",
                type="pie",
                labels="Country/Region",
                values="Deaths/100k",
            )

            tgb.chart(
                "{data_world_evolution_relative}",
                properties="{data_world_evolution_relative_properties}",
            )

        tgb.chart(
            lambda vaccination: vaccination.sort_values(
                "Rate_First_Vaccination", ascending=False
            ),
            type="bar",
            x="COUNTRY",
            y="Rate_First_Vaccination",
        )

    tgb.html("br")

    tgb.text(
        "The data reflects the period from the onset of the pandemic in March 2020 through November 2020, highlighting key metrics to gauge the public health response and the efficacy of measures taken to control the spread of the virus. For projections and additional insights, please navigate to the 'Predictions' tab."
    )
