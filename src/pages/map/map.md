# Covid Dashboard - **Map**{: .color-primary} Statistics

You can select clusters and countries in the two maps below. These will give you information on these clusters and countries. 

<|layout|columns=1 1|
<|
### Covid Clusters
##### Total Deaths: <|{to_text(sum_deaths)}|text|raw|>
<|chart|figure={cluster_map}|height=700px|selected={cluster_selected}|>
|>

<|
### Vaccination Rate
##### Mean Rate of Vaccination: <|{int(mean_rate_of_vaccination)}|text|raw|> % | Total Vaccinations: <|{to_text(sum_vaccination)}|text|raw|>
<|chart|figure={vaccination_map}|height=700px|selected={countries_selected}|>
|>
|>


[//]: <> (This is a Markdown comment, here is how you can create the same map with Taipy:)
[//]: <> (<|{data_province_displayed}|chart|type=scattermapbox|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>)