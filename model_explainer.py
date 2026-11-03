"""Model-agnostic, local SHAP explanations for the saved loan pipeline.

The complete sklearn pipeline is treated as a black box. Categorical values are
encoded only for SHAP's numeric masker, then decoded before calling the model.
This keeps the model's original preprocessing inside the prediction pipeline.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]

NUMERIC_FEATURES = [
    "no_of_dependents",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]
CATEGORICAL_FEATURES = ["education", "self_employed"]

FEATURE_LABELS = {
    "no_of_dependents": "Number of dependents",
    "education": "Education",
    "self_employed": "Self-employment",
    "income_annum": "Annual income",
    "loan_amount": "Requested loan amount",
    "loan_term": "Loan term",
    "cibil_score": "CIBIL score",
    "residential_assets_value": "Residential assets",
    "commercial_assets_value": "Commercial assets",
    "luxury_assets_value": "Luxury assets",
    "bank_asset_value": "Bank assets",
}


def _approval_class_index(model) -> int:
    """Find the class representing Approved / positive class in model.classes_."""
    classes = list(getattr(model, "classes_", []))
    if not classes:
        raise ValueError("The saved model does not expose classes_ for its probabilities.")

    for candidate in (1, True, "1", "approved", "approve", "yes", "true"):
        for index, value in enumerate(classes):
            if value == candidate or str(value).strip().lower() == str(candidate).strip().lower():
                return index

    raise ValueError(
        "Could not identify the Approved class in the saved model. "
        f"Model classes are: {classes!r}"
    )


def compute_local_shap_explanation(
    model,
    input_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    *,
    background_size: int = 40,
    permutations: int = 4,
) -> dict:
    """Explain one applicant's approval probability using model-agnostic SHAP.

    The complete model/pipeline is called for each masked sample. SHAP's tabular
    masker requires numeric values, so the two categorical fields are assigned
    stable integer codes for masking and decoded to their original strings before
    prediction. No tree-specific assumptions are made.
    """
    try:
        import shap
    except ImportError as error:  # pragma: no cover - exercised by deployment failure
        raise RuntimeError(
            "The SHAP package is not installed. Add shap==0.50.0 to requirements.txt."
        ) from error

    missing_input = [name for name in FEATURE_COLUMNS if name not in input_data.columns]
    missing_reference = [name for name in FEATURE_COLUMNS if name not in reference_data.columns]
    if missing_input:
        raise ValueError(f"Prediction input is missing columns: {missing_input}")
    if missing_reference:
        raise ValueError(f"Reference dataset is missing columns: {missing_reference}")
    if input_data.empty:
        raise ValueError("No applicant row was supplied for explanation.")

    row = input_data.loc[:, FEATURE_COLUMNS].iloc[[0]].copy()
    reference = reference_data.loc[:, FEATURE_COLUMNS].copy()

    # The UI categories are unpadded. Normalise the CSV's padded text values so
    # the baseline uses the same category labels presented by the input controls.
    for column in CATEGORICAL_FEATURES:
        row[column] = row[column].astype("string").str.strip().fillna("__MISSING__")
        reference[column] = (
            reference[column].astype("string").str.strip().fillna("__MISSING__")
        )
    for column in NUMERIC_FEATURES:
        row[column] = pd.to_numeric(row[column], errors="coerce")
        reference[column] = pd.to_numeric(reference[column], errors="coerce")

    reference = reference.dropna(subset=NUMERIC_FEATURES)
    if reference.empty:
        raise ValueError("The reference dataset has no complete numeric feature rows.")
    if row[NUMERIC_FEATURES].isna().any(axis=None):
        raise ValueError("The applicant input contains a missing or invalid numeric value.")

    # Build categorical maps from the entire reference set plus this applicant,
    # not just the background sample, so masking never invents a category code.
    category_to_code = {}
    code_to_category = {}
    for column in CATEGORICAL_FEATURES:
        categories = sorted(
            set(reference[column].astype(str).tolist())
            | set(row[column].astype(str).tolist())
        )
        category_to_code[column] = {category: index for index, category in enumerate(categories)}
        code_to_category[column] = {index: category for category, index in category_to_code[column].items()}

    def encode(frame: pd.DataFrame) -> np.ndarray:
        encoded = pd.DataFrame(index=frame.index)
        for column in FEATURE_COLUMNS:
            if column in CATEGORICAL_FEATURES:
                encoded[column] = (
                    frame[column].astype("string").fillna("__MISSING__").astype(str)
                    .map(category_to_code[column]).astype(float)
                )
            else:
                encoded[column] = pd.to_numeric(frame[column], errors="coerce").astype(float)
        if encoded.isna().any(axis=None):
            raise ValueError("A feature could not be encoded for the SHAP calculation.")
        return encoded.to_numpy(dtype=float)

    def decode(encoded_values) -> pd.DataFrame:
        values = np.asarray(encoded_values, dtype=float)
        if values.ndim == 1:
            values = values.reshape(1, -1)
        decoded = pd.DataFrame(values, columns=FEATURE_COLUMNS)
        for column in CATEGORICAL_FEATURES:
            integer_codes = np.rint(decoded[column].to_numpy()).astype(int)
            if not np.allclose(decoded[column].to_numpy(), integer_codes, atol=1e-8):
                raise ValueError(f"SHAP generated a non-category value for {column}.")
            inverse = code_to_category[column]
            try:
                decoded[column] = [inverse[int(code)] for code in integer_codes]
            except KeyError as error:
                raise ValueError(f"SHAP generated an unknown category code for {column}.") from error
        for column in NUMERIC_FEATURES:
            decoded[column] = pd.to_numeric(decoded[column], errors="coerce")
        return decoded.loc[:, FEATURE_COLUMNS]

    approval_index = _approval_class_index(model)

    def approval_probability(encoded_values) -> np.ndarray:
        model_input = decode(encoded_values)
        probabilities = np.asarray(model.predict_proba(model_input), dtype=float)
        return probabilities[:, approval_index]

    sample_size = min(max(2, int(background_size)), len(reference))
    background = reference.sample(n=sample_size, random_state=42)
    background_encoded = encode(background)
    applicant_encoded = encode(row)

    explainer = shap.Explainer(
        approval_probability,
        masker=background_encoded,
        algorithm="permutation",
        feature_names=[FEATURE_LABELS[column] for column in FEATURE_COLUMNS],
        seed=42,
    )
    max_evaluations = (2 * len(FEATURE_COLUMNS) + 1) * max(1, int(permutations))
    shap_result = explainer(applicant_encoded, max_evals=max_evaluations, silent=True)

    shap_values = np.asarray(shap_result.values, dtype=float)
    if shap_values.ndim == 2:
        shap_values = shap_values[0]
    if shap_values.ndim != 1 or len(shap_values) != len(FEATURE_COLUMNS):
        raise RuntimeError(
            "SHAP returned an unexpected attribution shape: "
            f"{np.asarray(shap_result.values).shape!r}"
        )

    base_values = np.asarray(shap_result.base_values, dtype=float).reshape(-1)
    if base_values.size == 0:
        raise RuntimeError("SHAP did not return a reference baseline value.")
    base_value = float(base_values[0])
    predicted_probability = float(approval_probability(applicant_encoded)[0])
    reconstructed_probability = base_value + float(np.sum(shap_values))
    additivity_error = abs(reconstructed_probability - predicted_probability)
    if additivity_error > 0.02:
        raise RuntimeError(
            "The SHAP explanation did not reconcile with the model probability "
            f"(difference {additivity_error:.3f}). Please retry the explanation."
        )

    features = []
    for index, column in enumerate(FEATURE_COLUMNS):
        raw_value = row.iloc[0][column]
        if column in NUMERIC_FEATURES:
            display_value = f"{float(raw_value):,.0f}"
        else:
            display_value = str(raw_value)
        impact = float(shap_values[index])
        features.append(
            {
                "column": column,
                "feature": FEATURE_LABELS[column],
                "value": display_value,
                "impact": impact,
                "impact_percentage_points": impact * 100.0,
            }
        )

    return {
        "base_probability": base_value,
        "model_probability": predicted_probability,
        "reconstructed_probability": reconstructed_probability,
        "additivity_error": additivity_error,
        "reference_rows": int(sample_size),
        "features": features,
    }


def build_local_explanation_summary(details: dict) -> str:
    """Create a deterministic explanation if Gemini is unavailable."""
    features = details["features"]
    positive = sorted(
        (item for item in features if item["impact"] > 1e-8),
        key=lambda item: item["impact"],
        reverse=True,
    )[:3]
    negative = sorted(
        (item for item in features if item["impact"] < -1e-8),
        key=lambda item: item["impact"],
    )[:3]

    def describe(items) -> str:
        if not items:
            return "No material contribution in this direction was measured."
        return "; ".join(
            f"{item['feature']} ({item['value']}) "
            f"{item['impact_percentage_points']:+.2f} percentage points"
            for item in items
        )

    return (
        f"The model's average approval estimate for the {details['reference_rows']} "
        f"reference applicants was {details['base_probability']:.1%}. For this input, "
        f"the saved model returned an approval estimate of {details['model_probability']:.1%}.\n\n"
        f"The largest SHAP contributions pushing the estimate upward were: {describe(positive)}.\n\n"
        f"The largest SHAP contributions pushing the estimate downward were: {describe(negative)}.\n\n"
        "These are local explanations of how this saved model behaved relative to the "
        "reference dataset. They are not proof of cause, lending rules, or a real-world "
        "credit assessment. Correlated inputs can share attribution, and the explanation "
        "depends on the reference records used."
    )
