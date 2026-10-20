# 🇿🇦 IDA117V S2 2026: Data Science for Better Service Delivery in South Africa

**Module**: Introduction to Data Science (IDA117V) | Second Semester 2026  
**Assessment**: Group Project (100 Marks)  
**Central Challenge**: *How can responsible data science help a South African public-service stakeholder identify need, prioritise limited resources, or improve the reliability and reach of a service?*

---

## 📌 1. Project Purpose & Executive Summary
In South Africa, municipal service delivery failures—spanning water pipe bursts, sewage overflows, electrical transformer overloads, and refuse non-collection—disproportionately impact vulnerable communities and trigger widespread social unrest. 

This project delivers an end-to-end, reproducible, and statistically validated machine-learning solution that classifies 3,500 municipal wards into three actionable vulnerability tiers:
* **Tier 0: Low Risk (Routine Maintenance)**
* **Tier 1: Moderate Vulnerability (14-Day Proactive Inspection)**
* **Tier 2: Critical Outage Risk (Immediate Emergency Intervention & Resource Pre-positioning)**

The solution moves beyond naive accuracy: it establishes a strict split-before-fit protocol, enforces POPIA compliance, compares transparent baselines with traditional and deep neural architectures, diagnoses overfitting, optimizes a locked champion pipeline, conducts three controlled ablations, and validates performance credibility via a paired exact McNemar test ($\alpha = 0.05$).

---

## 🗂️ 2. Repository Layout

```text
ida117v_project/
├── data/
│   ├── raw/
│   │   └── sa_municipal_service_delivery.csv # Raw ward dataset (3,500 records)
│   └── processed/
│       └── clean_service_delivery.csv        # Deduplicated, audited dataset
├── docs/                                     # Submission documentation & presentation
│   ├── technical_report.md                   # 15-20 Page comprehensive technical report
│   ├── contribution_statement.md             # Signed 6-member contribution matrix
│   ├── presentation_slides.md                # 14-slide presentation script & speaker notes
│   └── presentation.html                     # Interactive in-browser slide deck with timer
├── figures/                                  # 10 Publication-ready figures
│   ├── fig1_target_distribution.png          # Target class balance
│   ├── fig2_missingness_matrix.png           # Missingness & quality audit
│   ├── fig3_infra_age_vs_target.png          # Feature-target (Asset Age)
│   ├── fig4_informal_vs_vulnerability.png    # Feature-target (Informal % vs Load)
│   ├── fig5_provincial_disparity.png         # Geographic provincial disparity
│   ├── fig6_roc_curves.png                   # Combined macro One-vs-Rest ROC curves
│   ├── fig7_learning_curves.png              # Neural loss & macro-F1 learning curves
│   ├── fig8_model_comparison_bar.png         # Multi-metric comparative bar chart
│   ├── fig9_confusion_matrices.png           # 5-panel normalized confusion matrices
│   └── fig10_ablation_deltas.png             # Ablation delta performance plot
├── models/
│   └── champion_pipeline.joblib              # Serialized locked champion pipeline
├── notebooks/                                # 4 Interactive Jupyter Notebooks
│   ├── 01_eda_and_audit.ipynb                # Q1 & Q2: Data Audit, Missingness & EDA
│   ├── 02_model_training.ipynb               # Q3 & Q4: Leakage-Free Pipeline & Model Zoo
│   ├── 03_optimisation.ipynb                 # Q5: Champion Tuning & Isolated Test Eval
│   └── 04_ablation_mcnemar.ipynb             # Q6 & Q7: Ablations, McNemar & Verification
├── reports/                                  # Evidence logs & tables
│   ├── data_dictionary.md                    # Complete data dictionary
│   ├── model_validation_comparison.csv       # Multi-metric validation table
│   ├── classification_reports.md             # Per-model classification reports
│   ├── champion_optimisation_comparison.csv  # Pre- vs post-tuning metrics
│   ├── final_test_metrics.csv                # One-time locked test set metrics
│   ├── ablation_study_results.csv            # 3 Controlled ablation results
│   ├── mcnemar_test_results.json             # Exact McNemar statistical test results
│   └── mcnemar_table.md                      # 2x2 Contingency table & statistical decision
├── src/
│   ├── __init__.py
│   ├── data_generator.py                     # Stats SA grounded data generator
│   ├── audit_and_eda.py                      # Data audit & 5 purposeful figures (Q2)
│   ├── pipeline.py                           # Leakage-free ColumnTransformer & split (Q2)
│   ├── train_models.py                       # Baseline + 4 substantive models (Q3 & Q4)
│   ├── optimize_champion.py                  # Optuna/CV champion tuning & locked test (Q5)
│   ├── ablation_mcnemar.py                   # Controlled ablations & McNemar test (Q6)
│   ├── app.py                                # Gradio stakeholder web application (Q7)
│   └── verify_cases.py                       # 3 Valid cases + 1 invalid error test (Q7)
├── run_pipeline.py                           # Single-command master pipeline runner
├── requirements.txt                          # Locked Python environment dependencies
├── dataset_card.md                           # Metadata, provenance & POPIA compliance
└── technical_report.md                       # Comprehensive 15-20 page technical report
```

---

## ⚙️ 3. Installation & Environment Setup

Ensure Python 3.10+ (or Python 3.14) is installed. Install all locked dependencies:

```bash
# Navigate to the project directory
cd ida117v_project

# Install required dependencies
python -m pip install -r requirements.txt
```

---

## 🚀 4. Reproducible Execution

To execute the entire end-to-end pipeline from scratch (data generation, audit, 5 EDA figures, training 5 models, tuning the champion, evaluating the held-out test set, executing 3 ablations, running McNemar's test, and verifying UI cases):

```bash
python run_pipeline.py
```

All 10 figures and evidence tables will be automatically generated and saved into `figures/` and `reports/`.

---

## 🖥️ 5. Launching the Stakeholder User Interface

The deployment interface is built with Gradio and runs the locked `champion_pipeline.joblib`:

```bash
python src/app.py
```
Open your browser at `http://127.0.0.1:7860`.

### Demonstration Test Cases:
1. **Case 1 (Low Risk)**: City of Cape Town Metro Urban Ward (98% piped water, substation load 0.62, 1 burst).  
   *Result*: `🟢 Low Risk (Routine Service)` (98.4% Confidence).
2. **Case 2 (Moderate Vulnerability)**: Mangaung Formal Town Ward (78% piped water, asset age 38 yrs, 5 bursts).  
   *Result*: `🟡 Moderate Vulnerability (Active Monitoring)` (87.2% Confidence).
3. **Case 3 (Critical Outage Risk)**: City of Johannesburg Informal Settlement (78% informal dwellings, substation load 1.35, 11 bursts, 16 trips).  
   *Result*: `🔴 Critical Outage Risk (Emergency Intervention)` (96.8% Confidence).
4. **Case 4 (Invalid Input)**: Population density = -500, Informal dwelling % = 145%.  
   *Result*: `⚠️ Input Validation Error` with clear user feedback.

---

## ⚖️ 6. Ethical Governance & POPIA Safeguards
* **POPIA Act No. 4 of 2013**: Zero personal, confidential, or household-level identifiable records are retained. Data is aggregated to ward centroids ($>1,000$ households).
* **Reporting Bias Mitigation**: Mitigates digital divide disparities where affluent wards log complaints on mobile apps at higher rates than rural areas, by anchoring the model in physical asset telemetry (substation load factors, distribution age) rather than ticket counts alone.
* **Human-in-the-Loop**: The model serves as an advisory triage tool; all capital allocation decisions require certified municipal engineer review.

---

## 👥 7. Team Roles & Contribution Matrix
* **Project & Stakeholder Lead**: Problem formulation, public value mapping, cost matrix, POPIA governance (Question 1).
* **Data Governance & Preparation Lead**: Data dictionary, audit, deduplication, leakage prevention, reproducible ColumnTransformer pipeline (Question 2).
* **EDA & Visualisation Lead**: 5 purposeful visualisations, units, styling, and interpretive commentary (Question 2).
* **Traditional Modelling Lead**: Logistic Regression, XGBoost, cross-validation, hyperparameter optimization (Questions 3, 4, 5).
* **Neural Modelling Lead**: Multi-Layer Perceptron (MLP) and PyTorch Tabular ResNet with skip connections and learning curves (Questions 3 & 4).
* **Evaluation, Deployment & Reproducibility Lead**: Ablation study, exact McNemar test, Gradio UI deployment, test case verification, package packaging (Questions 6, 7, 8).

---

## 📽️ 8. Presentation Deck & Demonstration Instructions

The project includes an interactive, browser-based slide deck complete with speaker notes, embedded metrics, and an integrated presentation timer:

1. **Launch Interactive Slide Deck**:
   Open `docs/presentation.html` in Google Chrome, Microsoft Edge, or any modern web browser:
   ```powershell
   # Open directly in default browser on Windows
   start docs/presentation.html
   ```
2. **Keyboard Navigation**:
   * Press **Right Arrow (▶)** or **Spacebar** to move to the next slide.
   * Press **Left Arrow (◀)** to return to the previous slide.
   * Click **Start / Pause** in the top-right header to track your 10–12 minute presentation time.
3. **Markdown Slides & Speaker Notes**:
   Review slide-by-slide speaker scripts and anticipated panel questions in [`docs/presentation_slides.md`](docs/presentation_slides.md).
4. **Live UI Demo (Question 7)**:
   Keep the Gradio application running at `http://127.0.0.1:7860` and switch to the browser tab during Slide 12 to demonstrate the live prediction cases.

---

## 📦 9. Submission Checklist (100 Marks Covered)

| Rubric Question | Requirement | Implemented Deliverable | Verification Status |
| :---: | :--- | :--- | :---: |
| **Q1 (10 Marks)** | Problem framing, cost matrix, POPIA & ethical governance | Section 1 in `docs/technical_report.md`, `dataset_card.md` | ✅ Verified |
| **Q2 (18 Marks)** | Data audit, data dictionary, 5 purposeful EDA figures, leakage-free pipeline | `reports/data_dictionary.md`, `figures/fig1`–`fig5`, `src/pipeline.py` | ✅ Verified |
| **Q3 (18 Marks)** | 1 Naïve baseline + 4 substantive models (2 traditional, 2 neural) | `src/train_models.py`, `reports/model_validation_comparison.csv` | ✅ Verified |
| **Q4 (16 Marks)** | Overfitting diagnostics, learning curves, ROC overlays, confusion matrices | `figures/fig6`–`fig9`, `reports/classification_reports.md` | ✅ Verified |
| **Q5 (10 Marks)** | 5-Fold CV hyperparameter tuning, locked champion, isolated test set evaluation | `src/optimize_champion.py`, `models/champion_pipeline.joblib`, `final_test_metrics.csv` | ✅ Verified |
| **Q6 (10 Marks)** | 3 controlled ablations & paired McNemar test ($\alpha=0.05$) | `reports/ablation_study_results.csv`, `fig10_ablation_deltas.png`, `reports/mcnemar_table.md` | ✅ Verified |
| **Q7 (7 Marks)** | Deployed Web UI (Gradio), validation handling, 4 demonstration cases | `src/app.py`, `src/verify_cases.py`, verified at `http://127.0.0.1:7860` | ✅ Verified |
| **Q8 (7 Marks)** | Reproducible submission package, documentation, notebooks, contribution matrix | `notebooks/` (4 notebooks), `docs/contribution_statement.md`, `docs/presentation.html` | ✅ Verified |

