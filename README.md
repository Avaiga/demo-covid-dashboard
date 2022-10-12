# Demo Covid Dashboard

## Usage
- [Usage](#usage)
- [Demo Covid Dashboard](#what-is-demo-covid-dashboard)
- [Directory Structure](#directory-structure)
- [License](#license)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)

## What is Demo Covid Dashboard

Taipy is a Python library for creating Business Applications. More information on our
[website](https://www.taipy.io).

[Demo Covid Dashboard](https://github.com/Avaiga/demo-covid-dashboard) is a multi-page application showing how Taipy Core and Taipy Gui can work together to build a minimalist but powerful application.
This demo visualizes a Covid dataset for the year 2020. Pages shows different graphs and information on Covid. A Prediction page is also present to predict the number of death.

### Demo Type
- **Level**: Advanced
- **Topic**: Taipy-GUI, Taipy-Core
- **Components/Controls**: 
  - Taipy GUI: selector, chart, toggle, slider, expandable, table
  - Taipy Core: datanode, pipeline, scenario

## How to run

This demo works with a Python version superior to 3.8. Install the dependencies of the *Pipfile* and run the *main.py* in the `src/` folder.

## Introduction

This  demo manage multiple pages.

### Country page

The first page represents statistics on a specific country. The country can be changed as well as the the way the data is displayed (either cumulative or density). It will interact with the line chart provided on this page.

The pie chart shows the repartition of cases between Confirmed, Recovered, and Deaths. 

### Map

A map can be found on this page to explore the data. Colors and sizes are dependant on the number of Deaths of this location.

### Predictions

This page lets anyone create scenarios to predict on certain dates for a specific country. To create a scenario, a name has to be written and the 'Create' button pressed. The prediction will be created after clicking 'Submit' based on the prediction date and the country.

A list of scenarios can be found and any scenario can be selected to display their predictions.

### World page

Statistics on the World are presented on the page. A line chart and pie chart displays the data. Moreover, absolute or relative impact of Covid countries can be seen by changing the toggle between 'Absolute' and 'Relative'. 

## Directory Structure


- `src/`: Contains the demo source code.
  - `src/algos`: Contains the functions to be executed as tasks by Taipy.
  - `src/config`: Contains the configuration files.
  - `src/data`: Contains the application data files.
  - `src/images`: Contains the application image files.
  - `src/pages`: Contains the page definition files.
- `docs/`: contains the images for the documentation
- `CODE_OF_CONDUCT.md`: Code of conduct for members and contributors of _demo-covid-dashboard_.
- `CONTRIBUTING.md`: Instructions to contribute to _demo-covid-dashboard_.
- `INSTALLATION.md`: Instructions to install _demo-covid-dashboard_.
- `LICENSE`: The Apache 2.0 License.
- `Pipfile`: File used by the Pipenv virtual environment to manage project dependencies.
- `README.md`: Current file.

## License
Copyright 2022 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Installation

Want to install _Demo Covid Dashboard_? Check out our [`INSTALLATION.md`](INSTALLATION.md) file.

## Contributing

Want to help build _Demo Covid Dashboard_? Check out our [`CONTRIBUTING.md`](CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the _Demo Covid Dashboard_ community? Check out our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) file.
