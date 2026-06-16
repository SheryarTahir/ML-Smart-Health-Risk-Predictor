# Datasets

Download each CSV from Kaggle and place it in this folder with the exact
filename below, then run `python ml/training.py`.

| Disease   | Filename        | Source |
|-----------|-----------------|--------|
| Heart     | `heart.csv`     | https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset |
| Diabetes  | `diabetes.csv`  | https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database |
| Obesity   | `obesity.csv`   | https://www.kaggle.com/datasets/fatemehmehrparvar/obesity-levels |

## Expected target columns
- heart.csv     → `target`     (0 = no disease, 1 = disease)
- diabetes.csv  → `Outcome`    (0 = non-diabetic, 1 = diabetic)
- obesity.csv   → `NObeyesdad` (7-class obesity level — label-encoded automatically)

## Preprocessing performed automatically
1. Drop duplicate rows
2. Median-fill numeric NaNs, mode-fill categorical NaNs
3. Label-encode categorical features and the target if it's textual
4. Stratified 80/20 train-test split
5. `StandardScaler` fit on train and applied to test
