"""
run_pipeline.py
Master execution pipeline for IDA117V S2 2026 Data Science Group Project:
Runs the entire end-to-end reproducible workflow from raw data creation to 
statistical validation and verification:
1. Data generation
2. Audit, data dictionary & 5 EDA visualisations
3. Baseline & 4 substantive models (2 traditional, 2 neural)
4. Multi-metric evaluation, ROC curves & overfitting diagnosis
5. Champion optimization & locked test set evaluation
6. Controlled ablation study & McNemar statistical test
7. Case verification for deployment UI
"""

import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

def main():
    start_time = time.time()
    print("="*80)
    print("IDA117V S2 2026: DATA SCIENCE FOR BETTER SERVICE DELIVERY IN SOUTH AFRICA")
    print("END-TO-END REPRODUCIBLE MACHINE LEARNING PIPELINE EXECUTION")
    print("="*80)

    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    sys.path.append(src_dir)

    # 1. Data Generation
    print("\n>>> [PHASE 1/6] SYNTHESIZING SOUTH AFRICAN SERVICE DELIVERY DATASET...")
    from data_generator import generate_sa_service_delivery_data
    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    raw_path = os.path.join(raw_dir, 'sa_municipal_service_delivery.csv')
    df = generate_sa_service_delivery_data(n_samples=3500, random_seed=42)
    df.to_csv(raw_path, index=False)
    print(f"Dataset successfully created with {len(df)} records at {raw_path}")

    # 2. Audit & EDA
    print("\n>>> [PHASE 2/6] EXECUTING DATA AUDIT & GENERATING 5 PURPOSEFUL VISUALISATIONS...")
    from audit_and_eda import run_data_audit_and_eda
    run_data_audit_and_eda()

    # 3. Model Training & Evaluation
    print("\n>>> [PHASE 3/6] TRAINING NAIVE BASELINE + 4 SUBSTANTIVE MODELS (2 TRADITIONAL + 2 NEURAL)...")
    from train_models import run_model_experiments
    run_model_experiments()

    # 4. Champion Optimisation
    print("\n>>> [PHASE 4/6] OPTIMIZING CHAMPION HYPERPARAMETERS & LOCKED TEST SET EVALUATION...")
    from optimize_champion import run_champion_optimisation
    run_champion_optimisation()

    # 5. Ablation & McNemar Validation
    print("\n>>> [PHASE 5/6] CONDUCTING 3 CONTROLLED ABLATIONS & PAIRED MCNEMAR TEST...")
    from ablation_mcnemar import run_ablation_and_mcnemar
    run_ablation_and_mcnemar()

    # 6. Verification Cases
    print("\n>>> [PHASE 6/6] VERIFYING DEPLOYMENT PREDICTION PIPELINE & TEST CASES...")
    from verify_cases import run_case_demonstrations
    run_case_demonstrations()

    elapsed = time.time() - start_time
    print("\n" + "="*80)
    print(f"[SUCCESS] ALL PIPELINE PHASES COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print("="*80)

if __name__ == '__main__':
    main()
