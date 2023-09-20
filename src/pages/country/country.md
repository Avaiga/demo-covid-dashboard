# **Country**{: .color-primary} Statistics

<|layout|columns=1 1 1|
<|{selected_country}|selector|lov={selector_country}|on_change=on_change_country|dropdown|label=Country|>

<|{selected_representation}|toggle|lov={representation_selector}|on_change=convert_density|>
|>

<|layout|columns=1 1 1 1|
<|part|class_name=card m2|
## Deaths
<|{'{:,}'.format(int(data_country_date.iloc[-1, 6])).replace(',', ' ')}|>
|>

<|part|class_name=card m2|
## Recovered
<|{'{:,}'.format(int(data_country_date.iloc[-1, 5])).replace(',', ' ')}|>
|>

<|part|class_name=card m2|
## Confirmed
<|{'{:,}'.format(int(data_country_date.iloc[-1, 4])).replace(',', ' ')}|>
|>
|>

<|layout|columns=2 1|
<|{data_country_date}|chart|type=bar|x=Date|y[3]=Deaths|y[2]=Recovered|y[1]=Confirmed|layout={layout}|options={options}|>

<|{pie_chart}|chart|type=pie|values=values|labels=labels|>
|>