"""
optimize_champion.py
Implements Question 5:
- Hyperparameter tuning exclusively on Stratified Cross-Validation (NO test set tuning)
- Search space definition and scoring rule (Macro-F1)
- Pre- vs Post-Optimization comparison
- Locked final pipeline evaluation ONCE on held-out test set
- Serializes pipeline to models/champion_pipeline.joblib
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    roc_auc_score, average_precision_score, classification_report,
    confusion_matrix
)
from sklearn.preprocessing import label_binarize
from xgboost import XGBClassifier

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline import prepare_data_splits, build_preprocessor

def run_champion_optimisation():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, 'models')
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print("="*70)
    print("STEP 5.1: CHAMPION HYPERPARAMETER OPTIMISATION PROTOCOL")
    print("="*70)

    # 1. Load Data Splits (Strict 80% Train, 20% Held-Out Test)
    X_train_raw, X_test_raw, y_train, y_test = prepare_data_splits(random_state=42)

    # 2. Build feature preprocessor
    preprocessor = build_preprocessor()
    X_train_trans = preprocessor.fit_transform(X_train_raw)
    X_test_trans = preprocessor.transform(X_test_raw)

    print("\n[CHAMPION] Model Family Selected: XGBoost Gradient Boosted Decision Trees")
    print("  Scoring Rule: Macro-F1 (Balances sensitivity across all 3 vulnerability tiers)")
    print("  Validation Strategy: 5-Fold Stratified Cross-Validation on Training Set")
    print("  Held-out Test Protocol: STRICTLY ISOLATED until final locked model evaluation.")

    # 3. Pre-Optimisation Baseline Evaluation
    baseline_xgb = XGBClassifier(
        n_estimators=100, max_depth=4, learning_rate=0.1, 
        eval_metric='mlogloss', random_state=42
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    cv_pre_scores = []
    for tr_i, val_i in cv.split(X_train_trans, y_train):
        baseline_xgb.fit(X_train_trans[tr_i], y_train.iloc[tr_i])
        p = baseline_xgb.predict(X_train_trans[val_i])
        cv_pre_scores.append(f1_score(y_train.iloc[val_i], p, average='macro'))

    pre_opt_mean_f1 = np.mean(cv_pre_scores)
    pre_opt_std_f1 = np.std(cv_pre_scores)
    print(f"\n[PRE-TUNING] 5-Fold CV Macro-F1: {pre_opt_mean_f1:.4f} (+/- {pre_opt_std_f1:.4f})")

    # 4. Define Search Space
    param_distributions = {
        'n_estimators': [100, 150, 200, 250, 300],
        'max_depth': [3, 4, 5, 6, 7],
        'learning_rate': [0.03, 0.05, 0.08, 0.1, 0.15],
        'subsample': [0.7, 0.8, 0.9, 1.0],
        'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
        'min_child_weight': [1, 3, 5, 7],
        'gamma': [0, 0.1, 0.2, 0.4]
    }

    print("\n[SEARCH SPACE]")
    for k, v in param_distributions.items():
        print(f"  - {k}: {v}")

    # 5. Randomized Search with Cross-Validation
    random_search = RandomizedSearchCV(
        estimator=XGBClassifier(eval_metric='mlogloss', random_state=42),
        param_distributions=param_distributions,
        n_iter=10,
        scoring='f1_macro',
        cv=cv,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )

    print("\n[EXECUTING] RandomizedSearchCV running 10 parameter configurations...")
    random_search.fit(X_train_trans, y_train)

    best_params = random_search.best_params_
    post_opt_mean_f1 = random_search.best_score_

    print("\n" + "="*70)
    print("STEP 5.2: OPTIMISATION RESULTS & HYPERPARAMETER SELECTION")
    print("="*70)
    print(f"Selected Optimal Hyperparameters:")
    for k, v in best_params.items():
        print(f"  * {k}: {v}")
    print(f"\nPre-Optimisation CV Macro-F1:  {pre_opt_mean_f1:.4f}")
    print(f"Post-Optimisation CV Macro-F1: {post_opt_mean_f1:.4f}")
    delta_f1 = post_opt_mean_f1 - pre_opt_mean_f1
    print(f"Validation Performance Delta:  +{delta_f1:.4f} (+{delta_f1/pre_opt_mean_f1*100:.2f}%)")

    # Save Hyperparameter Comparison Table
    comp_df = pd.DataFrame([{
        'Phase': 'Pre-Optimisation Default',
        'CV Macro-F1': round(pre_opt_mean_f1, 4),
        'CV Std-Dev': round(pre_opt_std_f1, 4),
        'Configuration': "n_est=100, depth=4, lr=0.1"
    }, {
        'Phase': 'Post-Optimisation Tuned',
        'CV Macro-F1': round(post_opt_mean_f1, 4),
        'CV Std-Dev': round(np.std(random_search.cv_results_['mean_test_score']), 4),
        'Configuration': str(best_params)
    }])
    comp_df.to_csv(os.path.join(reports_dir, 'champion_optimisation_comparison.csv'), index=False)

    # 6. Fit Final Champion on ENTIRE Training Set
    best_xgb = XGBClassifier(**best_params, eval_metric='mlogloss', random_state=42)
    best_xgb.fit(X_train_trans, y_train)

    # Build Complete End-to-End Pipeline (Raw Data -> Preprocessor -> Champion Model)
    full_locked_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', best_xgb)
    ])

    # Save Pipeline Artifact
    pipeline_path = os.path.join(models_dir, 'champion_pipeline.joblib')
    joblib.dump(full_locked_pipeline, pipeline_path)
    print(f"\n[SAVED] End-to-End Champion Pipeline locked and saved to: {pipeline_path}")

    # =========================================================================
    # STEP 5.3: FINAL HELD-OUT TEST SET EVALUATION (EXECUTED EXACTLY ONCE)
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 5.3: FINAL LOCKED HELD-OUT TEST SET EVALUATION (ONCE-ONLY)")
    print("="*70)

    test_preds = full_locked_pipeline.predict(X_test_raw)
    test_probs = full_locked_pipeline.predict_proba(X_test_raw)

    test_acc = accuracy_score(y_test, test_preds)
    test_macro_f1 = f1_score(y_test, test_preds, average='macro')
    test_weighted_f1 = f1_score(y_test, test_preds, average='weighted')
    test_precision = precision_score(y_test, test_preds, average='macro')
    test_recall = recall_score(y_test, test_preds, average='macro')

    y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
    test_roc_auc = roc_auc_score(y_test_bin, test_probs, average='macro', multi_class='ovr')
    test_pr_auc = average_precision_score(y_test_bin, test_probs, average='macro')

    print(f"Held-Out Test Results:")
    print(f"  Test Accuracy:        {test_acc:.4f}")
    print(f"  Test Macro-F1:        {test_macro_f1:.4f}")
    print(f"  Test Weighted-F1:     {test_weighted_f1:.4f}")
    print(f"  Test Macro-Precision: {test_precision:.4f}")
    print(f"  Test Macro-Recall:    {test_recall:.4f}")
    print(f"  Test ROC-AUC (OvR):   {test_roc_auc:.4f}")
    print(f"  Test PR-AUC (OvR):    {test_pr_auc:.4f}")

    print("\nFinal Test Classification Report:")
    test_rep = classification_report(y_test, test_preds, target_names=['Low Risk', 'Moderate Vulnerability', 'Critical Risk'])
    print(test_rep)

    # Save Test Results & Predictions for McNemar Test
    test_results_df = pd.DataFrame([{
        'Metric': 'Accuracy', 'Score': round(test_acc, 4)
    }, {
        'Metric': 'Macro-F1', 'Score': round(test_macro_f1, 4)
    }, {
        'Metric': 'Weighted-F1', 'Score': round(test_weighted_f1, 4)
    }, {
        'Metric': 'Macro-Precision', 'Score': round(test_precision, 4)
    }, {
        'Metric': 'Macro-Recall', 'Score': round(test_recall, 4)
    }, {
        'Metric': 'Macro ROC-AUC', 'Score': round(test_roc_auc, 4)
    }, {
        'Metric': 'Macro PR-AUC', 'Score': round(test_pr_auc, 4)
    }])
    test_results_df.to_csv(os.path.join(reports_dir, 'final_test_metrics.csv'), index=False)

    predictions_df = pd.DataFrame({
        'y_true': y_test.values,
        'y_pred_champion': test_preds,
        'prob_class_0': test_probs[:, 0],
        'prob_class_1': test_probs[:, 1],
        'prob_class_2': test_probs[:, 2]
    })
    predictions_df.to_csv(os.path.join(reports_dir, 'champion_test_predictions.csv'), index=False)
    print(f"[SAVED] Test predictions saved to {os.path.join(reports_dir, 'champion_test_predictions.csv')}")

    return full_locked_pipeline, best_params

if __name__ == '__main__':
    run_champion_optimisation()
