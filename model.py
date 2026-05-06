import pickle
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

warnings.filterwarnings("ignore")

TARGET_ACCURACY = 0.95
RANDOM_STATE = 42
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"
DATASET_PATH = DATA_DIR / "kelulusan.csv"

DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def calculate_theoretical_limit(df, feature_columns, target_column):
    """
    Estimates the best possible accuracy when rows with identical features
    have conflicting target labels.
    """
    grouped = (
        df.groupby(feature_columns)[target_column]
        .value_counts()
        .unstack(fill_value=0)
    )
    max_correct = grouped.max(axis=1).sum()
    ambiguous_patterns = int((grouped > 0).sum(axis=1).gt(1).sum())
    return max_correct / len(df), ambiguous_patterns, grouped


# ==================== LOAD DATA ====================
print("=" * 60)
print("DECISION TREE C4.5 MODEL")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)
print(f"\n[OK] Data loaded: {len(df)} records")
print(f"[OK] Features: {list(df.columns)}")
print(f"\nData shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# ==================== DATA PREPROCESSING ====================
print_section("DATA PREPROCESSING")

X = df.drop("Kelulusan", axis=1)
y = df["Kelulusan"]

print("\nTarget distribution:")
print(y.value_counts())

limit_accuracy, ambiguous_patterns, grouped_patterns = calculate_theoretical_limit(
    df=df,
    feature_columns=list(X.columns),
    target_column="Kelulusan",
)

print("\nDataset consistency check:")
print(f"  Unique feature patterns: {len(grouped_patterns)}")
print(f"  Ambiguous patterns: {ambiguous_patterns}")
print(f"  Estimated maximum accuracy from current features: {limit_accuracy:.4f} ({limit_accuracy * 100:.2f}%)")

if limit_accuracy < TARGET_ACCURACY:
    print(
        f"\n[WARNING] Target {TARGET_ACCURACY * 100:.0f}% is not realistic with the current dataset/features."
    )
    print(
        "Rows with exactly the same feature values have different Kelulusan labels, "
        "so the model cannot reliably separate them."
    )

label_encoders = {}
X_encoded = X.copy()

for column in X_encoded.columns:
    le = LabelEncoder()
    X_encoded[column] = le.fit_transform(X_encoded[column])
    label_encoders[column] = le
    mapping = {str(label): int(value) for label, value in zip(le.classes_, le.transform(le.classes_))}
    print(f"[OK] {column}: {mapping}")

le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
target_mapping = {
    str(label): int(value)
    for label, value in zip(le_target.classes_, le_target.transform(le_target.classes_))
}
print(f"[OK] Kelulusan: {target_mapping}")

# ==================== SPLIT DATA ====================
print_section("TRAIN-TEST SPLIT")

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y_encoded,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y_encoded,
)

print(f"\nTraining set: {len(X_train)} samples ({len(X_train) / len(X) * 100:.1f}%)")
print(f"Testing set: {len(X_test)} samples ({len(X_test) / len(X) * 100:.1f}%)")

# ==================== TRAIN C4.5 DECISION TREE ====================
print_section("DECISION TREE C4.5 TRAINING + TUNING")

base_model = DecisionTreeClassifier(
    criterion="entropy",
    random_state=RANDOM_STATE,
)

param_grid = {
    "max_depth": [None, 2, 3, 4, 5, 6],
    "min_samples_split": [2, 4, 6, 8, 10],
    "min_samples_leaf": [1, 2, 3, 4, 5],
    "class_weight": [None, "balanced"],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    scoring="accuracy",
    cv=cv,
    n_jobs=1,
    refit=True,
)
grid_search.fit(X_train, y_train)
dt_model = grid_search.best_estimator_

print("\n[OK] Model trained successfully")
print(f"[OK] Best CV accuracy: {grid_search.best_score_:.4f} ({grid_search.best_score_ * 100:.2f}%)")
print(f"[OK] Best parameters: {grid_search.best_params_}")
print(f"[OK] Tree depth: {dt_model.get_depth()}")
print(f"[OK] Number of leaves: {dt_model.get_n_leaves()}")
print("[OK] Feature importances:")

feature_importance = pd.DataFrame(
    {
        "Feature": X.columns,
        "Importance": dt_model.feature_importances_,
    }
).sort_values("Importance", ascending=False)

for _, row in feature_importance.iterrows():
    print(f"  - {row['Feature']}: {row['Importance']:.4f}")

# ==================== PREDICTION & EVALUATION ====================
print_section("MODEL EVALUATION")

y_train_pred = dt_model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)

y_test_pred = dt_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)

print("\nACCURACY:")
print(f"  Training Accuracy: {train_accuracy:.4f} ({train_accuracy * 100:.2f}%)")
print(f"  Testing Accuracy:  {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")

if test_accuracy >= TARGET_ACCURACY:
    print(f"\n[OK] Target accuracy {TARGET_ACCURACY * 100:.0f}% achieved.")
else:
    print(f"\n[WARNING] Target accuracy {TARGET_ACCURACY * 100:.0f}% not achieved.")
    print("To approach 95%, add stronger predictive features or clean conflicting labels in data/kelulusan.csv.")

print("\nDETAILED METRICS (Testing Set):")
print(f"  Precision: {precision_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"  Recall:    {recall_score(y_test, y_test_pred, average='weighted'):.4f}")
print(f"  F1-Score:  {f1_score(y_test, y_test_pred, average='weighted'):.4f}")

cm = confusion_matrix(y_test, y_test_pred)
print("\nCONFUSION MATRIX:")
print(cm)

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(
        y_test,
        y_test_pred,
        target_names=le_target.classes_,
        digits=4,
    )
)

# ==================== VISUALIZATION ====================
print_section("SAVING VISUALIZATIONS")

plt.figure(figsize=(25, 15))
plot_tree(
    dt_model,
    feature_names=X.columns,
    class_names=le_target.classes_,
    filled=True,
    rounded=True,
    fontsize=10,
)
plt.title("Decision Tree C4.5 Model", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig(ASSETS_DIR / "decision_tree_visualization.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: assets/decision_tree_visualization.png")
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(feature_importance["Feature"], feature_importance["Importance"], color="steelblue")
plt.xlabel("Importance", fontsize=12)
plt.ylabel("Feature", fontsize=12)
plt.title("Feature Importance in C4.5 Decision Tree", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(ASSETS_DIR / "feature_importance.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: assets/feature_importance.png")
plt.close()

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le_target.classes_)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix - Testing Set", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(ASSETS_DIR / "confusion_matrix.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: assets/confusion_matrix.png")
plt.close()

# ==================== SAMPLE PREDICTIONS ====================
print_section("SAMPLE PREDICTIONS")

print("\nTesting set predictions (first 10 samples):")
print(f"{'Actual':<15} {'Predicted':<15} {'Match':<10}")
print("-" * 40)

for i in range(min(10, len(y_test))):
    actual = le_target.classes_[y_test[i]]
    predicted = le_target.classes_[y_test_pred[i]]
    match = "Yes" if actual == predicted else "No"
    print(f"{actual:<15} {predicted:<15} {match:<10}")

# ==================== SAVE MODEL ====================
with open(MODELS_DIR / "model_c45.pkl", "wb") as f:
    pickle.dump(dt_model, f)
with open(MODELS_DIR / "label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)
with open(MODELS_DIR / "target_encoder.pkl", "wb") as f:
    pickle.dump(le_target, f)

print("\n[OK] Model saved: models/model_c45.pkl")
print("[OK] Encoders saved: models/label_encoders.pkl, models/target_encoder.pkl")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
