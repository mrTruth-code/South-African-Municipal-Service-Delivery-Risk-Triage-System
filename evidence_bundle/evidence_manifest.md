# 📦 IDA117V Evidence Bundle Manifest & Provenance Catalog
**Module:** INTRODUCTION TO DATA SCIENCE (IDA117V) | S2 2026  
**Project Title:** Municipal Basic Service-Delivery Outage & Infrastructure Vulnerability Triage System  
**Submission Date:** 20 October 2026  
**Team Members:** MM Masemola (218615937), B Mdluli (222012937), M Mammburu (219952058), ME Maleke (219868499), PA Mavhungu (220527930)  

---

## 🗂️ Catalog of Verified Evidence Files

| File Relative Path | Size | SHA-256 (Truncated) | Verification Status |
| :--- | :---: | :---: | :---: |
| `dataset_card.md` | 3.7 KB | `3462f244743e` | Verified Artifact |
| `experiment_log.json` | 2.1 KB | `72c1024f68f1` | Verified Artifact |
| `experiment_log.md` | 2.3 KB | `f629b605b45a` | Verified Artifact |
| `figures/fig10_ablation_deltas.png` | 105.2 KB | `b417253e692e` | Verified Artifact |
| `figures/fig1_target_distribution.png` | 131.9 KB | `514500dcc81f` | Verified Artifact |
| `figures/fig2_missingness_matrix.png` | 158.3 KB | `f68dfc7d13be` | Verified Artifact |
| `figures/fig3_infra_age_vs_target.png` | 172.7 KB | `c0343d90c25c` | Verified Artifact |
| `figures/fig4_informal_vs_vulnerability.png` | 1023.2 KB | `285d06dcf4d5` | Verified Artifact |
| `figures/fig5_provincial_disparity.png` | 185.7 KB | `9fdbdcdab1d1` | Verified Artifact |
| `figures/fig6_roc_curves.png` | 305.3 KB | `ee479caae9dd` | Verified Artifact |
| `figures/fig7_learning_curves.png` | 312.4 KB | `404f2548c05c` | Verified Artifact |
| `figures/fig8_model_comparison_bar.png` | 181.2 KB | `51a55d8eaf9f` | Verified Artifact |
| `figures/fig9_confusion_matrices.png` | 426.9 KB | `bf298f70f720` | Verified Artifact |
| `mcnemar_predictions/champion_test_predictions.csv` | 27.6 KB | `db9a8cd70557` | Verified Artifact |
| `mcnemar_predictions/mcnemar_table.md` | 1.8 KB | `60f47c3493f0` | Verified Artifact |
| `mcnemar_predictions/mcnemar_test_results.json` | 0.6 KB | `33af24c78778` | Verified Artifact |
| `metric_tables/ablation_study_results.csv` | 0.7 KB | `2632224dd69b` | Verified Artifact |
| `metric_tables/champion_optimisation_comparison.csv` | 0.4 KB | `9b534ffffd53` | Verified Artifact |
| `metric_tables/classification_reports.md` | 2.6 KB | `8f834985160e` | Verified Artifact |
| `metric_tables/data_dictionary.md` | 2.3 KB | `064609b20c51` | Verified Artifact |
| `metric_tables/final_test_metrics.csv` | 0.6 KB | `504811ad7b51` | Verified Artifact |
| `metric_tables/model_validation_comparison.csv` | 0.6 KB | `880e2cebfae7` | Verified Artifact |

---

### Integrity & Reproducibility Statement
All models, test predictions, and evaluation tables within this evidence bundle were produced by executing `run_pipeline.py` with master random seed `42` on the 3,500 ward dataset. The held-out test predictions represent the exact 700 cases evaluated during the paired McNemar test (chi-square = 68.8091, p = 2.14e-6).
