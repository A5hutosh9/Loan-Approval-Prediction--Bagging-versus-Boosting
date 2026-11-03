import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ui_theme import apply_theme, sidebar_brand, hero

st.set_page_config(page_title="Fairness Analysis | Bharat Loan AI", page_icon="⚖️", layout="wide")
apply_theme()
sidebar_brand()
hero(
    "Fairness Analysis",
    "Review descriptive model metrics across education and self-employment groups.",
)
st.caption("PAGE 05 · FAIRNESS REVIEW")

st.info(
    "**DATASET:** loan_approval_dataset.csv — 4,269 rows × 13 columns. "
    "**IMPORTANT:** The group metrics displayed below are predefined reported values; "
    "they are not recalculated dynamically from the CSV on each page load."
)
st.warning(
    "Fairness analysis is limited to the attributes and predefined metrics shown here. "
    "Differences between groups do not by themselves establish discrimination."
)

st.markdown("## SELECT MODEL")
model_name = st.selectbox(
    "MODEL",
    ["Decision Tree", "Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"],
)

education_data = {
    "Decision Tree": [["Graduate", 434, 0.6198, 0.9793, 0.9815, 0.0244, 0.0185], ["Not Graduate", 420, 0.6238, 0.9786, 0.9847, 0.0314, 0.0153]],
    "Bagging": [["Graduate", 434, 0.6267, 0.9862, 0.9926, 0.0244, 0.0074], ["Not Graduate", 420, 0.6286, 0.9881, 0.9962, 0.0252, 0.0038]],
    "Random Forest": [["Graduate", 434, 0.6198, 0.9793, 0.9815, 0.0244, 0.0185], ["Not Graduate", 420, 0.6310, 0.9810, 0.9923, 0.0377, 0.0077]],
    "AdaBoost": [["Graduate", 434, 0.6060, 0.9654, 0.9593, 0.0244, 0.0407], ["Not Graduate", 420, 0.6262, 0.9667, 0.9770, 0.0503, 0.0230]],
    "Gradient Boosting": [["Graduate", 434, 0.6244, 0.9839, 0.9889, 0.0244, 0.0111], ["Not Graduate", 420, 0.6262, 0.9810, 0.9885, 0.0314, 0.0115]],
}
employment_data = {
    "Decision Tree": [["No", 426, 0.6408, 0.9812, 0.9889, 0.0323, 0.0111], ["Yes", 428, 0.6028, 0.9766, 0.9769, 0.0238, 0.0231]],
    "Bagging": [["No", 426, 0.6408, 0.9859, 0.9926, 0.0258, 0.0074], ["Yes", 428, 0.6145, 0.9883, 0.9962, 0.0238, 0.0038]],
    "Random Forest": [["No", 426, 0.6362, 0.9765, 0.9815, 0.0323, 0.0185], ["Yes", 428, 0.6145, 0.9836, 0.9923, 0.0298, 0.0077]],
    "AdaBoost": [["No", 426, 0.6315, 0.9718, 0.9742, 0.0323, 0.0258], ["Yes", 428, 0.6005, 0.9603, 0.9615, 0.0417, 0.0385]],
    "Gradient Boosting": [["No", 426, 0.6408, 0.9812, 0.9889, 0.0323, 0.0111], ["Yes", 428, 0.6098, 0.9836, 0.9885, 0.0238, 0.0115]],
}

columns = ["Group", "Samples", "Approval Rate", "Accuracy", "TPR", "FPR", "FNR"]
education_df = pd.DataFrame(education_data[model_name], columns=["Education"] + columns[1:])
employment_df = pd.DataFrame(employment_data[model_name], columns=["Self-Employed"] + columns[1:])

def style_group_chart(data, category, title):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0b1d2e")
    ax.set_facecolor("#0b1d2e")
    ax.bar(data[category], data["Approval Rate"], color=["#3696dc", "#39c2bd"])
    ax.set_ylabel("Approval Rate", color="#eaf3ff")
    ax.set_title(title, color="#f2f7ff")
    ax.set_ylim(0, 1)
    ax.tick_params(colors="#d7e7f7")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#49617a")
    ax.grid(axis="y", alpha=.15)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("## EDUCATION GROUP")
st.dataframe(
    education_df.style.format({
        "Approval Rate": "{:.2%}", "Accuracy": "{:.2%}",
        "TPR": "{:.2%}", "FPR": "{:.2%}", "FNR": "{:.2%}",
    }),
    use_container_width=True,
)
style_group_chart(
    education_df, "Education", f"APPROVAL RATE BY EDUCATION · {model_name.upper()}"
)

st.markdown("## SELF-EMPLOYMENT GROUP")
st.dataframe(
    employment_df.style.format({
        "Approval Rate": "{:.2%}", "Accuracy": "{:.2%}",
        "TPR": "{:.2%}", "FPR": "{:.2%}", "FNR": "{:.2%}",
    }),
    use_container_width=True,
)
style_group_chart(
    employment_df, "Self-Employed", f"APPROVAL RATE BY EMPLOYMENT · {model_name.upper()}"
)

st.markdown("## METRIC GUIDE")
st.markdown(
    """
    - **Approval Rate:** proportion of applicants predicted as approved.
    - **TPR (True Positive Rate):** proportion of actually approved applicants correctly predicted as approved.
    - **FPR (False Positive Rate):** proportion of actually rejected applicants incorrectly predicted as approved.
    - **FNR (False Negative Rate):** proportion of actually approved applicants incorrectly predicted as rejected.
    - **Accuracy:** proportion of all predictions that are correct.
    """
)

with st.expander("HOW TO INTERPRET THESE GROUP COMPARISONS"):
    st.markdown(
        "Compare approval rates and error rates together. Differences may reflect sample "
        "composition, model behavior, data quality, or other factors; the displayed table "
        "cannot identify a cause. This explanation is rule-based, not a live Gemini response. "
        "A complete fairness assessment would require dynamically calculated and validated "
        "metrics, additional context, and appropriate domain and legal review."
    )

st.caption(
    "These comparisons are descriptive and are not a complete fairness assessment of real-world lending."
)
