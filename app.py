import streamlit as st
from utils import load_repository_dataset, show_dataset_expander
from ui_theme import apply_theme, sidebar_brand, hero

st.set_page_config(page_title="Bharat Loan AI | Project Dashboard", page_icon="🏦", layout="wide")
apply_theme()
sidebar_brand()

st.sidebar.markdown("**PROJECT NAVIGATION**")
st.sidebar.caption("Academic machine-learning demonstration")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='color:#c9dcef;font-size:11px;font-weight:800;letter-spacing:.8px;'>DEVELOPED BY GROUP 10</div>",
    unsafe_allow_html=True,
)

hero("Bharat Loan AI", "Loan approval prediction with Bagging, Boosting, and an optional Gemini explanation.")
st.caption("PAGE 01 · PROJECT OVERVIEW")

df = load_repository_dataset()
rows_label = f"{df.shape[0]:,}" if df is not None else "Unavailable"

st.markdown("## PROJECT AT A GLANCE")
st.write(
    "Explore the dataset, compare ensemble strategies, run a custom experiment, "
    "or test an applicant using the saved model."
)
cols = st.columns(4)
cols[0].metric("Dataset Records", rows_label)
cols[1].metric("Models Studied", "5")
cols[2].metric("Ensemble Approaches", "2")
cols[3].metric("AI Explanation", "Optional Gemini")

if df is None:\n    st.warning("The bundled dataset CSV could not be loaded. The saved prediction model may still be available.")\n\nst.markdown("## DATASET CARD")
st.markdown(
    """
    <div class="section-card">
      <div class="section-title">LOAN APPROVAL DATASET</div>
      <div class="section-subtitle">The reference dataset supports the saved prediction model and the reported model-comparison results.</div>
      <ul>
        <li><b>File:</b> <code>loan_approval_dataset.csv</code></li>
        <li><b>Size:</b> 4,269 rows × 13 columns (including identifier and target columns in the source dataset).</li>
        <li><b>Target:</b> <code>loan_status</code> — Approved or Rejected.</li>
        <li><b>Predictors:</b> CIBIL score, annual income, loan amount and term, dependents, education, self-employment, and asset values.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## EXPLORE THE APPLICATION")
items = st.columns(3)
with items[0]:
    st.markdown("### BAGGING VS BOOSTING")
    st.write("Understand parallel and sequential ensemble learning and review reported validation metrics.")
with items[1]:
    st.markdown("### RUN EXPERIMENT")
    st.write("Upload a compatible binary-classification CSV and evaluate five models with cross-validation.")
with items[2]:
    st.markdown("### LOAN PREDICTION")
    st.write("Enter applicant features and view the saved model's prediction and probability estimates.")

if df is not None:
    show_dataset_expander(df, "PREVIEW THE REPOSITORY DATASET")

st.markdown("## PREDICTION WORKFLOW")
st.markdown(
    """
    <div class="workflow">
      <div class="workflow-step"><div class="workflow-num">1</div><div class="workflow-title">APPLICANT INPUT</div><div class="workflow-text">Provide the financial and applicant features.</div></div>
      <div class="workflow-step"><div class="workflow-num">2</div><div class="workflow-title">PREPROCESSING</div><div class="workflow-text">The saved pipeline prepares the input features.</div></div>
      <div class="workflow-step"><div class="workflow-num">3</div><div class="workflow-title">MODEL INFERENCE</div><div class="workflow-text">The ensemble produces a class prediction and probabilities.</div></div>
      <div class="workflow-step"><div class="workflow-num">4</div><div class="workflow-title">AI EXPLANATION</div><div class="workflow-text">Gemini can optionally explain the model output.</div></div>
    </div>
    <div class="footer-card">🇮🇳 <b>BHARAT LOAN AI</b> · GROUP 10 · ACADEMIC MACHINE-LEARNING PROJECT · NOT A REAL FINANCIAL INSTITUTION</div>
    """,
    unsafe_allow_html=True,
)
