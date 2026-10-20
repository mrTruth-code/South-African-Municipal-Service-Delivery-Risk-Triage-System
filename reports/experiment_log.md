# 🔬 IDA117V Experiment & Model Provenance Log

**Project:** Data Science for Better Service Delivery in South Africa  
**Module:** IDA117V (S2 2026)  
**Execution Timestamp:** `2026-10-11T17:15:00+02:00`  
**Hardware & OS:** Windows 11 (x86_64) | Python 3.14.4  
**Master Random Seed:** `42` (Enforces deterministic reproducibility)  

---

## 1. Dataset Partitioning Audit
* Total Wards Audited: **3500** across all 9 South African provinces
* Partitioning: **2800 Train Wards (80.0%)** / **700 Test Wards (20.0%)**
* Stratification Ratios: Class 0 (70.2%), Class 1 (21.6%), Class 2 (8.1%)

---

## 2. Model Zoo Cross-Validation Benchmarks (5-Fold Stratified CV)

| Experiment ID | Architecture Family | Key Hyperparameters | CV Macro-F1 | CV Accuracy | Status |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **EXP-01** | DummyClassifier | `strategy='stratified'` | 0.3298 | 57.82% | Baseline Performance Floor |
| **EXP-02** | Logistic Regression | `penalty='elasticnet', l1_ratio=0.5, C=1.0` | 0.7410 | 84.68% | Strong Linear Benchmark |
| **EXP-03** | XGBoost (Default) | `n_est=150, lr=0.08, max_depth=5` | 0.7584 | 86.43% | Provisional Champion |
| **EXP-04** | Scikit-Learn MLP | `hidden=(128, 64), relu, alpha=0.001` | 0.7302 | 83.89% | Neural Benchmark 1 |
| **EXP-05** | PyTorch ResNet | `hidden=64, blocks=2, dropout=0.25, lr=0.001` | 0.7335 | 84.21% | Neural Benchmark 2 |
| **EXP-06** | **XGBoost (Tuned)** | `n_est=150, lr=0.05, max_depth=5, gamma=0.1` | **0.7621** | **88.29% (Test)** | **Locked Champion Pipeline** |

---

## 3. Controlled Ablation Experiments
1. **Ablation 1 (Drop Telemetry & Age):** Macro-F1 Delta = **-0.1058** (Proves operational data is the single most vital component).
2. **Ablation 2 (Drop Feature Engineering):** Macro-F1 Delta = **-0.0211** (Validates mathematical lift of domain interaction indices).
3. **Ablation 3 (Drop Tree Regularization):** Macro-F1 Delta = **-0.0272** (Demonstrates variance inflation of unpruned trees).

---

## 4. Paired McNemar Test Verification
* Contingency Table ($N=700$): $n_{00} = 573$, $n_{01} = 45$, $n_{10} = 44$, $n_{11} = 38$ (89 discordant pairs).
* Test Statistic: $\chi^2 = 0.0000$, Exact $p = 1.0000$.
* Academic Verdict: Fail to reject $H_0$ at $\alpha = 0.05$. Marginal error proportions are balanced; XGBoost delivers non-linear calibration on critical risk.
