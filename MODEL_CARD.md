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

The app loads the serialized artifact using Joblib and supplies a DataFrame containing the 11 applicant attributes listed above. It obtains the predicted class and the class probabilities from the saved estimator/pipeline.

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

1. Dataset provenance and redistribution permissions are not documented in the repository.
2. A complete training script for recreating the saved model artifact is absent.
3. The comparison-page metrics are embedded reported values rather than freshly computed values.
4. The fairness-page metrics are predefined and are not dynamically recomputed from the dataset.
5. No independent test-set, external-population, calibration, robustness, or uncertainty results are documented.
6. Gemini explanations are an optional language layer. They describe the model output and must not be treated as the source of the prediction or as evidence that the prediction is correct.
7. Model outputs may reflect patterns and limitations in the training data and should not be generalised to other populations.

## Responsible-use statement

This model is for academic learning and demonstration only. It must not be used as a substitute for a qualified lender's underwriting process, and it must not be used to make decisions that affect real people.
