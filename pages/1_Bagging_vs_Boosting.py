import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_repository_dataset, show_dataset_expander
from ui_theme import apply_theme, sidebar_brand, hero

st.set_page_config(page_title="Ensemble Methods | Bharat Loan AI", page_icon="⚖️", layout="wide")
apply_theme()
sidebar_brand()
hero("Ensemble Methods", "A side-by-side study of Bagging and Boosting in loan approval classification.")
st.caption("PAGE 02 · MODEL COMPARISON")
st.info(
    "**Dataset:** loan_approval_dataset.csv — 4,269 loan applications and 13 columns. "
    "The target is loan_status (Approved/Rejected). Features describe credit, income, "
    "loan, education, employment, and assets. **Models:** Decision Tree, Bagging, "
    "Random Forest, AdaBoost, and Gradient Boosting. The values below are reported "
    "project validation metrics."
)

st.markdown("## BAGGING · PARALLEL LEARNING")
st.write(
    "Bagging (Bootstrap Aggregating) trains multiple estimators independently on "
    "bootstrap samples, then combines their predictions. It is commonly used to reduce variance."
)
col1, col2, col3 = st.columns(3)
col1.metric("Training Strategy", "Parallel")
col2.metric("Core Purpose", "Reduce Variance")
col3.metric("Project Example", "Bagging")

st.markdown("## BOOSTING · SEQUENTIAL LEARNING")
st.write(
    "Boosting builds estimators in sequence. Later estimators focus on patterns or "
    "errors left by earlier ones, combining them into a stronger model."
)
col1, col2, col3 = st.columns(3)
col1.metric("Training Strategy", "Sequential")
col2.metric("Core Purpose", "Improve Errors")
col3.metric("Project Examples", "AdaBoost / Gradient Boosting")

st.markdown("## CONCEPTUAL COMPARISON")
comparison = pd.DataFrame({
    "Feature": ["Training", "Main Goal", "Estimator Relationship", "Examples"],
    "Bagging": ["Parallel", "Reduce Variance", "Independent", "Bagging, Random Forest"],
    "Boosting": ["Sequential", "Improve Errors", "Dependent", "AdaBoost, Gradient Boosting"],
})
st.dataframe(comparison, use_container_width=True, hide_index=True)

df = load_repository_dataset()
if df is not None:
    show_dataset_expander(df, "INSPECT THE PROJECT DATASET")

st.markdown("## REPORTED VALIDATION METRICS")
st.caption("These metrics describe the reported evaluation setup, not lending guarantees.")
results = pd.DataFrame({
    "Model": ["Decision Tree", "Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"],
    "Validation Accuracy": [0.9782, 0.9843, 0.9796, 0.9590, 0.9803],
    "Validation F1": [0.9825, 0.9875, 0.9837, 0.9669, 0.9843],
    "Validation ROC-AUC": [0.9771, 0.9975, 0.9967, 0.9948, 0.9981],
})
st.dataframe(
    results.style.format({
        "Validation Accuracy": "{:.4f}",
        "Validation F1": "{:.4f}",
        "Validation ROC-AUC": "{:.4f}",
    }),
    use_container_width=True,
)

for metric, title, ylabel in [
    ("Validation Accuracy", "VALIDATION ACCURACY BY MODEL", "Accuracy"),
    ("Validation F1", "VALIDATION F1-SCORE BY MODEL", "F1-score"),
    ("Validation ROC-AUC", "VALIDATION ROC-AUC BY MODEL", "ROC-AUC"),
]:
    st.markdown(f"### {title}")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("#0b1d2e")
    ax.set_facecolor("#0b1d2e")
    ax.bar(results["Model"], results[metric])
    ax.set_ylim(0.90, 1.00)
    ax.set_ylabel(ylabel, color="#eaf3ff")
    ax.tick_params(axis="x", rotation=18, colors="#d7e7f7")
    ax.tick_params(axis="y", colors="#d7e7f7")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#49617a")
    ax.grid(axis="y", alpha=.15)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("## GENERALIZATION GAP")
st.caption("Gap values are training score minus validation score.")
gap_data = pd.DataFrame({
    "Model": ["Decision Tree", "Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"],
    "Accuracy Gap": [0.0218, 0.0157, 0.0204, 0.0066, 0.0156],
    "F1 Gap": [0.0175, 0.0125, 0.0163, 0.0054, 0.0125],
    "ROC-AUC Gap": [0.0229, 0.0025, 0.0033, 0.0016, 0.0018],
})
st.dataframe(
    gap_data.style.format({
        "Accuracy Gap": "{:.4f}",
        "F1 Gap": "{:.4f}",
        "ROC-AUC Gap": "{:.4f}",
    }),
    use_container_width=True,
)

with st.expander("HOW TO INTERPRET THESE RESULTS"):
    st.markdown(
        """
        - **Accuracy** is the share of predictions classified correctly.
        - **F1-score** balances precision and recall.
        - **ROC-AUC** measures how well the model separates the two classes across thresholds.
        - **Generalization gap** is training score minus validation score; a larger positive gap can indicate overfitting.

        Bagging combines independently trained estimators, while boosting builds estimators
        sequentially. These reported results apply only to this dataset and evaluation
        design; they do not guarantee outcomes for new applicants or real lending decisions.
        """
    )

st.caption("This academic project does not represent a real financial institution.")
