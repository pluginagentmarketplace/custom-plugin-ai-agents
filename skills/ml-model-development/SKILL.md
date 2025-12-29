---
name: ml-model-development
description: Build machine learning models with scikit-learn, feature engineering, model evaluation, cross-validation, hyperparameter tuning, and MLflow. Use when developing, training, and deploying ML models.
---

# ML Model Development

Master machine learning fundamentals with scikit-learn, advanced feature engineering, model evaluation, and experiment tracking with MLflow.

## Quick Start

### Data Preprocessing & Exploration
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load and explore data
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())

# Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Split data
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## Feature Engineering

### Feature Creation
```python
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_train)

# Categorical encoding
categorical_features = ['color', 'size']
numeric_features = ['price', 'quantity']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ]
)

X_processed = preprocessor.fit_transform(X_train)
```

### Feature Selection
```python
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

# SelectKBest
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X_train, y_train)
selected_features = X_train.columns[selector.get_support()].tolist()

# RFE - Recursive Feature Elimination
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(estimator=rf, n_features_to_select=10)
X_rfe = rfe.fit_transform(X_train, y_train)

# Feature importance
importances = rf.fit(X_train, y_train).feature_importances_
```

## Model Training

### Classification Models
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Logistic Regression
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

# Random Forest
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

# Gradient Boosting
gb = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
gb.fit(X_train, y_train)

# SVM
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train_scaled, y_train)
```

### Regression Models
```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# Ridge Regression (L2 regularization)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_scaled, y_train)

# Lasso Regression (L1 regularization)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train_scaled, y_train)

# ElasticNet (L1 + L2)
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic.fit(X_train_scaled, y_train)

# Random Forest Regressor
rf_reg = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
rf_reg.fit(X_train, y_train)
```

## Cross-Validation

### K-Fold Cross-Validation
```python
from sklearn.model_selection import (
    cross_val_score,
    cross_validate,
    KFold,
    StratifiedKFold
)

# Simple cross-validation
scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='accuracy')
print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Stratified K-Fold (for imbalanced datasets)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(rf, X_train, y_train, cv=skf, scoring='f1_weighted')

# Multiple metrics
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision_weighted',
    'recall': 'recall_weighted',
    'f1': 'f1_weighted'
}
cv_results = cross_validate(rf, X_train, y_train, cv=5, scoring=scoring)
```

## Hyperparameter Tuning

### Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.4f}")
```

### Random Search
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(50, 300),
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'learning_rate': uniform(0.01, 0.3)
}

random_search = RandomizedSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_dist,
    n_iter=20,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
best_model = random_search.best_estimator_
```

## Model Evaluation

### Classification Metrics
```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc
)
import matplotlib.pyplot as plt

y_pred = best_model.predict(X_test)
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

# Metrics
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print(f"F1: {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Classification Report
print(classification_report(y_test, y_pred))

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
```

### Regression Metrics
```python
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)

y_pred = best_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R² Score: {r2:.4f}")
print(f"MAPE: {mape:.4f}")
```

## MLflow Integration

### Track Experiments
```python
import mlflow
from mlflow.sklearn import log_model

# Set experiment
mlflow.set_experiment("ml_experiment")

with mlflow.start_run(run_name="rf_baseline"):
    # Log parameters
    mlflow.log_params({
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    })

    # Train model
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    # Log metrics
    mlflow.log_metrics({
        'accuracy': accuracy_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred)
    })

    # Log model
    log_model(rf, "model")

    # Log artifacts
    mlflow.log_artifact("model_summary.txt")
```

### Load Tracked Models
```python
# Load model by run ID
logged_model = "runs:/run_id/model"
loaded_model = mlflow.pyfunc.load_model(logged_model)
predictions = loaded_model.predict(X_test)

# Search experiments
experiment = mlflow.get_experiment_by_name("ml_experiment")
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
best_run = runs.loc[runs['metrics.f1'].idxmax()]
```

## Pipeline

### End-to-End Pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Define preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

# Create pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)
```

## Best Practices

✅ **Always split data** before preprocessing
✅ **Scale features** appropriately (StandardScaler, MinMaxScaler)
✅ **Handle missing values** before training
✅ **Use cross-validation** for robust evaluation
✅ **Track experiments** with MLflow
✅ **Feature engineering** based on domain knowledge
✅ **Regularization** to prevent overfitting
✅ **Class imbalance** handling (SMOTE, class weights)
✅ **Monitor model** performance on test set

## Common Pitfalls

❌ Data leakage (scaling before split, using test data in preprocessing)
❌ Ignoring class imbalance
❌ Not using stratified k-fold for imbalanced data
❌ Overfitting through excessive hyperparameter tuning
❌ Ignoring feature importance
❌ Not documenting experiments
❌ Training on test data accidentally

## Resources

- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Feature Engineering for ML](https://github.com/3778/awesome-feature-engineering)
- [Scikit-learn Cheatsheet](https://scikit-learn.org/stable/tutorial.html)
