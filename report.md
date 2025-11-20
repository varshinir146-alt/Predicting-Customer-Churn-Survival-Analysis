# Project Report - Survival Analysis

## 1. Objective
Simulate a survival dataset and demonstrate end-to-end analysis: EDA, Kaplan-Meier estimation, Cox proportional hazards modeling, and interpretation.

## 2. Data
Provided simulated_survival_data.csv with variables:
- id: subject id
- age: age in years (integer)
- sex: 0 female, 1 male
- treatment: A or B
- biomarker: continuous standard-normal biomarker
- time: observed follow-up time (same units)
- event: event indicator (1=event, 0=censored)

## 3. Methods
- EDA: descriptive statistics and missingness
- Kaplan-Meier: overall survival curve and survival probabilities at selected times
- Cox PH model: covariates age, sex, biomarker, treatment (treatment_B indicator)
- PH test: lifelines' proportional_hazard_test

## 4. Results (fill after running run_analysis_full.py)
- See results/ for generated text deliverables and plots.

## 5. Interpretation guidance
- Report hazard ratios with 95% CI and p-values
- Discuss clinical relevance and potential confounding
- If PH assumption violated: consider stratification or time-varying effects

## 6. Reproducibility
- Script is deterministic for provided simulated data.
