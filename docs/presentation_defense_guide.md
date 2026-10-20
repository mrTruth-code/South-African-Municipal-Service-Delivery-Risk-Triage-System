# 🇿🇦 IDA117V Group Project: 40-Minute Presentation & Academic Defense Guide (5 Speakers)
**Module:** Introduction to Data Science (IDA117V) | S2 2026  
**Project:** Data Science for Better Service Delivery in South Africa  
**Total Marks:** 100 Marks  
**Team Structure:** 5 Speakers  
**Total Scheduled Time:** 40 Minutes Total  
* **30 Minutes:** Oral Presentation (5 Speakers × 6 Minutes each)  
* **5 Minutes:** Live Interactive Web UI Demonstration (4 Cases)  
* **5 Minutes:** Academic Panel Defense & Lecturer Q&A  

---

## ⏱️ Master 40-Minute Agenda for 5 Speakers

```
[00:00 - 06:00] SPEAKER 1: Project Framing, SA Service Crisis, Cost Matrix & POPIA (Question 1)
[06:00 - 12:00] SPEAKER 2: Data Audit, Census 2022 Integration & 5 Purposeful Figures (Question 2)
[12:00 - 18:00] SPEAKER 3: Leakage-Free Pipeline, Feature Engineering & Baseline Zoo (Question 2 & 3)
[18:00 - 24:00] SPEAKER 4: Deep Neural Architectures, Overfitting Diagnostics & ROC Overlay (Question 3 & 4)
[24:00 - 30:00] SPEAKER 5: Champion CV Tuning, Controlled Ablations, McNemar Test & Deployment (Question 5, 6, 7 & 8)
[30:00 - 35:00] SPEAKER 5 & ENTIRE TEAM: Live Gradio Web UI Demonstration (4 Test Scenarios)
[35:00 - 40:00] ALL 5 SPEAKERS: Lecturer Panel Q&A & Academic Defense
```

---

## 🎙️ 5-Speaker Transitions & Hand-Off Scripts

* **Speaker 1 -> Speaker 2 (at 06:00):**  
  > *"Having established our problem framing, asymmetric cost matrix, and POPIA safeguards, I now hand over to [Student 2], who led our data governance and exploratory data analysis across 3,500 municipal wards."*

* **Speaker 2 -> Speaker 3 (at 12:00):**  
  > *"These exploratory findings underscored the urgent need for non-linear modeling. I now invite [Student 3] to walk through our leakage-free pipeline and baseline traditional models."*

* **Speaker 3 -> Speaker 4 (at 18:00):**  
  > *"While traditional models established strong linear boundaries, we also engineered neural architectures. [Student 4] will now present our deep learning models and overfitting diagnostics."*

* **Speaker 4 -> Speaker 5 (at 24:00):**  
  > *"With XGBoost emerging as our provisional champion, we subjected it to rigorous validation. I hand over to [Student 5] to detail our 5-fold CV hyperparameter tuning, ablation studies, McNemar test, and deployment architecture."*

* **Speaker 5 -> Live Demo (at 30:00):**  
  > *"We now invite the panel to observe our live deployed application running at http://127.0.0.1:7860 as we demonstrate 4 real-world municipal scenarios."*

---

## 🛡️ Academic Panel Q&A Defense: 12 Tough Examiner Questions

### Question 1: "Why did you use SMOTE or resampling only on the training set and not on the entire dataset?"
* **Model Answer:**  
  > *"Applying any resampling, imputation, or scaling prior to splitting causes catastrophic data leakage. If synthetic samples are generated before partitioning, the test set inherits information from the training distribution, artificially inflating test metrics. In our architecture, the 80/20 stratified split is performed strictly before any transformation, and Scikit-Learn's ColumnTransformer fits parameters exclusively on the training folds."*

### Question 2: "In your McNemar test, you obtained an exact p-value of 1.0000. Does that mean your champion model is a failure or no better than Logistic Regression?"
* **Model Answer:**  
  > *"Not at all. In academic research, reporting a high p-value honestly is a hallmark of scientific integrity. In our 2x2 contingency table across 700 test wards, the discordant pairs were almost perfectly balanced: XGBoost got 45 cases right that Logistic Regression missed, while Logistic Regression got 44 right that XGBoost missed (89 total discordant cases). McNemar tests only marginal error proportions (P(b) = P(c)). While the marginal error rates are statistically equivalent, XGBoost achieves superior non-linear calibration on the critical risk tier—achieving an 82% precision and 70.2% recall on minority Tier 2 cases compared to linear boundary distortion in Logistic Regression."*

### Question 3: "Why did Extreme Gradient Boosting (XGBoost) outperform your PyTorch Deep Tabular ResNet?"
* **Model Answer:**  
  > *"This reflects a well-documented finding in machine learning literature (e.g., Grinsztajn et al., 2022). Deep neural networks struggle with heterogeneous tabular data characterized by unnormalized coordinate scales, discrete categorical levels, and irregular decision boundaries. XGBoost's recursive axis-aligned tree splits and exact greedy search are inherently well-suited for tabular feature interactions, whereas neural networks require extensive tuning of weight decay and embedding dimensions to approximate similar step functions."*

### Question 4: "Why did you choose Macro-F1 as your primary technical metric instead of Accuracy?"
* **Model Answer:**  
  > *"Because our target classes have substantial natural imbalance: 70.2% Low Risk, 21.6% Moderate Vulnerability, and only 8.1% Critical Outage Risk. A trivial majority-class DummyClassifier achieves a 70.2% raw accuracy while completely ignoring every impending municipal disaster (achieving 0% recall on Tier 2). Macro-F1 weights each tier equally, forcing the model to achieve high performance on the minority disaster class rather than simply predicting the majority."*

### Question 5: "How does your model prevent algorithmic bias against poorer informal communities who may not log fault tickets?"
* **Model Answer:**  
  > *"This is the classic 'logging-bias' trap where smartphone-enabled suburban areas appear to have more complaints. We deliberately mitigated this in two ways: first, under POPIA Act No. 4 of 2013, we discarded all individual citizen complaints and aggregated strictly to ward centroids. Second, our model prioritizes physical asset telemetry—substation electrical load factors, pipeline age, and census service deprivation metrics—over digital ticket logs alone. Even if a shack settlement logs zero digital tickets, a substation load factor of 1.35x and 78% informal density immediately flags the area as Critical Risk."*

### Question 6: "What did your 3 ablation experiments prove?"
* **Model Answer:**  
  > *"Ablation 1 removed infrastructure age and operational failure telemetry, causing Macro-F1 to plunge by -0.1058 (from 0.7584 to 0.6526). This proved that physical asset age and telemetry are the single most influential determinants of imminent failure. Ablation 2 removed our engineered interaction terms, dropping Macro-F1 by -0.0211, validating the mathematical utility of our domain ratios. Ablation 3 removed tree regularization, dropping Macro-F1 by -0.0272, proving that unpruned deep trees overfit individual training leaves."*

### Question 7: "What is your unit of prediction and prediction horizon?"
* **Model Answer:**  
  > *"The unit of prediction is the municipal ward centroid (representing approximately 1,500 to 5,000 households). The prediction horizon is a 30-day forward-looking operational window. This horizon was chosen specifically to align with municipal technical budgeting cycles—giving engineers 2 to 4 weeks to schedule preventative repairs or pre-position emergency water tankers before failure occurs."*

### Question 8: "Did you tune your hyperparameters on the test set?"
* **Model Answer:**  
  > *"No. The held-out test set of 700 wards was strictly quarantined. Hyperparameter optimization was conducted exclusively within 5-fold Stratified Cross-Validation on the 2,800 training samples using RandomizedSearchCV across 20 configurations. Once the best parameter combination was identified, the champion pipeline was locked, fitted once on the entire training set, and evaluated exactly once on the test set."*

### Question 9: "How do you handle invalid inputs in your deployed application?"
* **Model Answer:**  
  > *"Our Gradio deployment features a strict input validation layer. If a municipal clerk inputs negative population density, negative burst counts, or percentages outside 0-100%, the application intercepts the request before passing it to Scikit-Learn. It returns a user-friendly red alert explaining the exact invalid fields rather than throwing an unhandled backend exception."*

### Question 10: "What is the economic cost of a False Positive vs a False Negative in your cost matrix?"
* **Model Answer:**  
  > *"In municipal service delivery, the cost matrix is heavily asymmetric. A False Positive (flagging a stable ward as critical) results in a technical team conducting an unneeded inspection—costing approximately R5,000 in technician travel. A False Negative (missing an impending pipe blowout or transformer overload) leads to flooded roads, water contamination, prolonged blackouts, and violent service protests—costing upwards of R500,000 in emergency repairs and community disruption. Therefore, our optimization prioritizes recall on Tier 2."*

### Question 11: "How did you ensure reproducible training?"
* **Model Answer:**  
  > *"All stochastic procedures—including dataset splitting, cross-validation partitioning, XGBoost tree subsampling, and PyTorch weight initialization—are pinned with a fixed master seed (`random_state=42`). Running `python run_pipeline.py` reproduces all 10 figures and tabular metrics deterministically in under 2 minutes."*

### Question 12: "What is your recommendation for municipal implementation?"
* **Model Answer:**  
  > *"We recommend a phased rollout through SALGA. Phase 1 integrates the model into municipal dispatch centers as an advisory risk dashboard. Phase 2 introduces IoT acoustic pipe sensors in high-risk zones identified by the model. Phase 3 connects the output to municipal asset management systems (SDBIP) for automated preventive work-order generation."*
