import numpy as np
import plotly.express as px
import taipy.gui.builder as tgb

from data.data import data, vaccination
from utils import to_text
from pages.map.charts import create_choropleth_mapbox, create_cluster_map


def initialize_map(data):
    data["Province/State"] = data["Province/State"].fillna(data["Country/Region"])
    data_province = data.groupby(
        ["Country/Region", "Province/State", "Longitude", "Latitude"]
    ).max()

    data_province_displayed = data_province[data_province["Deaths"] > 10].reset_index()

    # Size when using Taipy charts
    # data_province_displayed['Size'] = np.sqrt(data_province_displayed.loc[:,'Deaths']/data_province_displayed.loc[:,'Deaths'].max())*80 + 3
    # data_province_displayed['Text'] = data_province_displayed.loc[:,'Deaths'].astype(str) + ' deaths </br> ' + data_province_displayed.loc[:,'Province/State']

    # Size when using Plotly Python
    data_province_displayed["Size"] = (
        (
            data_province_displayed.loc[:, "Deaths"]
            / data_province_displayed.loc[:, "Deaths"].max()
        )
        * 100
    ) + 0.1
    return data_province_displayed


data_province_displayed = initialize_map(data)

sum_deaths = data_province_displayed["Deaths"].sum()
cluster_selected = []

mean_rate_of_vaccination = np.mean(vaccination["Rate_First_Vaccination"])
sum_vaccination = vaccination["Total_First_Vaccination"].sum()
countries_selected = []

vaccination_map = create_choropleth_mapbox(vaccination)
cluster_map = create_cluster_map(data_province_displayed)


def on_change(state, var_name, var_value):
    if isinstance(var_value, list) and len(var_value) > 0:
        var_value = var_value[0]
        if var_name == "countries_selected" and len(var_value) > 0:
            var_value = list(var_value)
            # Mean rate of vaccination:
            state.mean_rate_of_vaccination = state.vaccination.loc[
                var_value, "Rate_First_Vaccination"
            ].mean()
            # Sum count of vaccination:
            state.sum_vaccination = state.vaccination.loc[
                var_value, "Total_First_Vaccination"
            ].sum()
        elif var_name == "countries_selected":
            state.mean_rate_of_vaccination = np.mean(
                vaccination["Rate_First_Vaccination"]
            )
            state.sum_vaccination = vaccination["Total_First_Vaccination"].sum()
        if var_name == "cluster_selected" and len(var_value) > 0:
            # Sum of deaths
            state.sum_deaths = state.data_province_displayed.loc[
                var_value, "Deaths"
            ].sum()
        elif var_name == "cluster_selected":
            state.sum_deaths = data_province_displayed["Deaths"].sum()


with tgb.Page() as map_page:
    tgb.text("# **Map** Statistics", mode="md")
    tgb.text(
        "You can select clusters and countries in the two maps below. These will give you information on these clusters and countries."
    )

    with tgb.layout(columns="1 1", columns__mobile="1"):
        # First map part
        with tgb.part():
            tgb.text("### Covid Clusters", mode="md")
            tgb.text(
                lambda sum_deaths: f"##### Total Deaths: {to_text(sum_deaths)}",
                mode="md",
            )
            tgb.chart(
                figure="{cluster_map}",
                selected="{cluster_selected}",
            )

        # Second map part
        with tgb.part():
            tgb.text("### Vaccination Rate", mode="md")
            tgb.text(
                lambda mean_rate_of_vaccination, sum_vaccination: f"##### Mean Rate of Vaccination: {int(mean_rate_of_vaccination)}% | Total Vaccinations: {to_text(sum_vaccination)}",
                mode="md",
            )
            tgb.chart(
                figure="{vaccination_map}",
                selected="{countries_selected}",
            )


"""
# For Taipy charts
marker_map = {"color":"Deaths", "size": "Size", "showscale":True, "colorscale":"Viridis"}
layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 38, "lon": -90 }, "zoom": 3}
            }
options = {"unselected":{"marker":{"opacity":0.5}}}
"""
