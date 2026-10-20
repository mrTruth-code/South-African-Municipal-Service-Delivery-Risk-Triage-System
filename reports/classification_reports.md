# Model Classification Reports on Held-Out Validation Split

## Naive Baseline
```text
                            precision    recall  f1-score   support

              Low Risk (0)       0.69      0.72      0.71       287
Moderate Vulnerability (1)       0.26      0.20      0.23        99
    Critical Emergency (2)       0.13      0.18      0.15        34

                  accuracy                           0.55       420
                 macro avg       0.36      0.37      0.36       420
              weighted avg       0.55      0.55      0.55       420

```

## Logistic Regression
```text
                            precision    recall  f1-score   support

              Low Risk (0)       0.96      0.90      0.93       287
Moderate Vulnerability (1)       0.69      0.73      0.71        99
    Critical Emergency (2)       0.67      0.88      0.76        34

                  accuracy                           0.86       420
                 macro avg       0.77      0.84      0.80       420
              weighted avg       0.87      0.86      0.86       420

```

## XGBoost
```text
                            precision    recall  f1-score   support

              Low Risk (0)       0.91      0.95      0.93       287
Moderate Vulnerability (1)       0.73      0.67      0.69        99
    Critical Emergency (2)       0.79      0.68      0.73        34

                  accuracy                           0.86       420
                 macro avg       0.81      0.76      0.79       420
              weighted avg       0.86      0.86      0.86       420

```

## Neural MLP
```text
                            precision    recall  f1-score   support

              Low Risk (0)       0.92      0.94      0.93       287
Moderate Vulnerability (1)       0.74      0.70      0.72        99
    Critical Emergency (2)       0.82      0.82      0.82        34

                  accuracy                           0.87       420
                 macro avg       0.83      0.82      0.82       420
              weighted avg       0.87      0.87      0.87       420

```

## PyTorch Tabular ResNet
```text
                            precision    recall  f1-score   support

              Low Risk (0)       0.92      0.94      0.93       287
Moderate Vulnerability (1)       0.69      0.67      0.68        99
    Critical Emergency (2)       0.70      0.68      0.69        34

                  accuracy                           0.85       420
                 macro avg       0.77      0.76      0.77       420
              weighted avg       0.85      0.85      0.85       420

```

