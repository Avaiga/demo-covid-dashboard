# Covid Dashboard - **Country**{: .color-primary} Statistics

This page provides a view of the COVID-19 pandemic's impact in a selectd country, with statistics on the number of confirmed cases, recoveries, vaccination and fatalities.

<br/>

<|layout|columns=1 1 1|
<|{selected_country}|selector|lov={selector_country}|on_change=on_change_country|dropdown|label=Country|>

<|{selected_representation}|toggle|lov={representation_selector}|on_change=convert_density|>
|>

<br/>

<|layout|columns=2 2 2 2 2 1|gap=25px|
<|card|
**Deaths**{: .color-primary}
<|{to_text(data_country_date.iloc[-1]['Deaths'])}|text|class_name=h3|>
|>

<|card|
**Recovered**{: .color-primary}
<|{to_text(data_country_date.iloc[-1]['Recovered'])}|text|class_name=h3|>
|>

<|card|
**Confirmed**{: .color-primary}
<|{to_text(data_country_date.iloc[-1]['Confirmed'])}|text|class_name=h3|>
|>

<|card|
**Vaccinated Population**{: .color-primary}
<|{to_text(get_vaccination_stats(vaccination, selected_country)['Total_First_Vaccination'])}|text|class_name=h3|>
|>

<|card|
**Vaccination rate**{: .color-primary}
<|{to_text(get_vaccination_stats(vaccination, selected_country)['Rate_First_Vaccination'])} %|text|class_name=h3|>
|>
|>
<br/>

<|layout|columns=2 1|
<|{data_country_date}|chart|type=bar|x=Date|y[3]=Deaths|y[2]=Recovered|y[1]=Confirmed|layout={layout}|options={options}|title=Covid Evolution|>

<|{pie_chart}|chart|type=pie|values=values|labels=labels|title=Distribution between cases|>
|>

<br/>

The data reflects the period from the onset of the pandemic in March 2020 through November 2020, highlighting key metrics to gauge the public health response and the efficacy of measures taken to control the spread of the virus. For projections and additional insights, please navigate to the 'Predictions' tab.