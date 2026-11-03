# Loan Approval Prediction: Bagging vs. Boosting

**Group 10 | B.Tech Computer Science and Engineering (Artificial Intelligence & Machine Learning)**

An academic machine-learning project that studies ensemble classification methods on a loan-approval dataset and presents the results through an interactive Streamlit application.

> **Academic-use notice:** This repository is an educational prototype. It is not a bank, credit bureau, underwriting system, or financial-advice service. Its predictions must not be used to approve, reject, price, or otherwise make decisions about real loan applicants.

## Project overview

The project explores how **Bagging** and **Boosting** approaches behave on a binary loan-status classification task. The repository includes a saved prediction pipeline, a dataset, a multi-page Streamlit interface, an experiment workflow for uploaded CSV files, and an optional Gemini-powered explanation layer.

The application is organised around four main activities:

1. **Understand ensemble learning** — compare the concepts and reported validation metrics for Decision Tree, Bagging, Random Forest, AdaBoost, and Gradient Boosting.
2. **Run an experiment** — upload a binary-classification CSV, select a target, and evaluate five classifiers using stratified cross-validation.
3. **Explore a prediction** — enter applicant attributes and obtain a prediction from the saved model artifact.
4. **Review group metrics** — inspect the education and self-employment comparisons included in the fairness page.

The interface uses a shared, high-contrast glass visual theme and is designed to adapt to desktop and mobile screens.

## Application capabilities

| Area | What it does |
|---|---|
| Dataset overview | Displays the repository dataset and basic column/missing-value information |
| Ensemble comparison | Explains Bagging and Boosting and shows the project's reported model metrics |
| Experiment runner | Performs preprocessing, stratified cross-validation, metric reporting, ROC curves, and CSV export for an uploaded dataset |
| Loan prediction | Uses `loan_model.pkl` to generate a class prediction and probability estimates from entered features |
| AI explanation | Optionally uses the Gemini API to explain experiment or prediction outputs |
| Fairness analysis | Displays group-level metrics for education and self-employment categories |

## Dataset

The application describes the bundled dataset as **4,269 records and 13 columns**. The prediction interface uses the following applicant attributes:

- Number of dependents
- Education
- Self-employment status
- Annual income
- Loan amount and loan term
- CIBIL score
- Residential, commercial, and luxury asset values
- Bank asset value

The target is `loan_status` (Approved / Rejected). The source dataset also contains an identifier column; identifiers should not be treated as predictive financial characteristics.

**Dataset provenance:** The repository currently contains the CSV but does not document its original publisher, download location, or redistribution terms. Those details should be verified and cited before the dataset is reused or redistributed outside this academic project.

## Reported model comparison

The Ensemble Methods page displays the following **reported validation values**:

| Model | Validation accuracy | Validation F1 | Validation ROC-AUC |
|---|---:|---:|---:|
| Decision Tree | 0.9782 | 0.9825 | 0.9771 |
| Bagging | 0.9843 | 0.9875 | 0.9975 |
| Random Forest | 0.9796 | 0.9837 | 0.9967 |
| AdaBoost | 0.9590 | 0.9669 | 0.9948 |
| Gradient Boosting | 0.9803 | 0.9843 | 0.9981 |

These are the values currently encoded in `pages/1_Bagging_vs_Boosting.py`; they are presented as previously reported project results, not as a fresh execution performed when the page opens. The separate **Run Experiment** page computes new metrics for the dataset uploaded by the user. Results can vary with the data, feature handling, class distribution, validation design, and model configuration. The table alone is not evidence of performance on unseen real-world lending populations.

## Method used by the experiment runner

For an uploaded CSV, the application:

1. lets the user select a binary target column;
2. normalises common binary target labels;
3. removes recognised identifier columns and completely empty columns;
4. imputes numerical values with the median;
5. imputes categorical values with the most frequent value and applies one-hot encoding;
6. evaluates Decision Tree, Bagging, Random Forest, AdaBoost, and Gradient Boosting with stratified cross-validation; and
7. reports accuracy, F1, ROC-AUC, train/validation gaps, and cross-validated ROC curves.

The experiment page uses a fixed random seed for its cross-validation and model initialisation. This improves repeatability for a fixed software environment and input dataset, but it does not replace a separate external test set or independent replication.

## Repository structure

```text
.
├── app.py                         # Streamlit home page and project overview
├── pages/
│   ├── 1_Bagging_vs_Boosting.py   # Ensemble concepts and reported comparison
│   ├── 2_Run_Experiment.py        # Upload, preprocess, train, and evaluate models
│   ├── 3_Loan_Prediction.py       # Prediction using the saved model artifact
│   └── 5_Fairness_Analysis.py    # Education and employment group comparisons
├── ai_explainer.py                # Shared Gemini API helper for optional explanations
├── utils.py                       # Dataset loading and target-label utilities
├── ui_theme.py                    # Shared application styling and UI components
├── loan_approval_dataset.csv      # Dataset used by the project
├── loan_model.pkl                 # Serialized prediction model/pipeline
├── requirements.txt               # Pinned runtime dependencies\n├── requirements-dev.txt           # Test dependencies\n├── tests/\n│   └── test_utils.py               # Binary-target normalization tests\n├── .github/workflows/ci.yml        # Compile and unit-test checks
└── .streamlit/
    └── config.toml                # Streamlit visual theme
```

**Reproducibility note:** The saved model artifact is included, but a dedicated training script or notebook that recreates `loan_model.pkl` from the raw dataset is not currently included. The exact training procedure and artifact-generation steps should be added to the repository if full model-training reproducibility is required.

## Run locally

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
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the Streamlit application

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) in the terminal.

## Optional Gemini API configuration

Gemini is used only for natural-language explanations; the saved ML model performs the prediction. The application can still show the model result without a Gemini key. If Gemini is unavailable or its quota is exhausted, the AI explanation is skipped and the already-generated model prediction remains visible.

For a deployed Streamlit Community Cloud app:

1. Open the app's **Settings → Secrets** panel.
2. Add the following TOML entry:

   ```toml
   GEMINI_API_KEY = "your-private-api-key"
   ```

3. Save the secret and allow the app to restart.

For local testing, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder. **Never commit the real secrets file, paste an API key into source code, or publish it in an issue or screenshot.** The repository's `.gitignore` excludes the local secrets file. See [SECURITY.md](SECURITY.md) for the data-handling notes.

Gemini explanations are generated only after the user presses the explanation button. On the prediction page, the entered applicant features and model output are sent to Google's Gemini API for that explanation. Use synthetic demonstration data only. Gemini requests are subject to provider availability, account limits, and applicable pricing; an API key does not guarantee indefinite availability or unlimited use.

## Important interpretation and limitations

- The prediction is a model output, not a real credit decision or a recommendation.
- A model probability is not necessarily a calibrated probability of repayment or approval in a different population.
- The comparison values are reported values embedded in the comparison page. They should be independently reproduced before being treated as verified findings.
- The fairness page currently displays predefined group-level metric values. It does **not** recalculate those metrics dynamically from the CSV on each page load; treat them as descriptive project figures, not a completed or independently validated fairness audit.
- Group differences do not by themselves establish discrimination or explain their cause. A proper fairness assessment needs validated calculations, sample-size and uncertainty analysis, contextual review, and relevant legal/domain expertise.
- The repository does not currently provide documented dataset provenance or a complete training script for recreating the saved model.
- The serialized `.pkl` model should only be loaded from a trusted source and with compatible dependency versions.

## Technical stack

- Python
- Streamlit
- pandas and NumPy
- scikit-learn
- Matplotlib
- Joblib
- SHAP (listed as a project dependency)
- Google Gen AI SDK (optional Gemini explanations)

## Academic context

**Project:** Loan Approval Prediction — Bagging vs. Boosting  
**Group:** Group 10  
**Programme:** B.Tech CSE (AIML)

The repository is maintained as an academic demonstration of supervised learning, ensemble methods, model evaluation, and responsible interpretation of ML outputs.


## Quality checks

The repository includes unit tests for binary-target encoding and a GitHub Actions workflow that compiles the Python source files and runs the tests on Python 3.11.

Run the checks locally with:

```bash
pip install -r requirements-dev.txt
python -m compileall -q app.py ai_explainer.py utils.py ui_theme.py pages
pytest -q
```

The test suite checks that numeric 0/1 labels keep their intended meaning, recognised approval/rejection labels map consistently, missing targets remain missing, and invalid single-class targets are rejected.
