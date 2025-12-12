# Electricity Market Dispatch

This repository contains an hourly electricity dispatch model using a merit-order (pay-as-clear) approach, with an optional pro-rata allocation when total renewable (wind + solar) availability exceeds demand. Both a Jupyter Notebook (`.ipynb`) and a Python script (`.py`) are provided.

## Files
- `dispatch_model.ipynb` – Notebook version for interactive exploration.
- `dispatch_model.py` – Python script version for running end-to-end dispatch and saving outputs.

### Outputs

**CSV Files:**

- `dispatch_results.csv` – Hourly dispatch of all units (original merit order).  
- `dispatch_hourly_summary.csv` – Hourly summary including total dispatched, shortage hours, mismatch, and marginal price.  
- `dispatch_prorata.csv` – Hourly dispatch with pro-rata allocation among renewables.  
- `hourly_prorata.csv` – Hourly summary for pro-rata dispatch.

## How to Run
For the Python script:

```bash
python dispatch_model.py
