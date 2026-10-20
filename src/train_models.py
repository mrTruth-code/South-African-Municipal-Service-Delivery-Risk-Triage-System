"""
train_models.py
Implements Question 3 & Question 4:
- Naive Baseline: DummyClassifier (stratified)
- Traditional 1: Logistic Regression (balanced)
- Traditional 2: XGBoost Classifier
- Neural 1: Multi-Layer Perceptron (scikit-learn MLPClassifier with Early Stopping)
- Neural 2: PyTorch Tabular ResNet (Deep Tabular Network with Skip Connections & LayerNorm)
- Fair multi-metric evaluation: Accuracy, Macro-F1, Weighted-F1, Precision, Recall, Macro ROC-AUC, PR-AUC
- Overfitting diagnosis: Train-validation generalization gap, learning curves, loss curves
- Saves figures: fig6_roc_curves.png, fig7_learning_curves.png, fig8_model_comparison_bar.png, fig9_confusion_matrices.png
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    roc_auc_score, average_precision_score, classification_report,
    confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import StratifiedKFold, cross_val_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# Import data pipeline
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline import prepare_data_splits, build_preprocessor

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# =========================================================================
# PYTORCH TABULAR RESNET MODEL (NEURAL MODEL 2)
# =========================================================================
class TabularResidualBlock(nn.Module):
    def __init__(self, dim, dropout=0.2):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim),
            nn.LayerNorm(dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(dim, dim),
            nn.LayerNorm(dim)
        )
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(x + self.block(x))

class PyTorchTabularResNet(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_classes=3, dropout=0.2):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        self.res1 = TabularResidualBlock(hidden_dim, dropout)
        self.res2 = TabularResidualBlock(hidden_dim, dropout)
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        x = self.stem(x)
        x = self.res1(x)
        x = self.res2(x)
        return self.head(x)

# PyTorch Scikit-Learn Wrapper for Cross-Validation and Predictions
class PyTorchResNetWrapper:
    def __init__(self, input_dim, hidden_dim=128, num_classes=3, lr=0.003, weight_decay=1e-3, epochs=50, batch_size=64, random_state=42):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.lr = lr
        self.weight_decay = weight_decay
        self.epochs = epochs
        self.batch_size = batch_size
        self.random_state = random_state
        self.model = None
        self.history = {'train_loss': [], 'val_loss': [], 'train_f1': [], 'val_f1': []}

    def fit(self, X_tr, y_tr, X_val=None, y_val=None):
        torch.manual_seed(self.random_state)
        np.random.seed(self.random_state)
        
        self.model = PyTorchTabularResNet(self.input_dim, self.hidden_dim, self.num_classes)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=self.epochs)

        # Handle validation split if not provided
        if X_val is None:
            n_val = int(0.15 * len(X_tr))
            perm = np.random.permutation(len(X_tr))
            val_idx, tr_idx = perm[:n_val], perm[n_val:]
            X_val, y_val = X_tr[val_idx], y_tr[val_idx]
            X_tr, y_tr = X_tr[tr_idx], y_tr[tr_idx]

        train_ds = TensorDataset(torch.tensor(X_tr, dtype=torch.float32), torch.tensor(y_tr, dtype=torch.long))
        val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.long))
        
        train_loader = DataLoader(train_ds, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=self.batch_size, shuffle=False)

        best_val_f1 = -1.0
        best_state = None
        patience = 12
        patience_counter = 0

        self.history = {'train_loss': [], 'val_loss': [], 'train_f1': [], 'val_f1': []}

        for epoch in range(self.epochs):
            self.model.train()
            train_loss = 0.0
            tr_preds, tr_targets = [], []
            for bx, by in train_loader:
                optimizer.zero_grad()
                out = self.model(bx)
                loss = criterion(out, by)
                loss.backward()
                optimizer.step()
                train_loss += loss.item() * len(by)
                tr_preds.extend(out.argmax(dim=1).cpu().numpy())
                tr_targets.extend(by.cpu().numpy())

            scheduler.step()
            train_loss /= len(X_tr)
            train_f1 = f1_score(tr_targets, tr_preds, average='macro')

            # Validation
            self.model.eval()
            val_loss = 0.0
            v_preds, v_targets = [], []
            with torch.no_grad():
                for bx, by in val_loader:
                    out = self.model(bx)
                    loss = criterion(out, by)
                    val_loss += loss.item() * len(by)
                    v_preds.extend(out.argmax(dim=1).cpu().numpy())
                    v_targets.extend(by.cpu().numpy())

            val_loss /= len(X_val)
            val_f1 = f1_score(v_targets, v_preds, average='macro')

            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_f1'].append(train_f1)
            self.history['val_f1'].append(val_f1)

            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                best_state = self.model.state_dict().copy()
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    break

        if best_state is not None:
            self.model.load_state_dict(best_state)
        return self

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            tx = torch.tensor(X, dtype=torch.float32)
            out = self.model(tx)
            return out.argmax(dim=1).cpu().numpy()

    def predict_proba(self, X):
        self.model.eval()
        with torch.no_grad():
            tx = torch.tensor(X, dtype=torch.float32)
            out = self.model(tx)
            probs = torch.softmax(out, dim=1).cpu().numpy()
            return probs


# =========================================================================
# EXPERIMENT EXECUTION & EVALUATION
# =========================================================================
def run_model_experiments():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, 'figures')
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    print("="*70)
    print("STEP 3: PREPARING DATA SPLITS & LEAKAGE-FREE PIPELINE")
    print("="*70)
    X_train_raw, X_test_raw, y_train_series, y_test_series = prepare_data_splits(random_state=42)
    
    preprocessor = build_preprocessor()
    # FIT ONLY ON TRAINING SET
    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)
    
    y_train = y_train_series.values
    y_test = y_test_series.values
    
    input_dim = X_train.shape[1]
    print(f"Preprocessed Feature Matrix: {input_dim} features.")

    # 15% Internal Validation Split from Train for Model Comparison & Overfitting Assessment
    np.random.seed(42)
    n_val = int(0.15 * len(X_train))
    perm = np.random.permutation(len(X_train))
    val_idx, tr_idx = perm[:n_val], perm[n_val:]
    
    X_tr, y_tr = X_train[tr_idx], y_train[tr_idx]
    X_val, y_val = X_train[val_idx], y_train[val_idx]
    print(f"Internal Validation Split: Train={len(X_tr)}, Val={len(X_val)}")

    print("\n" + "="*70)
    print("STEP 3.2: DEFINING MODEL SUITE (1 NAIVE BASELINE + 4 SUBSTANTIVE MODELS)")
    print("="*70)
    
    models = {
        'Naive Baseline': DummyClassifier(strategy='stratified', random_state=42),
        'Logistic Regression': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42, C=1.0),
        'XGBoost': XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.08, subsample=0.8, 
                                 colsample_bytree=0.8, eval_metric='mlogloss', random_state=42),
        'Neural MLP': MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', alpha=0.01,
                                    learning_rate_init=0.003, max_iter=150, early_stopping=True,
                                    validation_fraction=0.15, n_iter_no_change=12, random_state=42),
        'PyTorch Tabular ResNet': PyTorchResNetWrapper(input_dim=input_dim, hidden_dim=128, num_classes=3,
                                                      lr=0.003, weight_decay=1e-3, epochs=60, batch_size=64, random_state=42)
    }

    metrics_records = []
    trained_models = {}
    val_predictions = {}
    val_probabilities = {}
    train_predictions = {}

    print("\n" + "="*70)
    print("STEP 4: TRAINING & FAIR MULTI-METRIC VALIDATION EVALUATION")
    print("="*70)

    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        if name == 'PyTorch Tabular ResNet':
            model.fit(X_tr, y_tr, X_val, y_val)
            y_pred_tr = model.predict(X_tr)
            y_pred_val = model.predict(X_val)
            y_prob_val = model.predict_proba(X_val)
        else:
            model.fit(X_tr, y_tr)
            y_pred_tr = model.predict(X_tr)
            y_pred_val = model.predict(X_val)
            if hasattr(model, "predict_proba"):
                y_prob_val = model.predict_proba(X_val)
            else:
                y_prob_val = np.zeros((len(X_val), 3))

        trained_models[name] = model
        val_predictions[name] = y_pred_val
        val_probabilities[name] = y_prob_val
        train_predictions[name] = y_pred_tr

        # Compute Multi-Metrics
        acc = accuracy_score(y_val, y_pred_val)
        macro_f1 = f1_score(y_val, y_pred_val, average='macro')
        weighted_f1 = f1_score(y_val, y_pred_val, average='weighted')
        precision_macro = precision_score(y_val, y_pred_val, average='macro')
        recall_macro = recall_score(y_val, y_pred_val, average='macro')

        # One-vs-Rest ROC-AUC & PR-AUC
        y_val_bin = label_binarize(y_val, classes=[0, 1, 2])
        try:
            roc_auc = roc_auc_score(y_val_bin, y_prob_val, average='macro', multi_class='ovr')
            pr_auc = average_precision_score(y_val_bin, y_prob_val, average='macro')
        except Exception:
            roc_auc = 0.50
            pr_auc = 0.33

        # Overfitting Gap (Train Macro F1 - Val Macro F1)
        train_macro_f1 = f1_score(y_tr, y_pred_tr, average='macro')
        generalization_gap = train_macro_f1 - macro_f1

        metrics_records.append({
            'Model': name,
            'Val Accuracy': round(acc, 4),
            'Val Macro-F1': round(macro_f1, 4),
            'Val Weighted-F1': round(weighted_f1, 4),
            'Val Macro-Precision': round(precision_macro, 4),
            'Val Macro-Recall': round(recall_macro, 4),
            'Val ROC-AUC (OvR)': round(roc_auc, 4),
            'Val PR-AUC (OvR)': round(pr_auc, 4),
            'Train Macro-F1': round(train_macro_f1, 4),
            'Overfitting Gap': round(generalization_gap, 4)
        })

        print(f"  Accuracy: {acc:.4f} | Macro-F1: {macro_f1:.4f} | ROC-AUC: {roc_auc:.4f} | Overfitting Gap: {generalization_gap:.4f}")

    metrics_df = pd.DataFrame(metrics_records)
    print("\n" + "="*70)
    print("MODEL VALIDATION COMPARISON TABLE:")
    print("="*70)
    print(metrics_df.to_string(index=False))

    # Save metrics to reports
    metrics_df.to_csv(os.path.join(reports_dir, 'model_validation_comparison.csv'), index=False)

    # =========================================================================
    # STEP 4.2: GENERATE COMBINED ROC CURVES (FIGURE 6)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(9, 7))
    colors = {
        'Naive Baseline': 'gray',
        'Logistic Regression': '#3498db',
        'XGBoost': '#27ae60',
        'Neural MLP': '#9b59b6',
        'PyTorch Tabular ResNet': '#e67e22'
    }

    y_val_bin = label_binarize(y_val, classes=[0, 1, 2])
    for name in models.keys():
        prob = val_probabilities[name]
        # Compute macro-average ROC curve
        fpr_dict = dict()
        tpr_dict = dict()
        roc_auc_dict = dict()
        for i in range(3):
            fpr_dict[i], tpr_dict[i], _ = roc_curve(y_val_bin[:, i], prob[:, i])
            roc_auc_dict[i] = auc(fpr_dict[i], tpr_dict[i])

        all_fpr = np.unique(np.concatenate([fpr_dict[i] for i in range(3)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(3):
            mean_tpr += np.interp(all_fpr, fpr_dict[i], tpr_dict[i])
        mean_tpr /= 3.0
        macro_auc = auc(all_fpr, mean_tpr)

        linestyle = '--' if name == 'Naive Baseline' else '-'
        ax.plot(all_fpr, mean_tpr, label=f'{name} (Macro AUC = {macro_auc:.3f})',
                color=colors[name], linewidth=2.0, linestyle=linestyle)

    ax.plot([0, 1], [0, 1], 'k:', label='Chance Level (AUC = 0.500)')
    ax.set_title('Figure 6: One-vs-Rest Macro ROC Curves on Held-Out Validation Split\n(Comparing Naive Baseline, Traditional and Neural Architectures)', pad=15)
    ax.set_xlabel('False Positive Rate (1 - Specificity)')
    ax.set_ylabel('True Positive Rate (Sensitivity / Recall)')
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    fig6_path = os.path.join(fig_dir, 'fig6_roc_curves.png')
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"\n[SAVED] {fig6_path}")

    # =========================================================================
    # STEP 4.4: OVERFITTING LEARNING & LOSS CURVES (FIGURE 7)
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # 7A: PyTorch ResNet Loss Curves
    resnet_hist = trained_models['PyTorch Tabular ResNet'].history
    epochs_range = range(1, len(resnet_hist['train_loss']) + 1)
    axes[0].plot(epochs_range, resnet_hist['train_loss'], label='Training Cross-Entropy Loss', color='#2980b9', linewidth=2)
    axes[0].plot(epochs_range, resnet_hist['val_loss'], label='Validation Cross-Entropy Loss', color='#e74c3c', linewidth=2, linestyle='--')
    axes[0].set_title('Figure 7A: PyTorch Tabular ResNet Training vs Validation Loss\n(Early Stopping & Cosine Annealing Regularization)', pad=12)
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Cross-Entropy Loss')
    axes[0].legend()

    # 7B: PyTorch ResNet Macro-F1 Generalization Curves
    axes[1].plot(epochs_range, resnet_hist['train_f1'], label='Training Macro-F1', color='#27ae60', linewidth=2)
    axes[1].plot(epochs_range, resnet_hist['val_f1'], label='Validation Macro-F1', color='#d35400', linewidth=2, linestyle='--')
    axes[1].set_title('Figure 7B: PyTorch Tabular ResNet Macro-F1 Generalization\n(Quantified Overfitting Gap Control)', pad=12)
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Macro-F1 Score')
    axes[1].legend()

    plt.tight_layout()
    fig7_path = os.path.join(fig_dir, 'fig7_learning_curves.png')
    plt.savefig(fig7_path, dpi=300)
    plt.close()
    print(f"[SAVED] {fig7_path}")

    # =========================================================================
    # STEP 4.3: MODEL COMPARISON BAR CHART (FIGURE 8)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 5.5))
    df_plot_metrics = metrics_df[['Model', 'Val Macro-F1', 'Val ROC-AUC (OvR)', 'Val Accuracy']].melt(
        id_vars='Model', var_name='Metric', value_name='Score'
    )
    sns.barplot(data=df_plot_metrics, x='Model', y='Score', hue='Metric', 
                palette=['#2980b9', '#27ae60', '#f39c12'], ax=ax, edgecolor='black', linewidth=0.8)
    ax.set_title('Figure 8: Comparative Validation Performance Across Naive Baseline and Substantive Models', pad=15)
    ax.set_ylabel('Metric Score (0.0 - 1.0)')
    ax.set_ylim(0, 1.08)
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.3f}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8, rotation=0, xytext=(0, 3),
                        textcoords='offset points', fontweight='bold')
    plt.xticks(rotation=20, ha='right')
    ax.legend(title='Metric', loc='lower right')
    plt.tight_layout()
    fig8_path = os.path.join(fig_dir, 'fig8_model_comparison_bar.png')
    plt.savefig(fig8_path, dpi=300)
    plt.close()
    print(f"[SAVED] {fig8_path}")

    # =========================================================================
    # STEP 4.2: CONFUSION MATRICES (FIGURE 9)
    # =========================================================================
    fig, axes = plt.subplots(1, 5, figsize=(22, 4.5))
    target_names = ['Low', 'Moderate', 'Critical']
    for idx, (m_name, y_p) in enumerate(val_predictions.items()):
        cm = confusion_matrix(y_val, y_p)
        cm_pct = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        annot_labels = np.array([[f"{cm[i,j]}\n({cm_pct[i,j]:.1f}%)" 
                                  for j in range(3)] for i in range(3)])
        sns.heatmap(cm, annot=annot_labels, fmt='', cmap='Blues', cbar=False, ax=axes[idx],
                    xticklabels=target_names, yticklabels=target_names)
        axes[idx].set_title(f'{m_name}', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Predicted Risk Tier')
        if idx == 0:
            axes[idx].set_ylabel('Actual Risk Tier')
        else:
            axes[idx].set_ylabel('')

    plt.suptitle('Figure 9: Confusion Matrices with Class Support and Normalized Percentages on Validation Split', fontsize=14, fontweight='bold', y=1.05)
    plt.tight_layout()
    fig9_path = os.path.join(fig_dir, 'fig9_confusion_matrices.png')
    plt.savefig(fig9_path, dpi=300)
    plt.close()
    print(f"[SAVED] {fig9_path}")

    # Save classification reports text
    rep_text = "# Model Classification Reports on Held-Out Validation Split\n\n"
    for name, pred in val_predictions.items():
        rep = classification_report(y_val, pred, target_names=['Low Risk (0)', 'Moderate Vulnerability (1)', 'Critical Emergency (2)'])
        rep_text += f"## {name}\n```text\n{rep}\n```\n\n"
    with open(os.path.join(reports_dir, 'classification_reports.md'), 'w', encoding='utf-8') as f:
        f.write(rep_text)
    print(f"[SAVED] {os.path.join(reports_dir, 'classification_reports.md')}")

    # Identify provisional champion based on Validation Macro-F1
    substantive_df = metrics_df[metrics_df['Model'] != 'Naive Baseline']
    champion_name = substantive_df.sort_values(by='Val Macro-F1', ascending=False).iloc[0]['Model']
    print("\n" + "="*70)
    print(f"PROVISIONAL CHAMPION SELECTED ON VALIDATION SCORE: {champion_name}")
    print("="*70)

    return champion_name, trained_models, preprocessor, X_train, y_train, X_test, y_test

if __name__ == '__main__':
    run_model_experiments()
