import plotly.express as px
from data.data import geojson


def create_choropleth_mapbox(vaccination):
    if vaccination is None or vaccination.empty:
        return None
    vaccination_map = px.choropleth_mapbox(
        vaccination,
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
        labels={
            "Rate_First_Vaccination": "Vaccination Rate",
            "Total_First_Vaccination": "Vaccination Count",
        },
        title="COVID-19 Vaccination Rates per 100 People by Country",
    )  # Title of the map

    vaccination_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return vaccination_map


def create_cluster_map(data_province_displayed):
    if data_province_displayed is None or data_province_displayed.empty:
        return None
    cluster_map = px.scatter_mapbox(
        data_province_displayed,
        lat="Latitude",
        lon="Longitude",
        size="Size",
        color="Deaths",
        color_continuous_scale="solar",
        size_max=60,
        hover_name="Province/State",
        hover_data={
            "Deaths": True,
            "Latitude": False,
            "Longitude": False,
            "Size": False,
        },
        mapbox_style="open-street-map",
        zoom=3,
        center={"lat": 38, "lon": -90},
    )

    # Update layout with specific options
    cluster_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode="zoom")
    return cluster_map
