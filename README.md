# coronavirus: dataset joins and dashboard construction

This repository contains scripts for building datasets for COVID-19 analysis
and a notebook for constructing an interactive visualization dashboard using
Bokeh.  Currently only US data is included.

[COVID-19 Dashboard](https://zgana.github.io/assets/dashboards/covid19.html) ← Hosted copy of the resulting dashboard, as of whenever I last updated it.  TODO: maybe automate and schedule updates?

* [get-static-data.sh](get-static-data.sh): Set up base geography and population datasets.
* [prep-latest-data.py](prep-latest-data.py): Get latest state-level and county-level data.
* [build-dashboard.ipynb](build-dashboard.ipynb): Build the dashboard.

