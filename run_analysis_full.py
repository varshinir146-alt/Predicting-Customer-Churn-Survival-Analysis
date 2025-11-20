"""
run_analysis_full.py

Full reproducible analysis script for the survival analysis project.
Generates EDA, Kaplan-Meier estimates, Cox proportional hazards model, PH test, and writes textual deliverables.

Requirements:
    pip install pandas numpy matplotlib lifelines

Usage:
    python run_analysis_full.py --input simulated_survival_data.csv --outdir results

Outputs (in results/):
    - eda_summary.txt
    - km_estimates.txt
    - km_plot.png
    - cox_summary.txt
    - ph_test.txt
    - final_interpretation.txt

This script is written to be runnable end-to-end.
"""
import os, argparse
import pandas as pd
import numpy as np

def safe_import_lifelines():
    try:
        import lifelines
        from lifelines import KaplanMeierFitter, CoxPHFitter
        return KaplanMeierFitter, CoxPHFitter, None
    except Exception as e:
        return None, None, e

def generate_eda(df, outdir):
    eda_file = os.path.join(outdir, "eda_summary.txt")
    with open(eda_file, "w") as f:
        f.write("EDA Summary\n")
        f.write("="*40 + "\n\n")
        f.write("Dataset shape: {} rows, {} columns\n\n".format(df.shape[0], df.shape[1]))
        f.write("Column types and missing values:\n")
        f.write(str(df.dtypes) + "\n\n")
        f.write("Missing values per column:\n")
        f.write(str(df.isnull().sum()) + "\n\n")
        f.write("Descriptive statistics (numeric):\n")
        f.write(str(df.describe()) + "\n\n")
        f.write("Event distribution:\n")
        events = df['event'].value_counts().to_dict()
        f.write(str(events) + "\n\n")
        f.write("Event rate: {:.2f}%\n".format(100*df['event'].mean()))
    return eda_file

def run_kaplan_meier(df, outdir):
    KMF, _, err = safe_import_lifelines()
    km_file = os.path.join(outdir, "km_estimates.txt")
    plot_file = os.path.join(outdir, "km_plot.png")
    if KMF is None:
        with open(km_file, "w") as f:
            f.write("lifelines not available. Install lifelines to compute Kaplan-Meier estimates.\n")
            f.write("pip install lifelines\n")
        return km_file, plot_file, "lifelines_missing"
    from lifelines import KaplanMeierFitter
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    with open(km_file, "w") as f:
        f.write("Kaplan-Meier estimates (summary)\n")
        f.write("="*40 + "\n\n")
        f.write(str(kmf.event_table.head(50)) + "\n\n")
        # show survival probs at selected times
        times_to_report = [1,3,6,12,24,36]
        f.write("Survival probabilities at times (units same as 'time'):\n")
        for t in times_to_report:
            try:
                s = kmf.predict(t)
                f.write("  time {}: {:.4f}\n".format(t, s))
            except Exception:
                f.write("  time {}: NA\n".format(t))
    # save simple plot
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6,4))
        kmf.plot_survival_function()
        plt.title("Kaplan-Meier Survival Curve")
        plt.xlabel("Time")
        plt.ylabel("Survival Probability")
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.close()
    except Exception as e:
        # ignore plotting errors
        pass
    return km_file, plot_file, None

def run_cox_model(df, outdir):
    _, CoxPHFitter, err = safe_import_lifelines()
    cox_file = os.path.join(outdir, "cox_summary.txt")
    ph_file = os.path.join(outdir, "ph_test.txt")
    if CoxPHFitter is None:
        with open(cox_file, "w") as f:
            f.write("lifelines not available. Install lifelines to run CoxPH.\n")
            f.write("pip install lifelines\n")
        with open(ph_file, "w") as f:
            f.write("lifelines not available. Install lifelines to run PH tests.\n")
        return cox_file, ph_file, "lifelines_missing"
    from lifelines import CoxPHFitter
    df2 = df.copy()
    # prepare categorical encoding for treatment and sex
    df2['sex'] = df2['sex'].astype(int)
    df2 = pd.get_dummies(df2, columns=['treatment'], drop_first=True)
    covariates = ['age','sex','biomarker','treatment_B']
    cph = CoxPHFitter()
    cph.fit(df2[['time','event']+covariates], duration_col='time', event_col='event', show_progress=False)
    with open(cox_file, "w") as f:
        f.write("Cox Proportional Hazards Model Summary\n")
        f.write("="*60 + "\n\n")
        f.write(cph.summary.to_string())
    # proportional hazards test
    try:
        from lifelines.statistics import proportional_hazard_test
        results = proportional_hazard_test(cph, df2, time_transform='rank')
        with open(ph_file, "w") as f:
            f.write("Proportional Hazards Test (lifelines)\n")
            f.write("="*60 + "\n\n")
            f.write(str(results.summary))
    except Exception as e:
        with open(ph_file, "w") as f:
            f.write("PH test failed or lifelines version doesn't support proportional_hazard_test.\n")
            f.write("Error: " + str(e) + "\n")
    return cox_file, ph_file, None

def write_final_interpretation(outdir):
    fi = os.path.join(outdir, "final_interpretation.txt")
    text = """
Final interpretation guidance (to be filled after running the analysis):
- Summarize the main results from EDA: data shape, event rate, notable imbalances.
- Report Kaplan-Meier survival probabilities at clinically meaningful times (e.g., 6, 12, 24 months).
- For the Cox model report: hazard ratios, 95% CIs, p-values for top predictors.
- State whether PH assumption holds; if violated, mention alternative approaches (stratified Cox, time-varying covariates).
- Provide a concise conclusion: e.g., "Treatment B is associated with a X% reduction in hazard (HR=..., 95%CI=..., p=...). Age and biomarker were associated with increased hazard."
    """
    with open(fi, "w") as f:
        f.write(text.strip())
    return fi

def main(args):
    df = pd.read_csv(args.input)
    os.makedirs(args.outdir, exist_ok=True)
    eda = generate_eda(df, args.outdir)
    km = run_kaplan_meier(df, args.outdir)
    cox = run_cox_model(df, args.outdir)
    fi = write_final_interpretation(args.outdir)
    print("Analysis complete. Outputs in:", args.outdir)
    print("EDA:", eda)
    print("KM:", km)
    print("Cox and PH:", cox)
    print("Final interpretation template:", fi)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='input CSV file path')
    parser.add_argument('--outdir', default='results', help='output directory')
    args = parser.parse_args()
    main(args)
