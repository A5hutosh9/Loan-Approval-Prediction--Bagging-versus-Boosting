import logging
from pathlib import Path

import pandas as pd
import joblib
import streamlit as st

from ai_explainer import (
    generate_gemini_text,
    get_gemini_api_key,
    is_quota_error,
)
from ui_theme import apply_theme, sidebar_brand, hero
from model_explainer import (
    FEATURE_COLUMNS,
    build_local_explanation_summary,
    compute_local_shap_explanation,
)
from utils import load_repository_dataset

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Loan Prediction | Bharat Loan AI",
    page_icon="🔮",
    layout="wide",
)

apply_theme()
sidebar_brand()
hero(
    "Loan Approval Prediction",
    "Enter applicant details, generate a model prediction, and request an optional Gemini explanation.",
)

st.caption("PAGE 04 · APPLICANT PREDICTION")
st.info(
    "Academic demonstration only. This model output is not a real bank decision, "
    "credit assessment, or financial recommendation."
)

@st.cache_resource
def load_model():
    return joblib.load(Path(__file__).resolve().parents[1] / "loan_model.pkl")


try:
    model = load_model()
except Exception as error:
    st.error("The saved model could not be loaded. Please check that loan_model.pkl is present and compatible with the deployed Python and scikit-learn versions.")
    st.caption(f"Technical detail: {error}")
    st.stop()


st.markdown("## APPLICANT INFORMATION")
st.caption("Complete the fields below. The trained pipeline expects these applicant features.")

with st.container(border=True):
    st.markdown("### PERSONAL & FINANCIAL DETAILS")
    personal_left, personal_right = st.columns(2)
    with personal_left:
        no_of_dependents = st.number_input(
            "Number of Dependents", min_value=0, max_value=20, value=2, step=1
        )
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self-Employed", ["No", "Yes"])
    with personal_right:
        income_annum = st.number_input(
            "Annual Income (₹)", min_value=0, value=600000, step=10000
        )
        loan_amount = st.number_input(
            "Loan Amount (₹)", min_value=0, value=1500000, step=10000
        )
        loan_term = st.number_input(
            "Loan Term (Years)", min_value=1, max_value=50, value=15, step=1
        )

    st.markdown("---")
    st.markdown("### ASSETS & CREDIT PROFILE")
    asset_left, asset_right = st.columns(2)
    with asset_left:
        cibil_score = st.number_input(
            "CIBIL Score", min_value=0, max_value=900, value=760, step=1
        )
        residential_assets_value = st.number_input(
            "Residential Assets (₹)", min_value=0, value=2000000, step=10000
        )
        commercial_assets_value = st.number_input(
            "Commercial Assets (₹)", min_value=0, value=500000, step=10000
        )
    with asset_right:
        luxury_assets_value = st.number_input(
            "Luxury Assets (₹)", min_value=0, value=300000, step=10000
        )
        bank_asset_value = st.number_input(
            "Bank Assets (₹)", min_value=0, value=400000, step=10000
        )
        st.markdown(
            "<div style='padding:10px 12px;border:1px solid rgba(125,185,245,.20);"
            "background:rgba(255,255,255,.045);border-radius:10px;color:#c6d8eb;"
            "font-size:12px;margin-top:4px;'>All amounts are entered in Indian Rupees (₹).</div>",
            unsafe_allow_html=True,
        )

    predict = st.button(
        "🔮 PREDICT LOAN STATUS",
        type="primary",
        use_container_width=True,
    )


if predict:
    input_values = {
        "no_of_dependents": no_of_dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "residential_assets_value": residential_assets_value,
        "commercial_assets_value": commercial_assets_value,
        "luxury_assets_value": luxury_assets_value,
        "bank_asset_value": bank_asset_value,
    }
    input_data = pd.DataFrame([input_values])

    try:
        prediction_value = int(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]
        model_classes = list(getattr(model, "classes_", [0, 1]))
        approved_index = model_classes.index(1) if 1 in model_classes else 1
        rejected_index = model_classes.index(0) if 0 in model_classes else 0
        approval_probability = float(probabilities[approved_index])
        rejection_probability = float(probabilities[rejected_index])
    except Exception as error:
        st.error("The model could not process these applicant details.")
        st.caption(f"Technical detail: {error}")
        st.stop()

    predicted_label = "APPROVED" if prediction_value == 1 else "REJECTED"
    risk_band = (
        "LOW" if approval_probability >= 0.80
        else "MODERATE" if approval_probability >= 0.60
        else "HIGH"
    )

    st.session_state["loan_prediction_result"] = {
        "input_values": input_values,
        "prediction": prediction_value,
        "predicted_label": predicted_label,
        "approval_probability": approval_probability,
        "rejection_probability": rejection_probability,
        "risk_band": risk_band,
    }
    # A new input must never display an old AI explanation.
    st.session_state.pop("loan_ai_explanation", None)
    st.session_state.pop("loan_ai_model", None)
    st.session_state.pop("loan_ai_source", None)
    st.session_state.pop("loan_shap_details", None)
    st.session_state.pop("loan_ai_error", None)


result = st.session_state.get("loan_prediction_result")

if result:
    st.markdown("---")
    st.markdown("## PREDICTION RESULT")
    if result["prediction"] == 1:
        st.markdown(
            """
            <div class="approval-card">
                <div class="approval-title">✓ LOAN APPROVED</div>
                <div>The trained model predicts that this application is likely to be approved.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="rejection-card">
                <div class="rejection-title">✕ LOAN REJECTED</div>
                <div>The trained model predicts that this application is likely to be rejected.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.markdown(
        f'<div class="metric-card"><div class="metric-label">APPROVAL PROBABILITY</div>'
        f'<div class="metric-value">{result["approval_probability"]:.1%}</div>'
        f'<div class="metric-note">Model probability</div></div>',
        unsafe_allow_html=True,
    )
    metric_2.markdown(
        f'<div class="metric-card"><div class="metric-label">PROJECT RISK BAND</div>'
        f'<div class="metric-value">{result["risk_band"]}</div>'
        f'<div class="metric-note">Illustrative project threshold</div></div>',
        unsafe_allow_html=True,
    )
    metric_3.markdown(
        f'<div class="metric-card"><div class="metric-label">REJECTION PROBABILITY</div>'
        f'<div class="metric-value">{result["rejection_probability"]:.1%}</div>'
        f'<div class="metric-note">Model probability</div></div>',
        unsafe_allow_html=True,
    )

    ai_tab, details_tab = st.tabs(["🤖 AI EXPLANATION", "👤 APPLICANT DETAILS"])

    with ai_tab:
        st.markdown(
            '<div class="ai-card"><div class="ai-label">MODEL-GROUNDED EXPLANATION · SHAP + GEMINI</div>'
            '<div>SHAP first measures how each applicant feature shifts this model\'s approval estimate '
            'relative to reference records. Gemini then explains those measured contributions in plain language. '
            'This explains model behaviour, not real-world causes or lending rules.</div></div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "The SHAP calculation runs locally in this app. When Gemini is configured, "
            "the applicant inputs, model output, and SHAP contributions are sent to Google Gemini. "
            "Use synthetic demonstration data only."
        )

        api_key = get_gemini_api_key()
        if not api_key:
            st.info(
                "Gemini is not configured. You will still get a local SHAP explanation; "
                "add GEMINI_API_KEY in Streamlit Settings → Secrets to also get a Gemini-written summary."
            )

        if st.button(
            "✨ GENERATE MODEL EXPLANATION",
            key="generate_loan_ai_explanation",
            type="primary",
            use_container_width=True,
        ):
            try:
                reference_data = load_repository_dataset()
                if reference_data is None:
                    raise RuntimeError(
                        "The repository dataset could not be loaded, so a SHAP reference set is unavailable."
                    )

                input_frame = pd.DataFrame([result["input_values"]]).loc[:, FEATURE_COLUMNS]
                with st.spinner("Calculating feature contributions with SHAP..."):
                    shap_details = compute_local_shap_explanation(
                        model=model,
                        input_data=input_frame,
                        reference_data=reference_data,
                        background_size=40,
                        permutations=4,
                    )

                st.session_state["loan_shap_details"] = shap_details
                fallback_explanation = build_local_explanation_summary(shap_details)
                st.session_state["loan_ai_explanation"] = fallback_explanation
                st.session_state["loan_ai_source"] = "LOCAL SHAP"
                st.session_state.pop("loan_ai_error", None)

                if api_key:
                    attribution_lines = "\n".join(
                        f"- {item['feature']} = {item['value']}: "
                        f"{item['impact_percentage_points']:+.2f} percentage points"
                        for item in sorted(
                            shap_details["features"],
                            key=lambda item: abs(item["impact"]),
                            reverse=True,
                        )
                    )
                    prompt = f"""
ROLE
You are a careful explainable-AI tutor for a college machine-learning project.

PREDICTION FACTS — DO NOT CHANGE THEM
Predicted class: {result["predicted_label"]}
Approval probability from the saved model: {result["approval_probability"]:.1%}
Rejection probability from the saved model: {result["rejection_probability"]:.1%}
SHAP reference baseline approval probability: {shap_details["base_probability"]:.1%}
SHAP reconstructed approval probability: {shap_details["reconstructed_probability"]:.1%}
Number of reference rows used: {shap_details["reference_rows"]}

MEASURED LOCAL SHAP CONTRIBUTIONS
A positive contribution moves this model's approval probability upward relative to its
reference baseline. A negative contribution moves it downward. The following figures
are measured SHAP values in percentage points, not causal effects:
{attribution_lines}

TASK
Explain this one prediction using these sections:
1. Prediction: state the predicted class and the two supplied probabilities.
2. Main factors pushing the estimate upward: explain the strongest positive SHAP
   contributions, using the actual feature values and signed percentage-point values.
3. Main factors pushing the estimate downward: explain the strongest negative SHAP
   contributions in the same way.
4. How to interpret this: explain that the SHAP values add from the reference baseline
   to the current model estimate, and describe them as local model attributions.

STRICT RULES
- Use only the supplied prediction and SHAP evidence. Do not invent model rules,
  feature thresholds, CIBIL cut-offs, causes, banking standards, or external facts.
- Do not say a feature caused the outcome. Say it pushed the model estimate up or down
  relative to the reference baseline.
- Do not describe the applicant as creditworthy, uncreditworthy, safe, or risky.
- Do not call the displayed project risk band an official risk grade.
- Explain the strongest two or three positive and negative contributions; do not
  simply list every input field.
- State that correlated inputs may share attribution and that results depend on the
  reference data.
- Use simple professional English for a college project evaluator.
- Keep the explanation under 200 words and return only the explanation.
"""
                    try:
                        with st.spinner("Gemini is writing the SHAP-based explanation..."):
                            explanation, model_used = generate_gemini_text(
                                prompt, api_key=api_key, max_output_tokens=600
                            )
                        st.session_state["loan_ai_explanation"] = explanation
                        st.session_state["loan_ai_model"] = model_used
                        st.session_state["loan_ai_source"] = f"GEMINI + SHAP · {model_used}"
                    except Exception as error:
                        st.session_state["loan_ai_error"] = str(error).replace(api_key, "[redacted]")
                        logger.exception("Gemini SHAP explanation failed")
            except Exception as error:
                st.session_state.pop("loan_shap_details", None)
                st.session_state.pop("loan_ai_explanation", None)
                st.session_state["loan_ai_error"] = str(error)
                logger.exception("Local SHAP explanation failed")

        shap_details = st.session_state.get("loan_shap_details")
        explanation = st.session_state.get("loan_ai_explanation")

        if st.session_state.get("loan_ai_error"):
            with st.expander("Explanation diagnostic", expanded=True):
                st.warning(
                    "One explanation step failed. The diagnostic below is included to make "
                    "the actual problem visible instead of silently returning a generic message."
                )
                st.code(st.session_state["loan_ai_error"])

        if explanation:
            with st.container(border=True):
                st.markdown("**EXPLANATION OF THIS PREDICTION**")
                st.markdown(explanation)
                st.caption(f"Explanation source: {st.session_state.get('loan_ai_source', 'SHAP')}")

        if shap_details:
            st.markdown("### LOCAL FEATURE CONTRIBUTIONS")
            baseline_col, prediction_col, difference_col = st.columns(3)
            baseline_col.metric(
                "REFERENCE BASELINE",
                f"{shap_details['base_probability']:.1%}",
            )
            prediction_col.metric(
                "MODEL ESTIMATE",
                f"{shap_details['model_probability']:.1%}",
            )
            difference_col.metric(
                "SHAP RECONCILIATION",
                f"{shap_details['additivity_error']:.2%}",
            )
            st.caption(
                "Positive SHAP values push this model's approval estimate upward; negative "
                "values push it downward. Values are percentage-point contributions relative "
                "to the reference baseline, not causes."
            )
            contribution_table = pd.DataFrame(shap_details["features"])
            contribution_table["impact_percentage_points"] = contribution_table[
                "impact_percentage_points"
            ].map(lambda value: f"{value:+.2f} pp")
            contribution_table = contribution_table.rename(
                columns={
                    "feature": "Feature",
                    "value": "Applicant value",
                    "impact_percentage_points": "Impact on approval estimate",
                }
            )[["Feature", "Applicant value", "Impact on approval estimate"]]
            st.dataframe(
                contribution_table.assign(
                    _sort=[
                        abs(item["impact"])
                        for item in shap_details["features"]
                    ]
                ).sort_values("_sort", ascending=False).drop(columns="_sort"),
                use_container_width=True,
                hide_index=True,
            )
            st.caption(
                f"Reference sample: {shap_details['reference_rows']} records from the bundled "
                "dataset. Correlated features can share attribution; SHAP values describe "
                "the saved model's behaviour, not causation or lending policy."
            )
        else:
            st.info(
                "Select **Generate Model Explanation** to calculate a local SHAP explanation "
                "and, when configured, ask Gemini to explain the measured contributions."
            )

    with details_tab:
        st.markdown("### APPLICANT DETAILS")
        st.dataframe(
            pd.DataFrame([result["input_values"]]).rename(
                columns={
                    "no_of_dependents": "Dependents",
                    "education": "Education",
                    "self_employed": "Self-Employed",
                    "income_annum": "Annual Income (₹)",
                    "loan_amount": "Loan Amount (₹)",
                    "loan_term": "Loan Term (Years)",
                    "cibil_score": "CIBIL Score",
                    "residential_assets_value": "Residential Assets (₹)",
                    "commercial_assets_value": "Commercial Assets (₹)",
                    "luxury_assets_value": "Luxury Assets (₹)",
                    "bank_asset_value": "Bank Assets (₹)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "The approval/rejection probabilities are model outputs. The displayed risk "
        "band uses an illustrative project threshold and is not a banking risk grade."
    )
else:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">READY FOR A TEST PREDICTION</div>
            <div class="section-subtitle">Enter the applicant information above and select Predict Loan Status. Your result will appear here.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("## HOW THE APPLICATION WORKS")
st.markdown(
    """
    <div class="workflow">
      <div class="workflow-step"><div class="workflow-num">1</div><div class="workflow-title">INPUT</div><div class="workflow-text">Applicant features are entered into the interface.</div></div>
      <div class="workflow-step"><div class="workflow-num">2</div><div class="workflow-title">PREPROCESSING</div><div class="workflow-text">The trained pipeline prepares numerical and categorical data.</div></div>
      <div class="workflow-step"><div class="workflow-num">3</div><div class="workflow-title">MODEL PREDICTION</div><div class="workflow-text">The saved ensemble model returns a class and probabilities.</div></div>
      <div class="workflow-step"><div class="workflow-num">4</div><div class="workflow-title">SHAP + GEMINI</div><div class="workflow-text">SHAP measures local feature contributions; Gemini explains the measured evidence.</div></div>
    </div>
    <div class="footer-card">🇮🇳 <b>BHARAT LOAN AI</b> · ACADEMIC PROJECT · NOT A REAL FINANCIAL INSTITUTION</div>
    """,
    unsafe_allow_html=True,
)
