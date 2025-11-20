# Survival Analysis Project - Complete Package

This folder contains a fully-documented survival analysis project with simulated data and ready-to-run code.

**Contents**
- simulated_survival_data.csv  (the dataset)
- run_analysis_full.py        (analysis script)
- eda_summary.txt             (template / generated after running the script)
- km_estimates.txt            (template / generated after running the script)
- cox_summary.txt             (template / generated after running the script)
- ph_test.txt                 (template / generated after running the script)
- final_interpretation.txt    (interpretation guidance template)
- report.md                   (project report template)
- survival_project_complete.zip  (this zip file)

## How to run (simple)

1. Create a Python environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install --upgrade pip
   pip install pandas numpy matplotlib lifelines
   ```

2. Run the analysis:
   ```bash
   python run_analysis_full.py --input simulated_survival_data.csv --outdir results
   ```

3. Check the `results/` directory for textual deliverables and plots.

## Notes on reproducibility
- The simulated dataset is reproducible (seed fixed).
- The analysis script tries to create readable, required text deliverables exactly as requested by the project instructions (EDA summary, KM estimates, Cox model summary, PH test, final interpretation template).

If you want me to run the analysis here and produce the actual output files (km_estimates, cox_summary), say **"Run analysis here"** and I will attempt to run it (may require installing `lifelines` in this environment).
