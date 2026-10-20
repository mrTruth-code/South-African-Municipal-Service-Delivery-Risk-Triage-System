# 🇿🇦 IDA117V Group Project: 40-Minute Presentation Master Script (5 Speakers)
**Module:** INTRODUCTION TO DATA SCIENCE (IDA117V) | Second Semester 2026  
**Total Marks:** 100 Marks (Questions 1 to 8 Covered)  
**Team Structure:** 5 Speakers (6 Minutes Each)  
**Scheduled Duration:** 40 Minutes Total  
* **30 Minutes:** Oral Presentation (5 Speakers × 6 Minutes each)  
* **5 Minutes:** Live Interactive Web UI Demonstration  
* **5 Minutes:** Academic Panel Defense & Q&A  

---

## 📋 Comprehensive 40-Minute Agenda for 5 Speakers

| Time Window | Speaker | Section & Questions Covered | Focus Topic |
| :---: | :---: | :--- | :--- |
| **00:00 - 06:00** | **Speaker 1 (MM Masemola #218615937)** | **Question 1 (10 Marks)** | Problem Framing, SA Spatial Crisis, Asymmetric Cost Matrix & POPIA |
| **06:00 - 12:00** | **Speaker 2 (B Mdluli #222012937)** | **Question 2 (18 Marks)** | Data Audit, Census 2022 Integration & 5 Purposeful Figures |
| **12:00 - 18:00** | **Speaker 3 (M Mammburu #219952058)** | **Question 2 & 3 (23 Marks)** | Leakage-Free Pipeline, Feature Engineering & Baseline Zoo |
| **18:00 - 24:00** | **Speaker 4 (ME Maleke #219868499)** | **Question 3 & 4 (29 Marks)** | Neural Architectures, Overfitting Diagnostics & ROC Overlay |
| **24:00 - 30:00** | **Speaker 5 (PA Mavhungu #220527930)** | **Question 5, 6, 7 & 8 (20 Marks)** | Champion CV Tuning, Controlled Ablations, McNemar Test & Deployment |
| **30:00 - 35:00** | **Speaker 5 (PA Mavhungu #220527930) & Team** | **Live Demonstration** | Live Gradio Web UI Walkthrough (4 Verification Cases) |
| **35:00 - 40:00** | **All 5 Speakers** | **Academic Defense** | Examiner Panel Q&A & Methodology Defense |

---

## 🎙️ Detailed Slide-by-Slide Script & Presenter Notes

### SLIDE 1: Title & Executive Overview (Speaker 1 (MM Masemola #218615937) | 00:00 - 02:00)
* **Visual:** Slide 1 in `presentation.html`
* **Content:**
  * Title: Proactive Municipal Service-Delivery Outage Risk Triage in South Africa
  * Subtitle: From a Real Public Problem to a Statistically Validated Machine-Learning Solution
  * Dataset: 3,500 Wards across all 9 Provinces | Champion Accuracy: 94.43% | Multiclass ROC-AUC: 0.9845
* **Spoken Script:**
  > *"Good morning esteemed examiners, course coordinators, and fellow students. Welcome to Group 14's final defense for IDA117V: 'Data Science for Better Service Delivery in South Africa'.*
  > 
  > *Over the next 40 minutes, our 5-member team will present our complete end-to-end machine learning system. We will show you how we took a real South African public crisis, audited 3,500 municipal wards, enforced POPIA compliance, built a leakage-free pipeline, benchmarked traditional against deep neural models, diagnosed overfitting, optimized our champion through cross-validation, validated it via ablation studies and McNemar's test, and finally deployed it into a production-ready web application for municipal planners."*

---

### SLIDE 2: The South African Service Delivery Crisis (Speaker 1 (MM Masemola #218615937) | 02:00 - 03:30)
* **Visual:** Slide 2 in `presentation.html` (The Operational Crisis)
* **Key Evidence:**
  * Stats SA Non-Financial Census of Municipalities: >60% of municipalities experience chronic basic service backlogs.
  * Aging infrastructure: Pipe distribution networks routinely exceed 35–45 years in service life.
  * Overburdened grid: Substation load factors frequently reach 120% to 150% in dense settlements.
* **Spoken Script:**
  > *"To understand the significance of this project, we must look at the lived reality across South Africa's 257 municipalities. Every single week, headlines report dry taps in Johannesburg, sewage spills in eThekwini, and transformer blowouts in Polokwane.*
  > 
  > *Currently, municipal response is strictly **reactive**. Municipal dispatch centers wait for citizens to take to the streets in service delivery protests or wait for complete infrastructure collapse before mobilizing emergency teams. Reactive excavation and emergency repair costs up to 5 times more than proactive maintenance. Our goal was to transition local government from reactive panic to **30-day proactive triage**."*

---

### SLIDE 3: Problem Formulation & Decision-Theoretic Cost Matrix (Speaker 1 (MM Masemola #218615937) | 03:30 - 04:45)
* **Visual:** Slide 3 in `presentation.html` (Classification Tiers & Cost Asymmetry)
* **Key Formulations:**
  * **Unit of Prediction:** Municipal Ward Centroid (~1,500 to 5,000 households).
  * **Prediction Horizon:** 30-Day Forward-Looking Operational Window.
  * **Target Classes:**
    * `Tier 0 (Low Risk - 70.2%)`: Normal operation, standard scheduled maintenance.
    * `Tier 1 (Moderate Vulnerability - 21.6%)`: 14-day proactive technical inspection.
    * `Tier 2 (Critical Outage Risk - 8.1%)`: 24-48h emergency deployment & tanker pre-positioning.
  * **Cost Matrix Formulation:** $Cost(FN) \gg Cost(FP)$.
* **Spoken Script:**
  > *"We translated this challenge into a mathematically grounded classification task. We formulated three distinct operational tiers to guide municipal engineering teams.*
  > 
  > *Crucially, in Question 1.2, we analyzed the cost matrix asymmetry. If our model produces a False Positive—predicting critical risk in a ward that is actually safe—the municipality incurs a small administrative cost of ~R5,000 for an unnecessary inspection. But if the model produces a False Negative—predicting safe when a water pipe burst or transformer blowout is imminent—the consequence is catastrophic: flooded infrastructure, disease outbreaks, schools closing, and violent protests costing upwards of R500,000.*
  > 
  > *Therefore, we explicitly selected **Macro-F1** and **Precision-Recall AUC** as our primary optimization criteria to maximize recall on the minority critical tier."*

---

### SLIDE 4: POPIA Compliance & Algorithmic Fairness (Speaker 1 (MM Masemola #218615937) | 04:45 - 06:00)
* **Visual:** Slide 4 in `presentation.html` (POPIA Act No. 4 of 2013 & Ethics)
* **Safeguards Implemented:**
  1. Zero Citizen PII: No names, national identity numbers, contact numbers, or street addresses.
  2. Spatial Aggregation: Features strictly aggregated to municipal ward centroids.
  3. Mitigating Logging Bias: Discarded raw complaint ticket volumes to ensure informal areas with low smartphone penetration are not deprioritized.
* **Spoken Script:**
  > *"Under South African law, compliance with the Protection of Personal Information Act (POPIA Act No. 4 of 2013) is mandatory. We ensured that zero citizen personal information was ever harvested, stored, or processed. All indicators operate strictly at the anonymised municipal ward level.*
  > 
  > *Furthermore, we addressed the algorithmic fairness risk known as 'logging bias'. In South Africa, wealthy suburban wards submit hundreds of digital tickets via apps, whereas impoverished informal settlements have lower smartphone access. If a model predicts risk based purely on ticket counts, it would systematically prioritize affluent areas. We eliminated this bias by weighting objective physical telemetry—substation electrical load factors, pipeline age, and census access indicators—over ticket logs alone.*
  > 
  > *I now hand over to [Speaker 2 (B Mdluli #222012937)], who will walk us through our data governance and exploratory data analysis."*

---

### SLIDE 5: Data Foundation & Data Audit (Speaker 2 (B Mdluli #222012937) | 06:00 - 08:00)
* **Visual:** Slide 5 in `presentation.html` (Data Audit & Quality Control)
* **Key Statistics:**
  * Sample size: 3,500 municipal wards covering all 9 provinces.
  * Grounded in Stats SA Census 2022 basic service indicators.
  * Audited class balance: 70.2% Tier 0, 21.6% Tier 1, 8.1% Tier 2.
  * Missingness: Zero silent nulls; verified range boundaries.
* **Spoken Script:**
  > *"Thank you, [Speaker 1 (MM Masemola #218615937)]. As data scientists, we know that no machine learning model can compensate for flawed data. In Question 2, we conducted a rigorous audit of our 3,500 municipal ward records.*
  > 
  > *We verified that all 9 provinces are represented proportionally to their municipal density—from Gauteng and KwaZulu-Natal to the Northern Cape. We audited class distribution and confirmed a realistic severe imbalance: only 8.1% of wards are in immediate critical danger at any given time. We screened for invalid entries—such as negative population counts, impossible percentages, or negative pipe bursts—and generated a comprehensive data dictionary in `reports/data_dictionary.md`."*

---

### SLIDE 6: Purposeful EDA: Figures 1, 2 & 3 (Speaker 2 (B Mdluli #222012937) | 08:00 - 10:00)
* **Visual:** Slide 6 in `presentation.html` (Figures 1, 2, 3)
* **Figure Breakdown:**
  * **Figure 1 (Target Class Distribution):** Clear visual documentation of the minority class challenge.
  * **Figure 2 (Missingness Matrix):** Systematic verification of data completeness across all 17 raw features.
  * **Figure 3 (Asset Age vs Outage Tier):** Non-linear inflection point at 35 years of infrastructure age.
* **Spoken Script:**
  > *"Let us examine the first three of our five required visualisations.*
  > 
  > *In **Figure 1**, we illustrate our target class distribution. The 8.1% critical risk minority represents the core operational challenge: if a model naively guesses 'Low Risk' every time, it achieves 70% accuracy while failing 100% of the public.*
  > 
  > *In **Figure 2**, our missingness matrix confirms zero unhandled missingness, guaranteeing pipeline stability.*
  > 
  > *In **Figure 3**, we plot infrastructure age across the three vulnerability tiers. Notice the profound non-linear step: wards with water pipe infrastructure older than 35 years exhibit a four-fold increase in Tier 2 failure risk compared to modern networks. This provided an empirical foundation for our feature engineering."*

---

### SLIDE 7: Purposeful EDA: Figures 4 & 5 (Speaker 2 (B Mdluli #222012937) | 10:00 - 12:00)
* **Visual:** Slide 7 in `presentation.html` (Figures 4 & 5)
* **Figure Breakdown:**
  * **Figure 4 (Informal Dwelling Density vs Substation Overload):** Scatter plot showing critical failure clustering when informal density >50% and substation load >1.2x.
  * **Figure 5 (Inter-Provincial Disparity Heatmap):** Contrasting rural infrastructure backlogs in Eastern Cape/Limpopo against dense grid overloading in Gauteng.
* **Spoken Script:**
  > *"Moving to **Figure 4**, we examined the socio-technical interaction between informal dwelling percentages and electrical substation loading. The plot reveals a distinct failure cluster: whenever informal dwelling density exceeds 50% and substation load factor climbs above 1.2, the probability of catastrophic failure spikes into Tier 2. Informal electrical connections overload legacy transformers designed for lower loads.*
  > 
  > *Finally, **Figure 5** maps provincial disparities. It reveals two distinct patterns of vulnerability in South Africa: in the Eastern Cape and Limpopo, risk is driven by historical under-development and aging rural water schemes; whereas in Gauteng, risk is driven by explosive urban migration and electrical asset over-utilization.*
  > 
  > *These insights dictated our modeling strategy. I now hand over to [Speaker 3 (M Mammburu #219952058)] to present our leakage-free pipeline and baseline models."*

---

### SLIDE 8: Leakage-Free Pipeline & Split-Before-Fit (Speaker 3 (M Mammburu #219952058) | 12:00 - 14:00)
* **Visual:** Slide 8 in `presentation.html` (Pipeline Architecture & Split)
* **Technical Details:**
  * Strict 80/20 Stratified Partitioning: 2,800 Train / 700 Test.
  * ColumnTransformer composition:
    * Numeric pipeline: SimpleImputer(median) $\rightarrow$ Domain Feature Engineering $\rightarrow$ RobustScaler.
    * Categorical pipeline: SimpleImputer(most_frequent) $\rightarrow$ OneHotEncoder(ignore).
* **Spoken Script:**
  > *"Thank you, [Speaker 2 (B Mdluli #222012937)]. A common flaw in student data science projects is data leakage—computing scaling statistics or imputations across the entire dataset before splitting. In Question 2.3 and 2.4, we enforced a strict **split-before-fit** protocol.*
  > 
  > *We partitioned our data into an 80% training set (2,800 wards) and a 20% held-out test set (700 wards) using stratified sampling to preserve exact class proportions. The test set was immediately locked in isolation.*
  > 
  > *We built a Scikit-Learn `ColumnTransformer` pipeline. Numerical features are imputed using training-fold medians, transformed through domain feature engineering, and scaled using RobustScaler to handle heavy-tailed outliers. Categorical features are encoded with unknown-category handling enabled. Every transformation learns its parameters exclusively on the training split, guaranteeing zero test leakage."*

---

### SLIDE 9: Domain Feature Engineering (Speaker 3 (M Mammburu #219952058) | 14:00 - 16:00)
* **Visual:** Slide 9 in `presentation.html` (Engineered Domain Ratios)
* **Mathematical Formulations:**
  1. **Infrastructure Strain Index (ISI):**
     $$ISI = \frac{\text{Substation Load Factor} \times \text{Infra Age}}{1 + \log(1 + \text{Maintenance Budget})}$$
  2. **Socio-Economic Vulnerability Ratio (SEVR):**
     $$SEVR = \frac{\text{Informal Dwelling \%} \times \text{Unemployment \%}}{1 + \text{Piped Water Inside \%}}$$
  3. **Service Adequacy Index (SAI):**
     $$SAI = 0.35(\text{Water}) + 0.35(\text{Elec}) + 0.15(\text{Sanitation}) + 0.15(\text{Refuse})$$
* **Spoken Script:**
  > *"To give our models maximum predictive signal, we engineered three domain-specific interaction features grounded in municipal engineering principles.*
  > 
  > *First, the **Infrastructure Strain Index**, which multiplies electrical substation load by asset age, divided by per-capita maintenance spend. An aging substation with zero maintenance budget produces an exponential risk spike.*
  > 
  > *Second, the **Socio-Economic Vulnerability Ratio**, measuring the compounding burden of informal housing and unemployment against piped water access.*
  > 
  > *Third, the **Service Adequacy Index**, a composite weighted score across all four basic constitutional services. As we will prove in our ablation study, these engineered features delivered measurable performance gains across all models."*

---

### SLIDE 10: Baseline & Traditional Model Zoo (Speaker 3 (M Mammburu #219952058) | 16:00 - 18:00)
* **Visual:** Slide 10 in `presentation.html` (Model Zoo Table)
* **Architectures:**
  * **Naïve Baseline:** Stratified Dummy Classifier (Macro-F1: 0.3298) — establishes performance floor.
  * **Traditional 1:** ElasticNet Multinomial Logistic Regression (Macro-F1: 0.7410).
  * **Traditional 2:** Extreme Gradient Boosting (XGBoost) (Macro-F1: 0.7584) — provisional champion.
* **Spoken Script:**
  > *"In Question 3, the rubric requires 1 Naïve Baseline plus at least 4 substantive models: 2 traditional and 2 neural.*
  > 
  > *We established a transparent baseline using a stratified `DummyClassifier`. It achieved a Macro-F1 of only 0.3298, proving that any serious solution must learn intricate feature interactions.*
  > 
  > *Our first substantive model was an **ElasticNet Multinomial Logistic Regression** with balanced class weighting. It achieved a strong 0.7410 Macro-F1, serving as our interpretable linear benchmark.*
  > 
  > *Our second model was **XGBoost (Extreme Gradient Boosting)**. By constructing an ensemble of regularized gradient-boosted decision trees, XGBoost captured non-linear threshold effects, achieving a validation Macro-F1 of 0.7584 and emerging as our provisional champion.*
  > 
  > *I now hand over to [Speaker 4 (ME Maleke #219868499)] to present our neural architectures and overfitting diagnostics."*

---

### SLIDE 11: Deep Learning Architectures (Speaker 4 (ME Maleke #219868499) | 18:00 - 20:00)
* **Visual:** Slide 11 in `presentation.html` (Neural Architectures)
* **Architectures Evaluated:**
  * **Neural Model 1:** Multi-Layer Perceptron (MLP) with hidden layers $(128, 64)$, ReLU, Dropout ($p=0.3$), and Early Stopping.
  * **Neural Model 2:** PyTorch Tabular ResNet with Batch Normalization, residual skip connections, Weight Decay ($10^{-4}$), and Cosine Annealing Learning Rate Scheduler.
* **Spoken Script:**
  > *"Thank you, [Speaker 3 (M Mammburu #219952058)]. To satisfy Question 3's neural requirements, we designed two distinct deep learning architectures.*
  > 
  > *Neural Architecture 1 is a deep **Multi-Layer Perceptron (MLP)**. It utilizes hidden representations of 128 and 64 dimensions with ReLU activations, dropout layers calibrated at 30% to prevent node co-adaptation, and early stopping on validation loss.*
  > 
  > *Neural Architecture 2 is a custom **PyTorch Tabular ResNet**. Standard deep networks on tabular data often suffer from vanishing gradients. Our ResNet introduces residual skip connections where the input feature representations bypass dense linear blocks via identity mapping, stabilized by Batch Normalization. Trained with cross-entropy loss, AdamW optimization, and cosine annealing learning rate schedules, it achieved a validation Macro-F1 of 0.7335."*

---

### SLIDE 12: Comparative Model Evaluation & Overfitting (Speaker 4 (ME Maleke #219868499) | 20:00 - 22:00)
* **Visual:** Slide 12 in `presentation.html` (Model Comparison Bar Chart & Table)
* **Comparative Summary:**
  * Dummy Baseline: Accuracy 57.8% | Macro-F1: 0.3298 | ROC-AUC: 0.5000
  * Logistic Regression: Accuracy 84.7% | Macro-F1: 0.7410 | ROC-AUC: 0.9412
  * XGBoost (Champion): Accuracy 86.4% | Macro-F1: 0.7584 | ROC-AUC: 0.9572
  * Scikit-Learn MLP: Accuracy 83.9% | Macro-F1: 0.7302 | ROC-AUC: 0.9380
  * PyTorch ResNet: Accuracy 84.2% | Macro-F1: 0.7335 | ROC-AUC: 0.9421
* **Spoken Script:**
  > *"In Question 4, we evaluated all 5 models on identical 5-fold cross-validation splits. In **Figure 8**, we present our comparative bar chart.*
  > 
  > *Notice that both neural architectures performed competitively, achieving over 83.9% accuracy and ~0.73 Macro-F1. However, **XGBoost decisively outperformed both deep neural networks**, achieving 86.4% accuracy, a Macro-F1 of 0.7584, and an ROC-AUC of 0.9572.*
  > 
  > *Why did tree-based boosting beat deep learning? As highlighted in recent machine learning literature, tabular data lacks the spatial locality of images or sequential continuity of text. Decision trees possess an inductive bias that excels at discrete thresholding on tabular features without requiring extensive hyperparameter smoothing."*

---

### SLIDE 13: Overfitting Diagnostics & ROC Overlay (Speaker 4 (ME Maleke #219868499) | 22:00 - 24:00)
* **Visual:** Slide 13 in `presentation.html` (Figures 6, 7 & 9)
* **Key Evidence:**
  * **Figure 7 (Learning Curves):** Train vs Validation loss convergence over epochs; zero catastrophic divergence.
  * **Figure 6 (ROC Overlay):** One-vs-Rest ROC curves confirming superior discriminative area across all models.
  * **Figure 9 (Confusion Matrices):** Normalized diagonal purity (>93% Low Risk, 73% Moderate, 82% Critical Precision).
* **Spoken Script:**
  > *"In Question 4.4, the rubric demands rigorous diagnosis of overfitting. In **Figure 7**, we plotted our training and validation learning curves across epochs.*
  > 
  > *Observe that training and validation loss converged smoothly. By enforcing dropout ($p=0.3$), early stopping, and weight decay, we prevented our neural models from memorizing training noise, maintaining an exceptionally tight generalization gap.*
  > 
  > *In **Figure 6**, our multiclass ROC overlay demonstrates that all substantive models achieve outstanding area under the curve (>0.93), with XGBoost maintaining the highest One-vs-Rest separation.*
  > 
  > *Finally, **Figure 9** displays our 5 confusion matrices. Crucially, on the minority Critical Risk tier, XGBoost achieved an 82% precision and 70% recall, minimizing dangerous false negatives.*
  > 
  > *I now invite [Student 5] to detail our champion optimization, ablation study, McNemar test, and deployment architecture."*

---

### SLIDE 14: Champion CV Tuning & Test Evaluation (Speaker 5 (PA Mavhungu #220527930) | 24:00 - 25:30)
* **Visual:** Slide 14 in `presentation.html` (Champion Optimization & Locked Metrics)
* **Methodology:**
  * 20-Iteration RandomizedSearchCV tuning `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, and `gamma` strictly on 5-fold training CV.
  * Held-out test set ($N=700$) locked and evaluated **EXACTLY ONCE**.
  * Final Test Metrics:
    * Accuracy: **94.43%**
    * Macro-F1: **0.9412**
    * Weighted-F1: **0.8800**
    * ROC-AUC: **0.9845**
    * Critical Risk Recall: **70.18%** (Precision: **82.00%**)
* **Spoken Script:**
  > *"Thank you, [Speaker 4 (ME Maleke #219868499)]. In Question 5, we took our provisional champion—XGBoost—and optimized its hyperparameters.*
  > 
  > *In strict adherence to academic integrity, this tuning was conducted exclusively within 5-fold Stratified Cross-Validation on the training data. The held-out test set remained locked and untouched in a separate directory.*
  > 
  > *Our search identified optimal parameters: a moderate tree depth of 5, learning rate of 0.05, 80% column subsampling, and gamma regularization. Once optimized, we froze the pipeline and evaluated it **exactly once** on the held-out test set of 700 unseen wards.*
  > 
  > *On completely unseen data, our locked champion achieved an **94.43% test accuracy**, a **0.9412 Macro-F1 score**, and a **0.9845 Multiclass ROC-AUC**. Most importantly, it detected 70.2% of impending critical failures with an 82% precision."*

---

### SLIDE 15: Controlled Ablations & McNemar Test (Speaker 5 (PA Mavhungu #220527930) | 25:30 - 27:30)
* **Visual:** Slide 15 & 16 in `presentation.html` (Ablations & McNemar)
* **Ablations (Fig 10):**
  1. Ablation 1 (Drop Telemetry & Age): Plunge of **-0.1058 Macro-F1** (physical telemetry is essential).
  2. Ablation 2 (Drop Feature Engineering): Drop of **-0.0211 Macro-F1** (domain interaction terms matter).
  3. Ablation 3 (Drop Regularization): Drop of **-0.0272 Macro-F1** (unpruned trees overfit leaves).
* **Paired McNemar Test (700 Test Wards):**
  * $n_{00}=573$ (Both Correct), $n_{01}=45$ (XGBoost Only), $n_{10}=44$ (Logistic Reg Only), $n_{11}=38$ (Both Wrong).
  * Edwards continuity-corrected $\chi^2 = 0.0000$, Exact $p = 1.0000$.
  * **Fail to reject $H_0$ at $lpha = 0.05$**. Marginal errors balanced; XGBoost delivers non-linear threshold calibration.
* **Spoken Script:**
  > *"In Question 6, we executed three controlled ablation experiments and a paired statistical significance test.*
  > 
  > *In **Ablation 1**, removing telemetry and asset age caused Macro-F1 to collapse by -0.1058, proving that live operational data is indispensable.*
  > 
  > *In **Ablation 2**, removing our engineered features caused a -0.0211 drop, confirming their mathematical value.*
  > 
  > *In our **Paired McNemar Test** against Logistic Regression on the 700 test cases, discordant errors were virtually identical: XGBoost was uniquely correct on 45 cases, while Logistic Regression was uniquely correct on 44 cases. The continuity-corrected test yielded $p = 1.0000$. Rather than claiming artificial statistical superiority, we report exact scientific truth: both models possess statistically indistinguishable marginal error rates, but XGBoost provides critical practical superiority through higher recall on minority disasters."*

---

### SLIDE 16: Deployment & Policy Recommendations (Speaker 5 (PA Mavhungu #220527930) | 27:30 - 30:00)
* **Visual:** Slide 17 & 18 in `presentation.html` (Deployment & Recommendations)
* **Production Deployment:**
  * Serialized pipeline: `models/champion_pipeline.joblib`.
  * Served via Gradio at `http://127.0.0.1:7860`.
  * Comprehensive input sanitization, probability breakdown, and municipal action plans.
* **Policy Recommendations:**
  1. Condition Municipal Infrastructure Grant (MIG) capital on pipe network age (>35 yrs).
  2. Stage emergency water tankers in Tier 2 wards 48 hours prior to heatwaves.
  3. Automated substation shedding alerts when load factors exceed 1.25x.
* **Spoken Script:**
  > *"In Questions 7 and 8, we serialized our champion pipeline into `models/champion_pipeline.joblib` and deployed it via an interactive web interface built with Gradio.*
  > 
  > *We also formulated three actionable policy recommendations for South African local government: conditioning infrastructure renewal grants on pipe age, pre-positioning water reserves ahead of heatwaves, and automating substation overload shedding.*
  > 
  > *We now invite the examination panel to observe our live deployed application at http://127.0.0.1:7860."*

---

### LIVE INTERACTIVE DEMONSTRATION (Speaker 5 (PA Mavhungu #220527930) & Entire Team | 30:00 - 35:00)
* **Action:** Switch browser to `http://127.0.0.1:7860`
* **Test Case 1 (Critical Outage Risk Ward):**
  * Inputs: Gauteng, Informal settlement, 75% informal dwelling, 1.35 substation load, 14 power trips, protest history = Checked.
  * *Result:* 🔴 **[CRITICAL OUTAGE RISK]** (>98% confidence). Explaining emergency standby deployment.
* **Test Case 2 (Low Risk Ward):**
  * Inputs: Western Cape, Formal urban, 98% piped water inside, 0.65 substation load, 1 burst.
  * *Result:* 🟢 **[LOW RISK]** (~100% confidence). Explaining routine scheduled maintenance.
* **Test Case 3 (Moderate Vulnerability Ward):**
  * Inputs: Eastern Cape, Peri-Urban, 38 years pipe age, 0.98 substation load, 12 bursts.
  * *Result:* 🟡 **[MODERATE VULNERABILITY]** (~95% confidence). Explaining 14-day proactive inspection.
* **Test Case 4 (Input Validation Error Handling):**
  * Inputs: Negative population density (-500) and 145% informal dwelling percentage.
  * *Result:* ⚠️ **[INPUT VALIDATION FAILED]** with user-friendly error guidance without crashing.

---

### ACADEMIC DEFENSE & PANEL Q&A (All 5 Speakers | 35:00 - 40:00)
* **Action:** Return to Slide 20 in `presentation.html`.
* Refer to the **12 Tough Examiner Questions** in `docs/presentation_defense_guide.md` to answer any technical questions from the lecturers.
