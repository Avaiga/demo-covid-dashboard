# **Prediction**{: .color-primary} page
  
  
<|layout|columns=2 5 5|
<|
### Scenario Creation

<|{selected_scenario}|scenario_selector|>
|>

<|
### Date

<|{selected_scenario.date if selected_scenario else None}|data_node|>
|>

<|
### Country    

<|{selected_country}|selector|lov={selector_country}|dropdown|on_change=on_change_country_scenario|label=Country|>
|>
|>

<|{selected_scenario}|scenario|>

---------------------------------------

## Result

<|{selected_scenario.result if selected_scenario else None}|data_node|>


<|Data Nodes|expandable|
<|1 5|layout|
<|{selected_data_node}|data_node_selector|> 

<|{selected_data_node}|data_node|>
|>
|>
