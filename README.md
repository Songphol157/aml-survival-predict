Acute Myeloid Leukemia Survival Prediction

Copyright (c) 2026 Songphol Tungjitviboonkun, MD, MS

DOI License: MIT

Live tool: https://aml-survival-predict.com

⚠️ Prototype only. This tool is for research and demonstration purposes and is not intended for clinical decision-making. It has not been prospectively validated and should not be used to guide the care of individual patients.

Background

Acute myeloid leukemia requires treatment decisions to be made within days of diagnosis, before a patient's response to therapy is known. The choice between intensive chemotherapy, lower-intensity therapy, and referral for allogeneic transplant depends on an estimate of prognosis made at presentation, from the clinical and genetic information available at that moment.

This project develops and validates machine learning survival models for adult AML that integrate routinely available clinical and genomic variables into individualized survival estimates, and makes those estimates freely accessible through a public web interface.

What the model does

Given the following inputs, the model returns an individualized survival probability curve and tabulated survival estimates at fixed time points:

Input	Values

Age at diagnosis	18–88 years

Sex	Male / Female

ELN 2017 risk category	Favorable / Intermediate / Adverse

Disease type	De novo / Secondary

Cytogenetics	Normal / Complex

FLT3-ITD mutation	Positive / Negative

NPM1 mutation	Positive / Negative

RUNX1 mutation	Positive / Negative

Methods

Three survival modelling approaches were developed and compared:

Random survival forest (RSF)

Cox proportional hazards regression

Gradient boosting machine (GBM) for survival

Model performance was assessed using Harrell's C-index, time-dependent AUROC, and the Brier score, capturing discrimination at a single summary level, discrimination across the follow-up period, and overall calibration and accuracy respectively.

Missing values in the input variables were imputed using the median of the observed values. Right-censoring was handled natively by each of the three survival methods.

Internal validation used bootstrap resampling and 5-fold cross-validation to estimate out-of-sample performance and to guard against overfitting.

Presentations

Development and Validation of Machine Learning Models for Survival Prediction in Adult Acute Myeloid Leukemia (ML-AML) — accepted for poster presentation, ESMO Congress 2026, Madrid, 23–27 October 2026 (abstract #1443).

Best Statistical & Computational Methods Abstract, UCSF Department of Epidemiology & Biostatistics Student Research Day, 19 May 2026.

Citation

If you use this software, please cite:

Tungjitviboonkun S. AML Survival Predict: machine learning survival prediction for adult acute myeloid leukemia. Zenodo. https://doi.org/10.5281/zenodo.22717853

License

Released under the MIT License. You are free to use, modify and distribute this software, including for commercial purposes, provided the copyright notice and licence text are retained. See LICENSE for the full terms.

Author

Songphol Tungjitviboonkun, MD, MS (also publishes as Steve Tungjitviboonkun) Department of Epidemiology and Biostatistics University of California, San Francisco

Contributing

Issues and pull requests are welcome. For questions about the model or the underlying research, please open an issue.
