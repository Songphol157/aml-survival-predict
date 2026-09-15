#master project/
#├── data/
#├── script/
#├── output/
#│   ├── models/
#│   │   └── gbm_model.joblib
#│   └── figures/
#└── webpage/
#    ├── app.py
#    └── index.html

from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
import os
import json
import threading

app = Flask(__name__, template_folder='.')

# Load model (relative to webpage/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "output", "models", "rsf_model.joblib")
model = joblib.load(MODEL_PATH)

# Persistent visitor counter (survives restarts; simple file-based store)
VISIT_COUNT_PATH = os.path.join(BASE_DIR, "..", "output", "visit_count.json")
_visit_lock = threading.Lock()


def _read_visit_count():
    try:
        with open(VISIT_COUNT_PATH, "r") as f:
            return int(json.load(f).get("count", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 0


def _write_visit_count(count):
    os.makedirs(os.path.dirname(VISIT_COUNT_PATH), exist_ok=True)
    with open(VISIT_COUNT_PATH, "w") as f:
        json.dump({"count": count}, f)

FEATURES = model.feature_names_in_ if hasattr(model, "feature_names_in_") else None

def preprocess_input(features_dict):
    def to_binary_mutation(v):
        # frontend sends 1 = Positive, 0 = Negative, -1 = Unknown
        if v == 1 or v == "1":
            return 1
        if v == 0 or v == "0":
            return 0
        return np.nan

    def map_sex(v):
        v = str(v).strip().lower()
        if v == "male":
            return 1
        if v == "female":
            return 0
        return np.nan

    def map_chromosome(v):
        v = str(v).strip().lower()
        if v == "normal":
            return 1
        if v == "complex":
            return 0
        return np.nan

    def map_denovo(v):
        v = str(v).strip().lower()
        if v == "de novo":
            return 1
        if v == "therapy-related":
            return 0
        return np.nan

    def map_eln(v):
        v = str(v).strip().lower()
        return {"favorable": 0, "intermediate": 1, "adverse": 2}.get(v, np.nan)

    row = pd.DataFrame([{
        "age_at_diagnosis": pd.to_numeric(features_dict.get("age"), errors="coerce"),
        "eln2017mode": map_eln(features_dict.get("eln2017")),
        "sex_male": map_sex(features_dict.get("sex")),
        "chromosome_cat_normal": map_chromosome(features_dict.get("chromosome")),
        "denovo_cat_true": map_denovo(features_dict.get("disease_type")),
        "flt3_itd_cat_positive": to_binary_mutation(features_dict.get("flt3_itd_cat")),
        "npm1_cat_positive": to_binary_mutation(features_dict.get("npm1_cat")),
        "runx1_cat_positive": to_binary_mutation(features_dict.get("runx1_cat")),
        "asxl1_cat_positive": to_binary_mutation(features_dict.get("asxl1_cat")),
        "tp53_cat_positive": to_binary_mutation(features_dict.get("tp53_cat")),
    }])

    row = row.reindex(columns=FEATURES, fill_value=0)
    row = row.apply(pd.to_numeric, errors="coerce").fillna(0)

    return row


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = data["features"]

        X = preprocess_input(features)
        surv_func = model.predict_survival_function(X)[0]

        times = np.arange(0, 26)
        survival = []

        for t in times:
            idx = np.searchsorted(surv_func.x, t, side="right") - 1
            if idx < 0:
                survival.append(1.0)
            else:
                survival.append(float(surv_func.y[idx]))

        return jsonify({
            "times": times.tolist(),
            "survival": survival,
            "percent_months": times.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/visit", methods=["POST"])
def visit():
    with _visit_lock:
        count = _read_visit_count() + 1
        _write_visit_count(count)
    return jsonify({"count": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
