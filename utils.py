"""Shared dataset and target-label utilities."""
from pathlib import Path

import pandas as pd
import streamlit as st


REPOSITORY_DATASET = Path(__file__).resolve().parent / "loan_approval_dataset.csv"


@st.cache_data(show_spinner=False)
def load_repository_dataset():
    """Load the bundled CSV once per app session; return None if unavailable."""
    try:
        df = pd.read_csv(REPOSITORY_DATASET)
        df.columns = df.columns.astype(str).str.strip()
        return df
    except (FileNotFoundError, pd.errors.ParserError, UnicodeDecodeError, OSError):
        return None


def show_dataset_expander(df, title="DATASET PREVIEW"):
    """Show a compact dataset preview and a basic schema-quality summary."""
    if df is None:
        return

    with st.expander(title):
        rows, columns = df.shape
        st.write(f"**Rows:** {rows:,}  ·  **Columns:** {columns}")
        st.dataframe(df.head(100), use_container_width=True, hide_index=True)
        if rows > 100:
            st.caption("Showing the first 100 rows for a quicker preview.")

        info = pd.DataFrame(
            {
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Missing Values": df.isna().sum().values,
                "Missing (%)": (df.isna().mean().values * 100).round(2),
            }
        )
        st.markdown("### DATASET QUALITY")
        st.dataframe(info, use_container_width=True, hide_index=True)


def normalize_binary_target(series):
    """
    Convert a binary target to 0/1 and return (encoded_series, mapping).

    Recognised positive labels are mapped to 1 and negative labels to 0.
    Numeric 0/1 labels retain their natural meaning. Unknown two-class labels
    are mapped deterministically in sorted order (first -> 0, second -> 1).
    Missing target values remain missing for the caller to remove.
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    non_missing = series.dropna()

    if pd.api.types.is_numeric_dtype(series):
        unique_original = list(pd.unique(non_missing))
        if len(unique_original) != 2:
            raise ValueError("Target column must contain exactly 2 non-missing classes.")
        if set(unique_original) == {0, 1}:
            mapping = {0: 0, 1: 1}
        else:
            ordered = sorted(unique_original)
            mapping = {ordered[0]: 0, ordered[1]: 1}
        return series.map(mapping), mapping

    values = series.astype("string").str.strip().str.lower()
    unique = sorted(values.dropna().unique().tolist())
    if len(unique) != 2:
        raise ValueError("Target column must contain exactly 2 non-missing classes.")

    positive_words = {
        "approved", "approve", "yes", "y", "true", "accepted", "accept",
        "1", "pass", "passed", "success", "successful",
    }
    negative_words = {
        "rejected", "reject", "no", "n", "false", "declined", "decline",
        "0", "fail", "failed",
    }

    positive = [value for value in unique if value in positive_words]
    negative = [value for value in unique if value in negative_words]

    if len(positive) == 1 and len(negative) == 1:
        mapping = {positive[0]: 1, negative[0]: 0}
    elif len(positive) == 1:
        other = next(value for value in unique if value != positive[0])
        mapping = {positive[0]: 1, other: 0}
    elif len(negative) == 1:
        other = next(value for value in unique if value != negative[0])
        mapping = {negative[0]: 0, other: 1}
    else:
        mapping = {unique[0]: 0, unique[1]: 1}

    return values.map(mapping).astype("Int64"), mapping
