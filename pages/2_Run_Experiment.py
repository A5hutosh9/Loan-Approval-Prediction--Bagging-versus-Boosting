import hashlib
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_curve
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from ai_explainer import render_live_experiment_explanation
from ui_theme import apply_theme, sidebar_brand, hero
from utils import normalize_binary_target


st.set_page_config(page_title="Run Experiment | Bharat Loan AI", page_icon="🧪", layout="wide")
apply_theme()
sidebar_brand()
hero(
    "Run Experiment",
    "Upload a binary-classification dataset and compare five models using stratified cross-validation.",
)
st.caption("PAGE 03 · CUSTOM MODEL EXPERIMENT")

uploaded_file = st.file_uploader("UPLOAD CSV DATASET", type=["csv"], key="experiment_csv")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    st.session_state["experiment_file_bytes"] = file_bytes
    st.session_state["experiment_file_name"] = file_name
    st.session_state["experiment_file_hash"] = file_hash
else:
    file_bytes = st.session_state.get("experiment_file_bytes")
    file_name = st.session_state.get("experiment_file_name")
    file_hash = st.session_state.get("experiment_file_hash")

if not file_bytes:
    st.info("Upload a CSV file to start a new experiment.")
    st.markdown(
        "**Supported targets:** Approved/Rejected, Yes/No, 1/0, or True/False. "
        "Choose a binary target column after uploading."
    )
    st.stop()

try:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = df.columns.astype(str).str.strip()
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

with st.expander("PREVIEW UPLOADED DATASET", expanded=False):
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.dataframe(df, use_container_width=True)

target_column = st.selectbox("CHOOSE THE TARGET COLUMN", df.columns)

signature = (file_hash, target_column)
if st.session_state.get("experiment_signature") != signature:
    st.session_state["experiment_signature"] = signature
    st.session_state.pop("experiment_results", None)
    st.session_state.pop("experiment_roc", None)
    st.session_state.pop("experiment_dataset_info", None)
    st.session_state.pop("experiment_ai_explanation", None)
    st.session_state.pop("experiment_ai_model", None)

try:
    y_raw, target_mapping = normalize_binary_target(df[target_column])
except Exception as exc:
    st.error(str(exc))
    st.stop()

mapping_summary = ", ".join(
    f"{label!s} → {encoded}" for label, encoded in target_mapping.items()
)
st.caption(
    f"Target encoding: {mapping_summary}. Class 1 is treated as the positive class "
    "for F1-score and ROC-AUC."
)

valid = y_raw.notna()
df = df.loc[valid].copy()
y = y_raw.loc[valid].astype(int)
X = df.drop(columns=[target_column])

id_columns = [
    c for c in X.columns
    if c.lower().replace("_", "").replace(" ", "")
    in {"id", "loanid", "applicationid", "customerid", "applicantid"}
]
if id_columns:
    X = X.drop(columns=id_columns)
    st.info(f"Automatically removed ID column(s): {', '.join(id_columns)}")

empty_columns = [c for c in X.columns if X[c].isna().all()]
if empty_columns:
    X = X.drop(columns=empty_columns)
    st.warning(f"Removed completely empty columns: {', '.join(empty_columns)}")

numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

st.markdown("## DETECTED FEATURES")
left, right = st.columns(2)
left.write("**NUMERICAL**")
left.write(numeric_features or "None")
right.write("**CATEGORICAL**")
right.write(categorical_features or "None")

counts = y.value_counts().sort_index()
st.markdown("## TARGET DISTRIBUTION")
a, b = st.columns(2)
a.metric("CLASS 0", int(counts.get(0, 0)))
b.metric("CLASS 1", int(counts.get(1, 0)))

if not numeric_features and not categorical_features:
    st.error("No usable feature columns remain after removing the target and ID/empty columns.")
    st.stop()

transformers = []
if numeric_features:
    transformers.append((
        "numeric",
        Pipeline([("imputer", SimpleImputer(strategy="median"))]),
        numeric_features,
    ))
if categorical_features:
    transformers.append((
        "categorical",
        Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]),
        categorical_features,
    ))
preprocessor = ColumnTransformer(transformers=transformers)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Bagging": BaggingClassifier(
        estimator=DecisionTreeClassifier(random_state=42),
        n_estimators=100, bootstrap=True, random_state=42, n_jobs=1,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, max_features="sqrt", random_state=42, n_jobs=1,
    ),
    "AdaBoost": AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1, random_state=42),
        n_estimators=100, learning_rate=0.5, random_state=42,
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42,
    ),
}

results_df = st.session_state.get("experiment_results")

if results_df is None:
    if st.button("🚀 RUN EXPERIMENT", type="primary", use_container_width=True):
        if len(X) < 20:
            st.error("Dataset is too small for a meaningful experiment (minimum 20 rows).")
            st.stop()

        class_counts = y.value_counts()
        if len(class_counts) != 2 or int(class_counts.min()) < 2:
            st.error("The target must contain exactly two classes, with at least two samples in each class.")
            st.stop()

        cv = StratifiedKFold(
            n_splits=min(5, int(class_counts.min())),
            shuffle=True,
            random_state=42,
        )
        results = []
        roc_data = {}
        progress = st.progress(0)

        for idx, (name, model) in enumerate(models.items()):
            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("model", model),
            ])
            scores = cross_validate(
                pipeline, X, y, cv=cv,
                scoring=["accuracy", "f1", "roc_auc"],
                return_train_score=True, n_jobs=1,
            )
            train_acc = scores["train_accuracy"].mean()
            val_acc = scores["test_accuracy"].mean()
            train_f1 = scores["train_f1"].mean()
            val_f1 = scores["test_f1"].mean()
            train_auc = scores["train_roc_auc"].mean()
            val_auc = scores["test_roc_auc"].mean()

            results.append({
                "Model": name,
                "Train Accuracy": train_acc,
                "Validation Accuracy": val_acc,
                "Train F1": train_f1,
                "Validation F1": val_f1,
                "Train ROC-AUC": train_auc,
                "Validation ROC-AUC": val_auc,
                "Accuracy Gap": train_acc - val_acc,
                "F1 Gap": train_f1 - val_f1,
                "ROC-AUC Gap": train_auc - val_auc,
            })

            probabilities = cross_val_predict(
                pipeline, X, y, cv=cv, method="predict_proba", n_jobs=1
            )[:, 1]
            fpr, tpr, _ = roc_curve(y, probabilities)
            roc_data[name] = (fpr, tpr, val_auc)
            progress.progress((idx + 1) / len(models))

        st.session_state["experiment_results"] = pd.DataFrame(results)
        st.session_state["experiment_roc"] = roc_data
        st.session_state["experiment_dataset_info"] = (len(df), df.shape[1], target_column)
        st.rerun()

    st.info("Select Run Experiment to calculate the model results.")
    st.stop()

rows, columns, target_name = st.session_state["experiment_dataset_info"]
st.success("Experiment completed. Results are saved for this session.")
render_live_experiment_explanation(results_df, rows, columns, target_name)

st.markdown("## MODEL RESULTS")
st.dataframe(
    results_df.style.format({
        column: "{:.4f}" for column in results_df.columns if column != "Model"
    }),
    use_container_width=True,
)

x = np.arange(len(results_df))
width = 0.35
for metric, heading in [
    ("Accuracy", "ACCURACY COMPARISON"),
    ("F1", "F1-SCORE COMPARISON"),
    ("ROC-AUC", "ROC-AUC COMPARISON"),
]:
    st.markdown(f"### {heading}")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0b1d2e")
    ax.set_facecolor("#0b1d2e")
    ax.bar(x - width / 2, results_df[f"Train {metric}"], width, label="Training")
    ax.bar(x + width / 2, results_df[f"Validation {metric}"], width, label="Validation")
    ax.set_xticks(x)
    ax.set_xticklabels(results_df["Model"], rotation=20, color="#d7e7f7")
    ax.set_ylabel(metric, color="#eaf3ff")
    ax.tick_params(axis="y", colors="#d7e7f7")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#49617a")
    ax.grid(axis="y", alpha=.15)
    ax.legend(facecolor="#102a43", edgecolor="#49617a", labelcolor="#eef6ff")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("## GENERALIZATION GAP")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0b1d2e")
ax.set_facecolor("#0b1d2e")
ax.bar(results_df["Model"], results_df["Accuracy Gap"])
ax.set_ylabel("Training − Validation Accuracy", color="#eaf3ff")
ax.tick_params(axis="x", rotation=20, colors="#d7e7f7")
ax.tick_params(axis="y", colors="#d7e7f7")
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color("#49617a")
ax.grid(axis="y", alpha=.15)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("## ROC CURVES")
fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor("#0b1d2e")
ax.set_facecolor("#0b1d2e")
for name, (fpr, tpr, auc_value) in st.session_state["experiment_roc"].items():
    ax.plot(fpr, tpr, label=f"{name} (AUC={auc_value:.3f})")
ax.plot([0, 1], [0, 1], linestyle="--", color="#91a8be")
ax.set_xlabel("False Positive Rate", color="#eaf3ff")
ax.set_ylabel("True Positive Rate", color="#eaf3ff")
ax.set_title("Cross-Validated ROC Curves", color="#f2f7ff")
ax.tick_params(colors="#d7e7f7")
ax.legend(facecolor="#102a43", edgecolor="#49617a", labelcolor="#eef6ff")
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("## DOWNLOAD RESULTS")
st.download_button(
    "⬇️ DOWNLOAD EXPERIMENT RESULTS",
    data=results_df.to_csv(index=False).encode("utf-8"),
    file_name="loan_experiment_results.csv",
    mime="text/csv",
)
