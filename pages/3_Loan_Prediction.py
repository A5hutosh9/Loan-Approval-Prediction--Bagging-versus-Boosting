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
            '<div class="ai-card"><div class="ai-label">GEMINI AI · EXPLANATION LAYER</div>'
            '<div>Ask Gemini to explain the prediction in plain language. The saved ML model '
            'has already produced the result; Gemini does not make or change the decision.</div></div>',
            unsafe_allow_html=True,
        )

        st.caption("PRIVACY: When you request an AI explanation, the applicant fields and model output shown above are sent to Google Gemini. Use synthetic demonstration data only; do not enter real people’s financial or identity details.")
        api_key = get_gemini_api_key()
        if not api_key:
            st.warning(
                "Gemini is not configured. Add GEMINI_API_KEY under your Streamlit app's "
                "Settings → Secrets. The prediction above remains available."
            )
        else:
            if st.button(
                "✨ GENERATE AI EXPLANATION",
                key="generate_loan_ai_explanation",
                type="primary",
                use_container_width=True,
            ):
                values = result["input_values"]
                prompt = f"""
You are an educational assistant explaining a machine-learning project called
Loan Approval Prediction: Bagging vs Boosting.

The trained model has already made the prediction. Do not change, second-guess,
or present a new lending decision.

Prediction: {result["predicted_label"]}
Model approval probability: {result["approval_probability"]:.1%}
Model rejection probability: {result["rejection_probability"]:.1%}
Illustrative project risk band: {result["risk_band"]}

Applicant data:
{values}

Write a clear explanation of about 110-140 words for a college project reviewer.
Explain the meaning of the model probability, describe that the listed applicant
features were supplied to the trained preprocessing and ensemble pipeline, and
summarise the workflow from input to model output. Do not claim that one specific
feature caused the decision or invent feature importance, banking rules, or
credit regulations. The application does not calculate feature-level attribution.
State clearly that this is an academic demonstration and not a real bank decision.
"""
                try:
                    with st.spinner("Gemini is preparing your explanation..."):
                        explanation, model_used = generate_gemini_text(
                            prompt, api_key=api_key, max_output_tokens=450
                        )
                    st.session_state["loan_ai_explanation"] = explanation
                    st.session_state["loan_ai_model"] = model_used
                except Exception as error:
                    if is_quota_error(error):
                        st.error(
                            "Gemini's request limit or free-tier quota has been reached. Your "
                            "prediction is still complete. Wait before trying again, or "
                            "check your Gemini API usage."
                        )
                    else:
                        st.error(
                            "Gemini could not generate the explanation. Check the API "
                            "key and model access, then try again."
                        )
                        logger.exception("Gemini loan explanation failed")

        explanation = st.session_state.get("loan_ai_explanation")
        if explanation:
            with st.container(border=True):
                st.markdown("**GEMINI AI · GENERATED EXPLANATION**")
                st.markdown(explanation)
                st.caption(f"Generated with {st.session_state.get('loan_ai_model', 'Gemini Flash')}.")

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
      <div class="workflow-step"><div class="workflow-num">4</div><div class="workflow-title">GEMINI EXPLANATION</div><div class="workflow-text">Gemini optionally explains the model output in plain language.</div></div>
    </div>
    <div class="footer-card">🇮🇳 <b>BHARAT LOAN AI</b> · ACADEMIC PROJECT · NOT A REAL FINANCIAL INSTITUTION</div>
    """,
    unsafe_allow_html=True,
)
