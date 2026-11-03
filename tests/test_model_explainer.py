import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from model_explainer import (
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    build_local_explanation_summary,
    compute_local_shap_explanation,
)


def _fit_test_model():
    rng = np.random.default_rng(17)
    rows = 100
    frame = pd.DataFrame(
        {
            "no_of_dependents": rng.integers(0, 5, rows),
            "education": rng.choice(["Graduate", "Not Graduate"], rows),
            "self_employed": rng.choice(["Yes", "No"], rows),
            "income_annum": rng.integers(500_000, 10_000_000, rows),
            "loan_amount": rng.integers(100_000, 30_000_000, rows),
            "loan_term": rng.integers(5, 30, rows),
            "cibil_score": rng.integers(300, 900, rows),
            "residential_assets_value": rng.integers(0, 10_000_000, rows),
            "commercial_assets_value": rng.integers(0, 10_000_000, rows),
            "luxury_assets_value": rng.integers(0, 10_000_000, rows),
            "bank_asset_value": rng.integers(0, 10_000_000, rows),
        }
    )
    target = (
        (frame["cibil_score"] > 600) & (frame["income_annum"] > 3_000_000)
    ).astype(int)
    preprocess = ColumnTransformer(
        [
            ("numeric", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    model = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", RandomForestClassifier(n_estimators=25, random_state=17)),
        ]
    )
    model.fit(frame[FEATURE_COLUMNS], target)
    return model, frame


def test_shap_explanation_reconciles_with_saved_pipeline_probability():
    model, reference = _fit_test_model()
    applicant = pd.DataFrame(
        [
            {
                "no_of_dependents": 2,
                "education": "Graduate",
                "self_employed": "No",
                "income_annum": 1_000_000,
                "loan_amount": 5_000_000,
                "loan_term": 12,
                "cibil_score": 500,
                "residential_assets_value": 200_000,
                "commercial_assets_value": 0,
                "luxury_assets_value": 0,
                "bank_asset_value": 100_000,
            }
        ]
    )

    details = compute_local_shap_explanation(
        model, applicant, reference, background_size=20, permutations=2
    )

    assert len(details["features"]) == len(FEATURE_COLUMNS)
    assert details["additivity_error"] < 0.02
    assert np.isclose(
        details["base_probability"] + sum(item["impact"] for item in details["features"]),
        details["model_probability"],
        atol=0.02,
    )
    summary = build_local_explanation_summary(details)
    assert "SHAP contributions" in summary
    assert "not proof of cause" in summary


def test_shap_explanation_accepts_padded_csv_categories():
    model, reference = _fit_test_model()
    reference["education"] = reference["education"].map(lambda value: f" {value} ")
    reference["self_employed"] = reference["self_employed"].map(lambda value: f" {value} ")
    applicant = reference[FEATURE_COLUMNS].iloc[[0]].copy()
    applicant["education"] = applicant["education"].str.strip()
    applicant["self_employed"] = applicant["self_employed"].str.strip()

    details = compute_local_shap_explanation(
        model, applicant, reference, background_size=20, permutations=1
    )
    assert len(details["features"]) == len(FEATURE_COLUMNS)
    assert details["additivity_error"] < 0.02
