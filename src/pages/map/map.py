
import numpy as np
from taipy.gui import Markdown
import plotly.express as px

from data.data import data, geojson, vaccination


def initialize_map(data):
    data['Province/State'] = data['Province/State'].fillna(data["Country/Region"])
    data_province = data.groupby(["Country/Region",
                                  'Province/State',
                                  'Longitude',
                                  'Latitude'])\
                         .max()
                         

    data_province_displayed = data_province[data_province['Deaths']>10].reset_index()

    # Size when using Taipy charts
    # data_province_displayed['Size'] = np.sqrt(data_province_displayed.loc[:,'Deaths']/data_province_displayed.loc[:,'Deaths'].max())*80 + 3
    # data_province_displayed['Text'] = data_province_displayed.loc[:,'Deaths'].astype(str) + ' deaths </br> ' + data_province_displayed.loc[:,'Province/State']

    # Size when using Plotly Python
    data_province_displayed['Size'] = ((data_province_displayed.loc[:,'Deaths']/data_province_displayed.loc[:,'Deaths'].max()) * 100) + 0.1
    return data_province_displayed


data_province_displayed = initialize_map(data)

sum_deaths = data_province_displayed['Deaths'].sum()
cluster_selected = [] 
# Creating a Plotly scatter mapbox plot
cluster_map = px.scatter_mapbox(data_province_displayed,
                        lat="Latitude",
                        lon="Longitude",
                        size="Size",
                        color="Deaths",
                        color_continuous_scale="solar",
                        size_max=60,
                        hover_name="Province/State",
                        hover_data={"Deaths": True, "Latitude": False, "Longitude": False, "Size": False},
                        mapbox_style="open-street-map",
                        zoom=3,
                        center={"lat": 38, "lon": -90})

# Update layout with specific options
cluster_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                  dragmode="zoom")


mean_rate_of_vaccination = np.mean(vaccination['Rate_First_Vaccination'])
sum_vaccination = vaccination['Total_First_Vaccination'].sum()
countries_selected = []
vaccination_map = px.choropleth_mapbox(vaccination,
                           geojson=geojson,  # You need a GeoJSON file for the country boundaries
                           featureidkey="id",
                           locations="ISO_A3",  # Column in your dataframe that matches GeoJSON features
                           color="Rate_First_Vaccination",  # Column giving the color intensity
                           hover_name="COUNTRY",  # Column for hover info
                           hover_data={"Rate_First_Vaccination": True, "Total_First_Vaccination": True},
                           zoom=1,  # Zoom level
                           center={"lat": 0, "lon": 0},  # Map center
                           color_continuous_scale="Viridis_r",  # Color scale
                           mapbox_style="carto-positron",
                           labels={"Rate_First_Vaccination": "Vaccination Rate", "Total_First_Vaccination": "Vaccination Count"},
                           title="COVID-19 Vaccination Rates per 100 People by Country")  # Title of the map

vaccination_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


def on_change(state, var_name, var_value):
    if var_name == 'countries_selected' and len(var_value)>0:
        # Mean rate of vaccination:
        state.mean_rate_of_vaccination = state.vaccination.loc[var_value, 'Rate_First_Vaccination'].mean()
        # Sum count of vaccination:
        state.sum_vaccination = state.vaccination.loc[var_value, 'Total_First_Vaccination'].sum()
    elif var_name == 'countries_selected':
        state.mean_rate_of_vaccination = np.mean(vaccination['Rate_First_Vaccination'])
        state.sum_vaccination = vaccination['Total_First_Vaccination'].sum()
    if var_name == 'cluster_selected' and len(var_value)>0:
        # Sum of deaths
        state.sum_deaths = state.data_province_displayed.loc[var_value, 'Deaths'].sum()
    elif var_name == 'cluster_selected':    
        state.sum_deaths = data_province_displayed['Deaths'].sum()
        

map_md = Markdown("pages/map/map.md")


"""
# For Taipy charts
marker_map = {"color":"Deaths", "size": "Size", "showscale":True, "colorscale":"Viridis"}
layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 38, "lon": -90 }, "zoom": 3}
            }
options = {"unselected":{"marker":{"opacity":0.5}}}
"""