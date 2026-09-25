import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


print("MODULE 2 - MACHINE LEARNING")

# LOAD CLEANED DATASET

df = pd.read_csv("titanic.csv")

print("\nDataset loaded from titanic.csv")
print(f"Dataset shape: {df.shape}")

# TASK 7: DEFINE FEATURES AND TARGET

target = "survived"

features = [
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "fare",
    "embarked"
]

X = df[features]
y = df[target]

print("\nFeatures:")
print(features)

print(f"\nTarget: {target}")

# CHECK CLASS BALANCE

print("CLASS BALANCE")

class_counts = y.value_counts().sort_index()
class_percentages = y.value_counts(normalize=True).sort_index() * 100

print("\nClass counts:")
print(class_counts)

print("\nClass percentages:")

for class_value in class_percentages.index:
    print(
        f"Class {class_value}: "
        f"{class_percentages[class_value]:.2f}%"
    )

# TASK 7: STRATIFIED TRAIN/TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("TRAIN / TEST SPLIT")

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

print("\nTraining class distribution:")
print(
    y_train.value_counts(normalize=True)
    .sort_index() * 100
)

print("\nTesting class distribution:")
print(
    y_test.value_counts(normalize=True)
    .sort_index() * 100
)

print("\nStratification keeps the class proportions approximately")
print("consistent between the training and testing datasets.")

# TASK 8: PREPROCESSING

print("TASK 8 - PREPROCESSING PIPELINE")

# Numerical features
numeric_features = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

# Categorical features
categorical_features = [
    "sex",
    "embarked"
]

# Numerical preprocessing

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

# Categorical preprocessing

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)

# Combine preprocessing

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)

# FIT PREPROCESSING ONLY ON TRAINING DATA

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)

print("\nPreprocessing completed.")

print(f"Original training shape: {X_train.shape}")
print(f"Processed training shape: {X_train_processed.shape}")

print(f"Original testing shape: {X_test.shape}")
print(f"Processed testing shape: {X_test_processed.shape}")

print("\nNumerical features:")
print(numeric_features)

print("\nCategorical features:")
print(categorical_features)

print("\nPreprocessor was fitted only on the training dataset.")
print("The test dataset was transformed using the fitted preprocessor.")
print("This prevents data leakage.")

# =========================================================
# TASK 9: CLASSIFICATION MODELS
# =========================================================

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import os

print("TASK 9 - CLASSIFICATION MODELS")

# Create model directory for later model artifacts
os.makedirs("model", exist_ok=True)

# LOGISTIC REGRESSION

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(X_train_processed, y_train)

logistic_predictions = logistic_model.predict(X_test_processed)

print("\nLogistic Regression trained successfully.")

# DECISION TREE

decision_tree_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=5
)

decision_tree_model.fit(X_train_processed, y_train)

decision_tree_predictions = decision_tree_model.predict(
    X_test_processed
)

print("Decision Tree trained successfully.")

# RANDOM FOREST

random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    oob_score=True
)

random_forest_model.fit(X_train_processed, y_train)

random_forest_predictions = random_forest_model.predict(
    X_test_processed
)

print("Random Forest trained successfully.")

# DECISION TREE VISUALIZATION

print("\nCreating Decision Tree visualization...")

# Get feature names after preprocessing
feature_names = preprocessor.get_feature_names_out()

plt.figure(figsize=(20, 10))

plot_tree(
    decision_tree_model,
    feature_names=feature_names,
    class_names=["Did not survive", "Survived"],
    filled=True,
    rounded=True,
    fontsize=8
)

plt.title("Decision Tree - Titanic Survival")
plt.tight_layout()

plt.savefig(
    "charts/decision_tree.png",
    dpi=150
)

plt.close()

print("Decision Tree visualization saved:")
print("charts/decision_tree.png")

# MODEL SUMMARY

print("MODEL TRAINING SUMMARY")

print("Logistic Regression: trained")
print("Decision Tree: trained")
print("Random Forest: trained")

print("\nAll three classification models have been trained successfully.")

# TASK 10: MODEL EVALUATION

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc
)

print("TASK 10 - MODEL EVALUATION")

# STORE MODELS AND PREDICTIONS

models = {
    "Logistic Regression": (
        logistic_model,
        logistic_predictions
    ),
    "Decision Tree": (
        decision_tree_model,
        decision_tree_predictions
    ),
    "Random Forest": (
        random_forest_model,
        random_forest_predictions
    )
}

results = []

# EVALUATE EACH MODEL

for model_name, (model, predictions) in models.items():

    # Probability predictions for ROC/AUC
    probabilities = model.predict_proba(
        X_test_processed
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "AUC": roc_auc
    })

    # PRINT METRICS

    print(model_name)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC/AUC  : {roc_auc:.4f}")

    # CONFUSION MATRIX

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print("\nConfusion Matrix:")
    print(cm)

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Did not survive",
            "Survived"
        ]
    )

    display.plot()

    plt.title(
        f"{model_name} - Confusion Matrix"
    )

    plt.tight_layout()

    safe_name = model_name.lower().replace(" ", "_")

    plt.savefig(
        f"charts/{safe_name}_confusion_matrix.png",
        dpi=150
    )

    plt.close()

# ROC CURVES

plt.figure(figsize=(8, 6))

for model_name, (model, predictions) in models.items():

    probabilities = model.predict_proba(
        X_test_processed
    )[:, 1]

    false_positive_rate, true_positive_rate, _ = roc_curve(
        y_test,
        probabilities
    )

    roc_auc_value = auc(
        false_positive_rate,
        true_positive_rate
    )

    plt.plot(
        false_positive_rate,
        true_positive_rate,
        label=f"{model_name} (AUC = {roc_auc_value:.3f})"
    )

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random classifier"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves - Titanic Classification Models")
plt.legend()
plt.tight_layout()

plt.savefig(
    "charts/roc_curves.png",
    dpi=150
)

plt.close()

print("\nROC curve saved:")
print("charts/roc_curves.png")

# COMPARISON TABLE

comparison_df = pd.DataFrame(results)

print("MODEL COMPARISON TABLE")

print(
    comparison_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1": "{:.4f}".format,
            "AUC": "{:.4f}".format
        }
    )
)

# Save comparison table
comparison_df.to_csv(
    "classification_comparison.csv",
    index=False
)

print("\nComparison table saved:")
print("classification_comparison.csv")

# TASK 11 - CLASS IMBALANCE

from imblearn.over_sampling import SMOTE

print("TASK 11 - CLASS IMBALANCE")

# 1. SHOW ORIGINAL CLASS BALANCE

print("\nOriginal training class distribution:")
print(y_train.value_counts())

print("\nOriginal training class percentages:")
print((y_train.value_counts(normalize=True) * 100).round(2))


# 2. BASELINE LOGISTIC REGRESSION

baseline_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

baseline_model.fit(X_train_processed, y_train)

baseline_predictions = baseline_model.predict(X_test_processed)

baseline_precision = precision_score(
    y_test,
    baseline_predictions
)

baseline_recall = recall_score(
    y_test,
    baseline_predictions
)

baseline_f1 = f1_score(
    y_test,
    baseline_predictions
)

print("\nBASELINE LOGISTIC REGRESSION")
print(f"Precision: {baseline_precision:.4f}")
print(f"Recall   : {baseline_recall:.4f}")
print(f"F1 Score : {baseline_f1:.4f}")


# 3. CLASS WEIGHT = BALANCED

balanced_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

balanced_model.fit(X_train_processed, y_train)

balanced_predictions = balanced_model.predict(X_test_processed)

balanced_precision = precision_score(
    y_test,
    balanced_predictions
)

balanced_recall = recall_score(
    y_test,
    balanced_predictions
)

balanced_f1 = f1_score(
    y_test,
    balanced_predictions
)

print("\nLOGISTIC REGRESSION - CLASS WEIGHT BALANCED")
print(f"Precision: {balanced_precision:.4f}")
print(f"Recall   : {balanced_recall:.4f}")
print(f"F1 Score : {balanced_f1:.4f}")

# 4. SMOTE - TRAINING DATA ONLY

smote = SMOTE(
    random_state=42
)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train_processed,
    y_train
)

print("\nClass distribution after SMOTE:")
print(y_train_smote.value_counts())

print("\nClass percentages after SMOTE:")
print((y_train_smote.value_counts(normalize=True) * 100).round(2))


# Train Logistic Regression on SMOTE data
smote_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

smote_model.fit(
    X_train_smote,
    y_train_smote
)

smote_predictions = smote_model.predict(X_test_processed)

smote_precision = precision_score(
    y_test,
    smote_predictions
)

smote_recall = recall_score(
    y_test,
    smote_predictions
)

smote_f1 = f1_score(
    y_test,
    smote_predictions
)

print("\nLOGISTIC REGRESSION - SMOTE")
print(f"Precision: {smote_precision:.4f}")
print(f"Recall   : {smote_recall:.4f}")
print(f"F1 Score : {smote_f1:.4f}")


# 5. COMPARISON TABLE

imbalance_comparison = pd.DataFrame({
    "Method": [
        "Baseline",
        "Class Weight Balanced",
        "SMOTE"
    ],
    "Precision": [
        baseline_precision,
        balanced_precision,
        smote_precision
    ],
    "Recall": [
        baseline_recall,
        balanced_recall,
        smote_recall
    ],
    "F1": [
        baseline_f1,
        balanced_f1,
        smote_f1
    ]
})

print("\nCLASS IMBALANCE COMPARISON")
print(
    imbalance_comparison.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

imbalance_comparison.to_csv(
    "imbalance_comparison.csv",
    index=False
)

print("\nComparison saved:")
print("imbalance_comparison.csv")


# 6. SHORT CONCLUSION

print("\nTASK 11 CONCLUSION")

print(
    "Class imbalance was handled using class_weight='balanced' "
    "and SMOTE."
)

print(
    "SMOTE was applied only to the training data, while the "
    "original test data was kept unchanged."
)

print(
    "The three approaches can be compared using precision, "
    "recall, and F1 score to understand the effect of imbalance handling."
)

# TASK 12 - RANDOM FOREST GRID SEARCH

from sklearn.model_selection import GridSearchCV

print("TASK 12 - RANDOM FOREST GRID SEARCH")

# 1. RANDOM FOREST WITH OOB ENABLED

rf_for_grid = RandomForestClassifier(
    random_state=42,
    oob_score=True,
    bootstrap=True,
    n_jobs=-1
)

# 2. PARAMETER GRID

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 5, 10],
    "max_features": ["sqrt", "log2"]
}

print("\nParameter grid:")
print(param_grid)


# 3. GRID SEARCH

grid_search = GridSearchCV(
    estimator=rf_for_grid,
    param_grid=param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)

print("\nRunning GridSearchCV...")

grid_search.fit(
    X_train_processed,
    y_train
)

print("GridSearchCV completed.")


# 4. BEST PARAMETERS

best_rf = grid_search.best_estimator_

print("\nBEST RANDOM FOREST PARAMETERS")
print(grid_search.best_params_)

print("\nBest cross-validation F1 score:")
print(f"{grid_search.best_score_:.4f}")


# 5. OOB SCORE

print("\nRANDOM FOREST OOB SCORE")
print(f"{best_rf.oob_score_:.4f}")


# 6. TEST SET PERFORMANCE

best_rf_predictions = best_rf.predict(X_test_processed)

best_rf_precision = precision_score(
    y_test,
    best_rf_predictions
)

best_rf_recall = recall_score(
    y_test,
    best_rf_predictions
)

best_rf_f1 = f1_score(
    y_test,
    best_rf_predictions
)

best_rf_accuracy = accuracy_score(
    y_test,
    best_rf_predictions
)

print("\nTUNED RANDOM FOREST TEST PERFORMANCE")
print(f"Accuracy : {best_rf_accuracy:.4f}")
print(f"Precision: {best_rf_precision:.4f}")
print(f"Recall   : {best_rf_recall:.4f}")
print(f"F1 Score : {best_rf_f1:.4f}")


# 7. SAVE GRID SEARCH RESULTS

grid_results = pd.DataFrame(
    grid_search.cv_results_
)

grid_results[
    [
        "param_n_estimators",
        "param_max_depth",
        "param_max_features",
        "mean_test_score",
        "rank_test_score"
    ]
].sort_values(
    "rank_test_score"
).to_csv(
    "random_forest_grid_search.csv",
    index=False
)

print("\nGrid search results saved:")
print("random_forest_grid_search.csv")


# TASK 12 CONCLUSION

print("\nTASK 12 CONCLUSION")

print(
    "GridSearchCV was used to tune n_estimators, max_depth, "
    "and max_features for the Random Forest model."
)

print(
    "The best parameter combination and out-of-bag score "
    "were recorded for the tuned Random Forest."
)

# TASK 13 - MULTIVARIATE LINEAR REGRESSION

print("TASK 13 - MULTIVARIATE LINEAR REGRESSION")

# 1. DEFINE REGRESSION FEATURES AND TARGET

regression_features = [
    "survived",
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "embarked"
]

regression_target = "fare"

X_reg = df[regression_features]
y_reg = df[regression_target]

print("\nRegression features:")
print(regression_features)

print("\nRegression target:")
print(regression_target)


# 2. TRAIN / TEST SPLIT

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg,
    y_reg,
    test_size=0.20,
    random_state=42
)

print("\nRegression training samples:", len(X_reg_train))
print("Regression testing samples:", len(X_reg_test))


# 3. REGRESSION PREPROCESSING

reg_numeric_features = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch"
]

reg_categorical_features = [
    "sex",
    "embarked"
]

reg_numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

reg_categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    ))
])

reg_preprocessor = ColumnTransformer([
    (
        "numeric",
        reg_numeric_pipeline,
        reg_numeric_features
    ),
    (
        "categorical",
        reg_categorical_pipeline,
        reg_categorical_features
    )
])


# 4. FIT PREPROCESSOR ONLY ON TRAINING DATA

X_reg_train_processed = reg_preprocessor.fit_transform(
    X_reg_train
)

X_reg_test_processed = reg_preprocessor.transform(
    X_reg_test
)

print("\nRegression preprocessing completed.")
print(
    "Processed training shape:",
    X_reg_train_processed.shape
)
print(
    "Processed testing shape:",
    X_reg_test_processed.shape
)

print(
    "Regression preprocessor was fitted only on training data."
)


# 5. TRAIN LINEAR REGRESSION

linear_regression_model = LinearRegression()

linear_regression_model.fit(
    X_reg_train_processed,
    y_reg_train
)

print("\nLinear Regression model trained successfully.")


# 6. PREDICT TEST DATA

y_reg_pred = linear_regression_model.predict(
    X_reg_test_processed
)

# 7. CALCULATE METRICS

reg_mae = mean_absolute_error(
    y_reg_test,
    y_reg_pred
)

reg_rmse = np.sqrt(
    mean_squared_error(
        y_reg_test,
        y_reg_pred
    )
)

reg_r2 = r2_score(
    y_reg_test,
    y_reg_pred
)


# Adjusted R²
n = len(y_reg_test)
p = X_reg_test_processed.shape[1]

reg_adjusted_r2 = (
    1
    - ((1 - reg_r2) * (n - 1))
    / (n - p - 1)
)


# 8. PRINT REGRESSION METRICS

print("\nREGRESSION PERFORMANCE")

print(f"MAE         : {reg_mae:.4f}")
print(f"RMSE        : {reg_rmse:.4f}")
print(f"R²          : {reg_r2:.4f}")
print(f"Adjusted R² : {reg_adjusted_r2:.4f}")

print("\nNumber of test samples:", n)
print("Number of predictors after encoding:", p)


# 9. RESIDUALS

residuals = y_reg_test - y_reg_pred

# 10. RESIDUAL PLOT

plt.figure(figsize=(8, 6))

plt.scatter(
    y_reg_pred,
    residuals,
    alpha=0.6
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel("Predicted Fare")
plt.ylabel("Residuals")
plt.title("Linear Regression Residual Plot")

plt.tight_layout()

plt.savefig(
    "charts/regression_residuals.png",
    dpi=300
)

plt.close()

print("\nResidual plot saved:")
print("charts/regression_residuals.png")


# 11. SIMPLE HETEROSCEDASTICITY CHECK

residual_data = pd.DataFrame({
    "predicted": y_reg_pred,
    "residual": residuals
})

residual_data["prediction_group"] = pd.qcut(
    residual_data["predicted"],
    q=4,
    duplicates="drop"
)

residual_spread = (
    residual_data
    .groupby("prediction_group", observed=True)["residual"]
    .std()
)

print("\nResidual standard deviation by predicted-fare group:")
print(residual_spread)


spread_ratio = (
    residual_spread.max() /
    residual_spread.min()
)

print(
    f"\nResidual spread ratio: {spread_ratio:.2f}"
)

if spread_ratio > 2:
    heteroscedasticity_conclusion = (
        "The residual spread changes substantially across "
        "predicted fare values, suggesting possible heteroscedasticity."
    )
else:
    heteroscedasticity_conclusion = (
        "The residual spread does not change substantially "
        "across predicted fare values, so strong heteroscedasticity "
        "is not evident from this check."
    )

print("\nHETEROSCEDASTICITY CONCLUSION")
print(heteroscedasticity_conclusion)


# 12. SAVE REGRESSION METRICS

regression_metrics = pd.DataFrame({
    "Metric": [
        "MAE",
        "RMSE",
        "R2",
        "Adjusted R2"
    ],
    "Value": [
        reg_mae,
        reg_rmse,
        reg_r2,
        reg_adjusted_r2
    ]
})

regression_metrics.to_csv(
    "regression_metrics.csv",
    index=False
)

print("\nRegression metrics saved:")
print("regression_metrics.csv")


# TASK 13 CONCLUSION

print("\nTASK 13 CONCLUSION")

print(
    "A multivariate Linear Regression model was trained "
    "to predict fare using the other available features."
)

print(
    "MAE, RMSE, R², and Adjusted R² were calculated on "
    "the held-out test set."
)

print(
    "A residual plot was created to visually inspect "
    "the regression errors."
)

print(heteroscedasticity_conclusion)

# TASK 14 - FINAL MODEL COMPARISON

print("TASK 14 - FINAL MODEL COMPARISON")

# 1. CLASSIFICATION FINAL TABLE

classification_final = pd.read_csv(
    "classification_comparison.csv"
)

print("\nCLASSIFICATION MODELS")
print(
    classification_final.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# 2. REGRESSION FINAL TABLE

regression_final = pd.DataFrame({
    "Model": ["Linear Regression"],
    "MAE": [reg_mae],
    "RMSE": [reg_rmse],
    "R2": [reg_r2],
    "Adjusted_R2": [reg_adjusted_r2]
})

print("\nREGRESSION MODEL")
print(
    regression_final.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# 3. SAVE FINAL COMPARISON TABLES

classification_final.to_csv(
    "final_classification_comparison.csv",
    index=False
)

regression_final.to_csv(
    "final_regression_comparison.csv",
    index=False
)

print("\nFinal comparison tables saved:")
print("final_classification_comparison.csv")
print("final_regression_comparison.csv")


# 4. IDENTIFY CLASSIFIER BASED ON F1

recommended_classifier_row = classification_final.loc[
    classification_final["F1"].idxmax()
]

recommended_classifier = recommended_classifier_row["Model"]

recommended_accuracy = recommended_classifier_row["Accuracy"]
recommended_precision = recommended_classifier_row["Precision"]
recommended_recall = recommended_classifier_row["Recall"]
recommended_f1 = recommended_classifier_row["F1"]
recommended_auc = recommended_classifier_row["AUC"]


# 5. FINAL CLASSIFIER RECOMMENDATION

print("\nFINAL CLASSIFIER RECOMMENDATION")

print(
    f"Based on the evaluation metrics, {recommended_classifier} "
    f"is the classifier selected for the final pipeline."
)

print(
    f"It achieved an accuracy of {recommended_accuracy:.4f}, "
    f"precision of {recommended_precision:.4f}, "
    f"recall of {recommended_recall:.4f}, "
    f"and F1 score of {recommended_f1:.4f}."
)

print(
    f"Its ROC/AUC score was {recommended_auc:.4f}, "
    f"which indicates its ability to distinguish between the "
    f"two survival classes."
)

print(
    "The final selection is based on the observed test-set "
    "metrics, with F1 used as the primary comparison metric."
)

# TASK 15 - SAVE COMPLETE FITTED PIPELINE

import joblib

print("TASK 15 - SAVE COMPLETE FITTED PIPELINE")


# 1. CREATE COMPLETE PIPELINE

final_pipeline = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "classifier",
        random_forest_model
    )
])


# 2. FIT COMPLETE PIPELINE ON RAW TRAINING DATA

final_pipeline.fit(
    X_train,
    y_train
)

print("\nComplete preprocessing + classifier pipeline fitted.")


# 3. CREATE MODEL DIRECTORY

os.makedirs(
    "model",
    exist_ok=True
)


# 4. SAVE PIPELINE

pipeline_path = "model/titanic_survival_pipeline.joblib"

joblib.dump(
    final_pipeline,
    pipeline_path
)

print("\nPipeline saved:")
print(pipeline_path)


# 5. RELOAD PIPELINE

loaded_pipeline = joblib.load(
    pipeline_path
)

print("\nPipeline successfully reloaded.")


# 6. RAW INPUT EXAMPLE

raw_input = pd.DataFrame([
    {
        "pclass": 3,
        "sex": "female",
        "age": 25,
        "sibsp": 0,
        "parch": 0,
        "fare": 15.0,
        "embarked": "S"
    }
])


print("\nRAW INPUT")
print(raw_input)


# 7. MAKE PREDICTION FROM RAW INPUT

prediction = loaded_pipeline.predict(
    raw_input
)

prediction_probability = loaded_pipeline.predict_proba(
    raw_input
)


print("\nPREDICTION")
print(
    "Predicted class:",
    int(prediction[0])
)

if prediction[0] == 1:
    print("Prediction: Survived")
else:
    print("Prediction: Did not survive")


print(
    f"Probability of survival: "
    f"{prediction_probability[0][1]:.4f}"
)


# TASK 15 CONCLUSION

print("\nTASK 15 CONCLUSION")

print(
    "The complete preprocessing and Random Forest classifier "
    "were saved as a single joblib pipeline."
)

print(
    "The saved pipeline was successfully reloaded and used "
    "to make a prediction from raw input data."
)

print(
    "The raw input did not require manual preprocessing because "
    "the preprocessing steps are included inside the pipeline."
)