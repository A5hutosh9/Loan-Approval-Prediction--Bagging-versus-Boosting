# Security and Privacy Notes

This repository is an academic demonstration. Do not use it to make real lending or credit decisions.

## API keys

- Store Gemini credentials in Streamlit Community Cloud Secrets or a local `.streamlit/secrets.toml` file.
- Never put a real API key in Python source code, notebooks, screenshots, issue reports, or commits.
- If a key is exposed, revoke it in Google AI Studio and create a replacement.
- The tracked `.streamlit/secrets.toml.example` file is a placeholder only. Copy it to `.streamlit/secrets.toml` and replace the placeholder locally.

## Applicant data

- Use synthetic or otherwise non-sensitive demonstration records.
- When a user requests a Gemini explanation on the Loan Prediction page, the entered applicant feature values and the model output are sent to Google's Gemini API to produce the explanation.
- Do not enter real names, account numbers, contact details, identity numbers, or real financial records.
- The app does not need Gemini to produce the model prediction. Gemini is an optional explanation layer.

## Serialized model

Only load `loan_model.pkl` from this trusted repository. Joblib/pickle files can execute code during deserialization and must not be loaded from untrusted sources.
