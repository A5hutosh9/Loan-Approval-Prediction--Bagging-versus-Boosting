"""Gemini explanation helper used by the experiment page."""
import html
import os
import streamlit as st

# These are stable text-generation models in Google's current Gemini API catalogue.
GEMINI_MODELS = (
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
)


def get_gemini_api_key():
    """Read the API key from Streamlit Secrets, then environment variables."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return (key or os.environ.get("GEMINI_API_KEY", "")).strip()


def is_quota_error(error):
    message = str(error).lower()
    return any(token in message for token in (
        "quota", "resource_exhausted", "daily limit", "billing",
        "429", "too_many_requests", "rate_limit", "rate limit",
    ))


def is_retryable_model_error(error):
    message = str(error).lower()
    return any(token in message for token in (
        "503", "service unavailable", "unavailable", "overloaded",
        "500", "internal server error", "404", "not found",
        "model_not_found", "unsupported model",
    ))


def generate_gemini_text(prompt, api_key=None, max_output_tokens=700):
    """Generate text with a stable Flash model and a small model fallback chain."""
    from google import genai
    from google.genai import types

    key = (api_key or get_gemini_api_key()).strip()
    if not key:
        raise RuntimeError(
            "Gemini API key is missing. Add GEMINI_API_KEY in Streamlit App → Settings → Secrets."
        )

    client = genai.Client(api_key=key)
    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.25,
                    max_output_tokens=max_output_tokens,
                ),
            )
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip(), model_name
            last_error = RuntimeError(f"{model_name} returned an empty response.")
        except Exception as error:
            last_error = error
            # A quota or credential problem affects the project/key, so stop
            # instead of wasting calls against more models.
            if is_quota_error(error) or not is_retryable_model_error(error):
                raise
            continue

    raise RuntimeError(
        "Gemini's available Flash models could not complete the request. "
        "Please retry later. Details: " + str(last_error)
    )


def render_live_experiment_explanation(results_df, dataset_rows, dataset_columns, target_column):
    """Render an on-demand, session-cached explanation of experiment metrics."""
    st.subheader("AI Explanation")
    st.caption("An optional Gemini-generated interpretation of the current experiment.")

    api_key = get_gemini_api_key()
    if not api_key:
        st.info("AI explanations are optional. Add GEMINI_API_KEY in Streamlit Secrets to enable this feature.")
        return

    explanation_key = "experiment_ai_explanation"
    model_key = "experiment_ai_model"

    if st.button("✨ Generate AI Explanation", key="generate_experiment_ai", type="primary"):
        metrics_csv = results_df.to_csv(index=False)
        prompt = f"""
You are a careful machine-learning tutor explaining a college project experiment.
Dataset: {dataset_rows} rows × {dataset_columns} columns.
Target: {target_column}.
Use only these supplied results:
{metrics_csv}

Explain accuracy, F1-score, ROC-AUC, the train-validation gap, and the main
limitations in plain English. Do not invent values, causes, or feature importance.
Do not claim one model is universally best. State that results depend on this
dataset and validation design and are not real-world lending guarantees.
Keep the explanation structured and under 220 words.
"""
        try:
            with st.spinner("Gemini is preparing the explanation..."):
                explanation, model_used = generate_gemini_text(
                    prompt, api_key=api_key, max_output_tokens=700
                )
            st.session_state[explanation_key] = explanation
            st.session_state[model_key] = model_used
        except Exception as error:
            if is_quota_error(error):
                st.error("Gemini free-tier quota is currently exhausted. Model evaluation is complete; try the AI explanation again after the quota resets.")
            else:
                st.error("Gemini could not generate an explanation right now. Check the API key, model access, and connection, then try again.")
                st.caption(f"Technical detail: {error}")

    explanation = st.session_state.get(explanation_key)
    if explanation:
        safe_explanation = html.escape(explanation).replace("\n", "<br>")
        st.markdown(
            f'<div class="ai-card"><div class="ai-label">GEMINI AI · EXPERIMENT REVIEW</div>'
            f'<div style="line-height:1.75;">{safe_explanation}</div></div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Generated with {st.session_state.get(model_key, 'Gemini Flash')}.")
