# Loan Approval Prediction: Bagging vs. Boosting

**Group 10 · B.Tech Computer Science and Engineering (Artificial Intelligence & Machine Learning)**

An academic machine-learning project comparing ensemble classification methods on a loan-approval dataset. The project includes a multi-page Streamlit app, a saved prediction pipeline, an experiment runner, local SHAP explanations, and optional Gemini-generated narration.

[![Open the Streamlit app](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://loan-approval-prediction-bagging-vs-boosting.streamlit.app)
[![Python quality checks](https://github.com/A5hutosh9/Loan-Approval-Prediction--Bagging-versus-Boosting/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/A5hutosh9/Loan-Approval-Prediction--Bagging-versus-Boosting/actions/workflows/ci.yml)

**Live app:** <https://loan-approval-prediction-bagging-vs-boosting.streamlit.app>

> **Academic-use notice:** This is an educational prototype, not a bank, credit bureau, underwriting system, or financial-advice service. Do not use its predictions to approve, reject, price, rank, or otherwise make decisions about real loan applicants.

## Contents

- [Project overview](#project-overview)
- [What the app includes](#what-the-app-includes)
- [Dataset](#dataset)
- [Reported model comparison](#reported-model-comparison)
- [How the experiment runner works](#how-the-experiment-runner-works)
- [Prediction explanations](#prediction-explanations)
- [Repository structure](#repository-structure)
- [Run locally](#run-locally)
- [Optional Gemini configuration](#optional-gemini-configuration)
- [Run quality checks](#run-quality-checks)
- [Limitations and reproducibility](#limitations-and-reproducibility)
- [Responsible use and security](#responsible-use-and-security)

## Project overview

The project studies how **Bagging** and **Boosting** behave on a binary loan-status classification task. The Streamlit app is organised around four activities:

1. **Ensemble comparison** — learn the difference between Bagging and Boosting and review the project's reported model metrics.
2. **Experiment runner** — upload a binary-classification CSV and evaluate five classifiers using stratified cross-validation.
3. **Loan prediction** — enter the 11 applicant features expected by the saved model and inspect its prediction and probability estimates.
4. **Fairness review** — view the predefined education and self-employment group comparisons, with their limitations clearly stated.

The interface uses a shared dark Emerald Glass theme and responsive layouts for desktop and mobile screens.

## What the app includes

| Area | Description |
|---|---|
| Dataset overview | Previews the bundled CSV and displays basic column and missing-value information |
| Ensemble comparison | Explains Bagging and Boosting and displays the reported results for five models |
| Experiment runner | Uploads a CSV, prepares features, runs stratified cross-validation, and reports evaluation metrics and ROC curves |
| Loan prediction | Loads `loan_model.pkl` to predict a class and return model probability estimates |
| Local explainability | Calculates model-agnostic SHAP permutation attributions for an individual prediction |
| Optional AI narration | Uses Gemini to explain measured SHAP contributions or uploaded-experiment metrics |

## Dataset

The bundled file is `loan_approval_dataset.csv`. The application describes it as **4,269 rows × 13 columns**.

The prediction interface uses these 11 attributes:

- Number of dependents
- Education
- Self-employment status
- Annual income
- Loan amount and loan term
- CIBIL score
- Residential, commercial, and luxury asset values
- Bank asset value

The target is `loan_status` (Approved / Rejected). The source CSV also contains an identifier column; identifiers should not be treated as predictive financial characteristics.

**Dataset source:** [Loan Approval Prediction Dataset by Archit Sharma on Kaggle](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset). The repository CSV has the same 4,269-row, 13-column schema and loan fields documented for this source. The Kaggle dataset page's licence metadata was not independently verifiable during this review, so check the current Kaggle page and comply with its displayed terms before redistributing the data.\n\n**Data-quality check:** the committed CSV contains 2,656 Approved and 1,613 Rejected records. A scan found 28 negative values in `residential_assets_value` (minimum: -100,000). Do not silently replace these values: verify the source's meaning and document any cleaning decision before retraining or interpreting the model.

## Reported model comparison

The Ensemble Methods page currently displays these **reported validation values**:

| Model | Validation accuracy | Validation F1 | Validation ROC-AUC |
|---|---:|---:|---:|
| Decision Tree | 0.9782 | 0.9825 | 0.9771 |
| Bagging | 0.9843 | 0.9875 | 0.9975 |
| Random Forest | 0.9796 | 0.9837 | 0.9967 |
| AdaBoost | 0.9590 | 0.9669 | 0.9948 |
| Gradient Boosting | 0.9803 | 0.9843 | 0.9981 |

These values are embedded in `pages/1_Bagging_vs_Boosting.py`; they are **not recalculated** when the page opens. The separate Run Experiment page computes new metrics for the CSV uploaded by the user. Do not assume the two result sources are directly comparable without reproducing the original evaluation setup.

The table is not evidence of performance on unseen real-world lending populations.

## How the experiment runner works

For an uploaded CSV, the application:

1. lets the user select a binary target column;
2. maps common labels such as Approved/Rejected, Yes/No, 1/0, and True/False to class labels;
3. removes recognised identifier columns and columns that are completely empty;
4. imputes numerical values with the median;
5. imputes categorical values with the most frequent value and applies one-hot encoding;
6. evaluates Decision Tree, Bagging, Random Forest, AdaBoost, and Gradient Boosting using stratified cross-validation; and
7. reports accuracy, F1, ROC-AUC, train/validation gaps, and cross-validated ROC curves.

A fixed random seed is used to improve repeatability for a fixed dataset and software environment. Cross-validation on an uploaded dataset is not a substitute for independent external validation.

## Prediction explanations

The prediction page can calculate a local **SHAP permutation explanation** for the saved model pipeline. The full preprocessing/model pipeline is treated as a black-box probability function; the explanation does not assume that the serialized artifact is a particular tree estimator.

The calculation uses a deterministic reference sample of up to 40 rows from the bundled dataset. Categorical inputs are encoded for SHAP's masking operation and converted back to their original text values before the model is called. The app checks that the baseline plus the feature contributions approximately reconciles with the model's approval-probability output.

Gemini is an optional narration layer. It explains the measured SHAP contributions; it does not make the prediction. If Gemini is not configured or an API request fails, the app can still show a local SHAP summary and contribution table.

SHAP values describe how this model behaves relative to its reference data. They are not proof of causation, lending policy, or the real-world reasons an applicant should be approved or rejected. Correlated features can share attribution, and the result depends on the reference records and approximation settings.

## Repository structure

```text
.
├── app.py                           # Streamlit home page and project overview
├── pages/
│   ├── 1_Bagging_vs_Boosting.py     # Ensemble concepts and reported metrics
│   ├── 2_Run_Experiment.py          # CSV upload, preprocessing, training and evaluation
│   ├── 3_Loan_Prediction.py         # Prediction using the saved model artifact
│   └── 5_Fairness_Analysis.py       # Predefined education and employment comparisons
├── ui_theme.py                      # Shared styling, sidebar branding and UI components
├── utils.py                         # Dataset loading and binary-target utilities
├── ai_explainer.py                  # Optional Gemini explanation helper
├── model_explainer.py               # Local model-agnostic SHAP explanations
├── loan_approval_dataset.csv        # Bundled project dataset
├── loan_model.pkl                   # Serialized prediction model/pipeline
├── requirements.txt                 # Application dependencies
├── requirements-dev.txt             # Application dependencies plus test tools
├── MODEL_CARD.md                    # Intended use, methodology and model limitations
├── SECURITY.md                      # API-key and applicant-data guidance
├── tests/
│   ├── test_utils.py                # Binary-target normalisation tests
│   └── test_model_explainer.py       # SHAP explanation tests
├── .devcontainer/
│   └── devcontainer.json            # VS Code / GitHub Codespaces environment
├── .github/
│   └── workflows/
│       └── ci.yml                   # Compile and test checks on GitHub Actions
├── pytest.ini                       # Pytest discovery and import configuration
├── .streamlit/
│   ├── config.toml                  # Streamlit theme configuration
│   └── secrets.toml.example         # Safe local Gemini secrets template
└── .gitignore                       # Excludes secrets, caches and local files
```

The current flat layout is intentional for this small Streamlit project: the shared modules sit beside `app.py`, so page imports stay simple. A larger application could later introduce a package structure, but moving files now would add risk without a clear benefit.

## Run locally

**Python 3.11 is used by the repository's GitHub Actions checks.**

### 1. Clone the repository

```bash
git clone https://github.com/A5hutosh9/Loan-Approval-Prediction--Bagging-versus-Boosting.git
cd Loan-Approval-Prediction--Bagging-versus-Boosting
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install application dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the app

```bash
python -m streamlit run app.py
```

Open the local URL printed by Streamlit (usually <http://localhost:8501>).

## Optional Gemini configuration

Gemini is used only for natural-language explanations. The saved ML model performs the prediction, and the app remains usable without a Gemini API key.

For the deployed Streamlit Community Cloud app:

1. Open the app's **Settings → Secrets** panel.
2. Add this TOML entry:

   ```toml
   GEMINI_API_KEY = "your-private-api-key"
   ```

3. Save the secret and allow the app to restart.

For local use, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder with your key. The real secrets file is excluded by `.gitignore`.

**Privacy note:** When a user requests a Gemini explanation on the Loan Prediction page, the entered applicant feature values and model output are sent to Google's Gemini API. Use synthetic demonstration data only. Never enter real names, identity numbers, account details, or real financial records. See [SECURITY.md](SECURITY.md).

Gemini is subject to provider availability, account limits, and applicable pricing. An API key does not guarantee unlimited or uninterrupted access. If Gemini is unavailable, the local prediction and SHAP explanation remain separate from the optional narration.

## Run quality checks

Install the development dependencies (this also installs the application dependencies):

```bash
python -m pip install -r requirements-dev.txt
```

Then run:

```bash
python -m compileall -q app.py ai_explainer.py model_explainer.py utils.py ui_theme.py pages
python -m pytest -q
```

GitHub Actions runs the same compile and test checks for pushes and pull requests to `main`. The test suite covers binary-target normalisation and the local SHAP explanation logic.

## Limitations and reproducibility

- **Saved model:** `loan_model.pkl` is included, but the repository does not contain a complete training script or notebook that recreates it from the raw CSV. The exact training split, estimator configuration, and artifact-generation steps therefore cannot be fully reproduced from this repository alone.
- **Comparison results:** the model-comparison values are hard-coded reported figures, not freshly generated results.
- **Fairness page:** the group-level values are predefined in `pages/5_Fairness_Analysis.py`; they are not dynamically recalculated from the CSV on each page load. Treat them as descriptive reported figures, not a completed or independently validated fairness audit.
- **External validation:** no independent external test-set results, confidence intervals, calibration analysis, or validation on another applicant population are documented.
- **Dataset documentation:** original dataset provenance and redistribution permissions still need to be verified.
- **Serialized model security:** only load the pickle/joblib artifact from a trusted source and use compatible dependency versions.

A more complete future research release should document the dataset source and licence, add a reproducible training pipeline, regenerate the reported metrics from a clearly defined evaluation protocol, and calculate subgroup fairness metrics dynamically with sample sizes and uncertainty estimates.

## Responsible use and security

This project is intended for classroom demonstration of supervised learning, ensemble methods, model evaluation, and responsible interpretation of ML outputs.

- Do not use it to make real credit or lending decisions.
- Do not interpret a model probability as a calibrated probability of repayment or approval in a different population.
- Group differences do not, by themselves, establish discrimination or explain its cause.
- Keep API keys out of source code, commits, screenshots, and issue reports.
- Use synthetic data for demonstrations and optional Gemini explanations.

For more detail, read [MODEL_CARD.md](MODEL_CARD.md) and [SECURITY.md](SECURITY.md).

---

**Project:** Loan Approval Prediction — Bagging vs. Boosting  
**Group:** Group 10  
**Programme:** B.Tech CSE (AIML)
