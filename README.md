# Drift Diffusion Model (DDM)

Simulation and quick parameter fitting for perceptual decision-making.

This project implements a minimal Drift Diffusion Model (DDM) to simulate
evidence accumulation in binary decision tasks and estimate the drift parameter
using a simple grid-search approach.

---

## Overview

The Drift Diffusion Model is widely used in cognitive neuroscience to model
decision-making processes at the subject level.

This repository:

- Simulates trial-level evidence accumulation
- Generates decision times and binary choices
- Estimates the drift rate parameter
- Produces visual comparison between observed and fitted RT distributions

---
## Project Structure


ddm-perceptual-decision-model/
├── src/
│   └── ddm_model.py
├── results/
│   ├── decision_time_distribution.png
│   ├── fit_overlay.png
│   └── fit_report.txt
├── notebooks/
├── requirements.txt
└── README.md

---


## Installation

pip install -r requirements.txt

---

## Run

python src/ddm_model.py

---

## Example Output

## Example output

### Model fit
![Fit overlay](plots/fit_overlay.png)

### Simulated RT distribution
![RT distribution](plots/decision_time_distribution.png)



