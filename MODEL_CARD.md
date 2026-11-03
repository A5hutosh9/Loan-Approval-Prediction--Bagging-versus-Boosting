# Model Card — Loan Approval Prediction

## Summary

This repository contains an academic binary-classification prototype for exploring loan-status prediction with ensemble learning. A serialized model/pipeline is stored in `loan_model.pkl` and loaded by the Streamlit prediction page.

This model card describes the implementation and limitations visible in the repository. It is not a certification of model quality, safety, fairness, or fitness for financial use.

## Intended use

- Classroom demonstration of a supervised classification workflow.
- Exploring the effect of Bagging and Boosting on a supplied loan-status dataset.
- Demonstrating prediction interfaces, model metrics, and AI-generated natural-language explanations.

## Out-of-scope use

Do not use this prototype to make or support real lending decisions, credit eligibility determinations, loan pricing, customer ranking, or other decisions that affect individuals. It has not been validated for regulated financial use or for deployment on a real applicant population.

## Data

- Repository file: `loan_approval_dataset.csv`
- Dataset dimensions stated in the application: 4,269 rows × 13 columns.
- Target: `loan_status` (Approved / Rejected).
- Predictors used by the prediction interface: dependents, education, self-employment, annual income, loan amount, loan term, CIBIL score, residential assets, commercial assets, luxury assets, and bank assets.
- The source dataset's original publisher, collection process, licence, and representativeness are not documented in the current repository.

Before using the data beyond the present academic demonstration, document its source, collection context, permission/licence, class distribution, missingness, and known limitations.

## Model and workflow

The app loads the serialized artifact using Joblib and supplies a DataFrame containing the 11 applicant attributes listed above. It obtains the predicted class and the class probabilities from the saved estimator/pipeline. The interface also displays an illustrative project risk band using fixed approval-probability thresholds; this is a UI label, not a validated banking risk grade.

### Local explanation method

For a requested individual prediction, the app uses SHAP's model-agnostic permutation explainer around the complete saved pipeline's Approved-class probability. It uses up to 40 deterministic reference rows from the bundled dataset. Categorical inputs are encoded for the SHAP masker and decoded before calling the original pipeline. The result reports signed contributions in probability units and checks that the baseline plus contributions reconciles with the model output.

Gemini is optional and only narrates the measured SHAP evidence. A deterministic local summary remains available when Gemini is unconfigured or unavailable. SHAP contributions are local model attributions, not causal explanations or validated lending rules. Correlated inputs can share attribution, and results depend on the chosen background records and permutation approximation.

The repository's experiment page separately constructs preprocessing pipelines for uploaded datasets:
- numerical columns: median imputation;
- categorical columns: most-frequent imputation followed by one-hot encoding;
- classifiers: Decision Tree, Bagging, Random Forest, AdaBoost, and Gradient Boosting;
- evaluation: stratified cross-validation, accuracy, F1, ROC-AUC, train/validation gaps, and ROC curves.

A complete training script/notebook for generating the committed `loan_model.pkl` artifact is not present in the current repository. Consequently, the exact estimator configuration, training split, feature transformations, and artifact-generation process cannot be fully reconstructed from the repository alone.

## Reported performance

The comparison page currently displays the following previously reported values:

| Model | Validation accuracy | Validation F1 | Validation ROC-AUC |
|---|---:|---:|---:|
| Decision Tree | 0.9782 | 0.9825 | 0.9771 |
| Bagging | 0.9843 | 0.9875 | 0.9975 |
| Random Forest | 0.9796 | 0.9837 | 0.9967 |
| AdaBoost | 0.9590 | 0.9669 | 0.9948 |
| Gradient Boosting | 0.9803 | 0.9843 | 0.9981 |

These figures are hard-coded in the comparison page and are not regenerated when that page is opened. The experiment runner produces new results for an uploaded dataset using its own model definitions and cross-validation workflow. These two result sources should not be assumed to be identical or directly comparable without reproducing the original experiment.

No independent external test-set results, confidence intervals, calibration analysis, or external validation are documented in the repository.

## Fairness and subgroup analysis

The fairness page presents predefined metric values for education and self-employment categories. Its own page description states that the values are not recalculated dynamically from the CSV each time the page loads. They should therefore be treated as static reported project figures, not as a reproducible audit.

A more complete assessment would require:
- documented and validated subgroup definitions;
- dynamic calculation from a clearly specified evaluation set;
- subgroup sample sizes and uncertainty intervals;
- relevant metrics selected for the use context;
- investigation of data and measurement limitations; and
- independent legal, ethical, and domain review.

Differences between groups do not by themselves demonstrate discrimination or identify a cause.

## Known limitations

1. The source is attributed to Archit Sharma's Kaggle dataset, but the current licence terms and redistribution permission still need to be verified. The dataset's original collection process and representativeness are not established.
2. A complete training script for recreating the saved model artifact is absent.
3. The comparison-page metrics are embedded reported values rather than freshly computed values.
4. The fairness-page metrics are predefined and are not dynamically recomputed from the dataset.
5. No independent test-set, external-population, calibration, robustness, or uncertainty results are documented.
6. SHAP explanations are local attributions relative to a reference sample, not causal explanations. Correlated features can share attribution, and results depend on the background sample and permutation approximation. Gemini is an optional narration layer; when configured, applicant inputs, model output, and SHAP contributions are sent to Google's Gemini API. Use synthetic demonstration data only. Gemini does not produce the prediction and its narrative is not evidence that the prediction is correct.
7. The committed CSV contains 28 negative `residential_assets_value` values (minimum -100,000); their meaning should be checked before retraining or drawing conclusions.\n8. Model outputs may reflect patterns and limitations in the training data and should not be generalised to other populations.

## Responsible-use statement

This model is for academic learning and demonstration only. It must not be used as a substitute for a qualified lender's underwriting process, and it must not be used to make decisions that affect real people.
