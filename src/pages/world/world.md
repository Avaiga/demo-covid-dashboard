# Covid Dashboard - **World**{: .color-primary} Statistics

Tracking the Global Reach and Trends of the COVID-19 Pandemic.

<br/>
<|layout|columns=2 2 2 2 2 1|gap=15px|
<|card|
**Deaths**{: .color-primary}
<|{to_text(np.sum(data_world_pie_absolute['Deaths']))}|text|class_name=h3|>
|>

<|card|
**Recovered**{: .color-primary}
<|{to_text(np.sum(data_world_pie_absolute['Recovered']))}|text|class_name=h3|>
|>

<|card|
**Confirmed**{: .color-primary}
<|{to_text(np.sum(data_world_pie_absolute['Confirmed']))}|text|class_name=h3|>
|>

<|card|
**Total vaccination**{: .color-primary}
<|{to_text(np.sum(vaccination['Total_First_Vaccination']))}|text|class_name=h3|>
|>

<|card|
**Vaccination rate**{: .color-primary}
<|{to_text(np.mean(vaccination['Rate_First_Vaccination']))} %|text|class_name=h3|>
|>
|>

<br/>

<|{selected_type}|toggle|lov={type_selector}|>

<|part|render={selected_type=='Absolute'}|
<|layout|columns=1 2|
<|{data_world_pie_absolute}|chart|type=pie|labels=Country/Region|values=Deaths|title=Distribution around the World|>

<|{data_world_evolution_absolute}|chart|properties={data_world_evolution_absolute_properties}|title=Evolution around the World|>
|>

<|{vaccination.sort_values('Total_First_Vaccination', ascending=False)}|chart|type=bar|x=COUNTRY|y=Total_First_Vaccination|>
|>

<|part|render={selected_type=='Relative'}|
<|layout|columns=1 2|
<|{data_world_pie_relative}|chart|type=pie|labels=Country/Region|values=Deaths/100k|>

<|{data_world_evolution_relative}|chart|properties={data_world_evolution_relative_properties}|>
|>

<|{vaccination.sort_values('Rate_First_Vaccination', ascending=False)}|chart|type=bar|x=COUNTRY|y=Rate_First_Vaccination|>
|>

<br/>

The data reflects the period from the onset of the pandemic in March 2020 through November 2020, highlighting key metrics to gauge the public health response and the efficacy of measures taken to control the spread of the virus. For projections and additional insights, please navigate to the 'Predictions' tab.