from taipy.gui import Markdown, notify


selected_data_node = None
selected_scenario = None


def on_change_country_scenario(state):
    state['Country'].on_change_country_scenario(state)

    state.selected_scenario.country.write(state.selected_country)
    notify(state, "success", "Scenario value saved!")


predictions_md = Markdown("pages/predictions/predictions.md")