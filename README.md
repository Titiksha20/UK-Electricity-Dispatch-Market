# UK-Electricity-Dispatch-Market

Electricity Market Dispatch Simulation

Merit Order Dispatch with Pro-Rata Renewable Allocation

This repository implements an hourly electricity market dispatch model using a merit-order (pay-as-clear) auction, with an extension that applies pro-rata allocation across renewable generators when zero-marginal-cost renewables oversupply demand.

Both an exploratory Jupyter Notebook and a production-style Python script are provided.

Overview

The model simulates hourly dispatch across:

Wind generators

Solar generators

Gas generators (with time-varying marginal costs)

For each hour:

Generators are dispatched in merit order (lowest marginal cost first).

The market clearing price is set by the highest marginal cost unit dispatched.

System-level diagnostics are computed:

Supply–demand mismatch

Shortage hours

Technology mix

Renewable shares

Pro-Rata Renewable Extension

When total renewable availability exceeds demand and all renewables have identical marginal costs (zero), dispatch is split proportionally by available capacity across wind and solar units to avoid arbitrary ordering effects.

Repository Structure
.
├── dispatch_model.ipynb        # Notebook version (exploration + plots)
├── dispatch_model.py           # Script version (reproducible execution)
├── data.xlsx                   # Input data (not included / user-provided)
├── dispatch_results.csv
├── dispatch_hourly_summary.csv
├── dispatch_prorata.csv
├── hourly_prorata.csv
└── README.md

Input Data Requirements

The model expects an Excel file with the following sheets:

Running the Notebook (.ipynb)

Use the notebook for:

Step-by-step inspection

Visual diagnostics

Method comparison (merit order vs pro-rata)

Steps:

Open dispatch_model.ipynb

Ensure data.xlsx is in the same directory


Running the Script (.py)

Use the script for:

Command line
python dispatch_model.py

Outputs

The script saves:

Dispatch results (plant-level)

Hourly system summaries

Pro-rata adjusted results

All plots as image files

Key Outputs
Output	Description
dispatch_results.csv	Merit-order dispatch (plant-level)
dispatch_hourly_summary.csv	Hourly system summary
dispatch_prorata.csv	Pro-rata renewable dispatch
hourly_prorata.csv	Hourly summary (pro-rata case)
Dispatch plots	Generation stack, prices, mismatches
Methodological Notes

Dispatch follows pay-as-clear pricing, consistent with day-ahead electricity markets.

Pro-rata allocation is applied only when renewable availability exceeds demand.

Gas dispatch and pricing logic are unchanged under the pro-rata extension.

Hourly resolution reflects day-ahead market clearing, not real-time balancing.

Intended Use

This model is suitable for:

Electricity market coursework

Energy systems analysis

Policy or renewables integration studies

Quantitative energy market modeling portfolios

License

This project is provided for academic and educational use.

If you want, I can:

Tighten this for a course submission

Rewrite it for a recruiter-facing portfolio

Add assumptions & limitations as a separate section

smaller and shorter not this much description needed

Got it — here’s a short, clean, no-fluff README that still looks professional.

Electricity Market Dispatch Model

This repository contains a simple hourly electricity market simulation using a merit-order (pay-as-clear) dispatch, with an optional pro-rata allocation for renewables when zero-cost supply exceeds demand.

Both a Jupyter Notebook (for exploration) and a Python script (for clean execution) are included.

Files
dispatch_model.ipynb   # Exploratory notebook
dispatch_model.py      # Script version
data.xlsx              # Input data (user provided)

Method

Hourly dispatch based on marginal cost (merit order)

Market price set by highest dispatched marginal cost

Pro-rata split across wind and solar only when renewables oversupply demand

Gas dispatch unchanged

Run
Notebook

Open dispatch_model.ipynb and run all cells.

Script
python dispatch_model.py


CSV outputs and plots are saved automatically.

Outputs

dispatch_results.csv

dispatch_hourly_summary.csv

dispatch_prorata.csv

hourly_prorata.csv

Dispatch, price, mismatch, and renewable-share plots
