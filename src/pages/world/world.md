# **World**{: .color-primary} Statistics


<|layout|columns=1 1 1 1|gap=50px|
<|part|class_name=card|
## Deaths
<|{'{:,}'.format(int(np.sum(data_world_pie_absolute['Deaths']))).replace(',', ' ')}|>
|>

<|part|class_name=card|
## Recovered
<|{'{:,}'.format(int(np.sum(data_world_pie_absolute['Recovered']))).replace(',', ' ')}|>
|>

<|part|class_name=card|
## Confirmed
<|{'{:,}'.format(int(np.sum(data_world_pie_absolute['Confirmed']))).replace(',', ' ')}|>
|>
|>

<|{selected_type}|toggle|lov={type_selector}|>

<|part|render={selected_type=='Absolute'}|
<|layout|columns=1 2|
<|{data_world_pie_absolute}|chart|type=pie|labels=Country/Region|values=Deaths|>

<|{data_world_evolution_absolute}|chart|properties={data_world_evolution_absolute_properties}|>
|>
|>

<|part|render={selected_type=='Relative'}|
<|layout|columns=1 2|
<|{data_world_pie_relative}|chart|type=pie|labels=Country/Region|values=Deaths/100k|>

<|{data_world_evolution_relative}|chart|properties={data_world_evolution_relative_properties}|>
|>
|>
