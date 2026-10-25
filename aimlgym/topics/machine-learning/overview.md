# Machine Learning

**You will be able to:** Build baselines and core models by hand, then use scikit-learn's estimator API, splits, pipelines, ColumnTransformer, cross-validation, grid search, trees, random forests, gradient boosting, ROC/PR thresholds and k-means in an end-to-end project.

**Topic prerequisites:** Pandas

Machine learning from the ground up, then with scikit-learn. You start with features, labels and
baselines, then learn the estimator API (`fit`, `predict`, `score`, `clone`), splitting,
classification metrics and scaling inside a pipeline. Least squares, gradient-descent regression
and logistic regression are built by hand; k-NN, validation curves, cross-validation,
ColumnTransformer pipelines, regularisation with grid search, decision trees, random forests,
gradient boosting, ROC and precision–recall thresholds and k-means use scikit-learn. A capstone
combines everything in one leak-free workflow.

**Packages:** `numpy`, `pandas` and `scikit-learn`. Where a library step replaces an earlier
from-scratch step, that step follows it as an **optional deep dive** showing what the library does
inside. **Project ideas:** a house-price predictor, a spam or fraud classifier, and serving your
model with FastAPI.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | ML-01 | [Features, Labels and Baseline Models](ml-baselines/problem.md) | beginner | NP-05 |
| 2 | ML-02 | [The scikit-learn Estimator API](sklearn-estimator-api/problem.md) | beginner | ML-01 |
| 3 | ML-03 | [Regression Metrics (optional deep dive)](regression-metrics/problem.md) | beginner | ML-01 |
| 4 | ML-04 | [Splitting Data with scikit-learn](sklearn-train-test-split/problem.md) | beginner | ML-02 |
| 5 | ML-05 | [Seeded Train/Test Split (optional deep dive)](train-test-split/problem.md) | beginner | ML-01, NP-10 |
| 6 | ML-06 | [Confusion Matrix, Precision, Recall, F1](classification-metrics/problem.md) | beginner | ML-01 |
| 7 | ML-07 | [Scaling inside a Pipeline](sklearn-scaler-pipeline/problem.md) | beginner | ML-04 |
| 8 | ML-08 | [Standard Scaler (fit on train only) (optional deep dive)](standard-scaler/problem.md) | beginner | ML-05 |
| 9 | ML-09 | [Least-Squares Line](least-squares-line/problem.md) | intermediate | ML-02, ST-11 |
| 10 | ML-10 | [Linear Regression by Gradient Descent](linreg-gradient-descent/problem.md) | intermediate | ML-09, MA-14 |
| 11 | ML-11 | [Logistic Regression from Scratch](logistic-regression/problem.md) | intermediate | ML-10, MA-03 |
| 12 | ML-12 | [k-Nearest Neighbours with scikit-learn](sklearn-knn/problem.md) | intermediate | ML-07, ML-11 |
| 13 | ML-13 | [k-Nearest Neighbors Classifier by Hand (optional deep dive)](knn-classifier/problem.md) | intermediate | ML-06, NP-11 |
| 14 | ML-14 | [Polynomial Features and Validation Curves](sklearn-polynomial-validation/problem.md) | intermediate | ML-12, ML-10 |
| 15 | ML-15 | [Polynomial Features and Overfitting by Hand (optional deep dive)](polynomial-overfitting/problem.md) | intermediate | ML-09, ML-05 |
| 16 | ML-16 | [Cross-Validation with scikit-learn](sklearn-cross-validation/problem.md) | intermediate | ML-14 |
| 17 | ML-17 | [k-Fold Cross-Validation by Hand (optional deep dive)](k-fold-cv/problem.md) | advanced | ML-15 |
| 18 | ML-18 | [Pipelines and ColumnTransformer](sklearn-column-transformer/problem.md) | intermediate | ML-16 |
| 19 | ML-P1 | [Project idea: House-Price Predictor](house-price-predictor/project.md) | ungraded | ML-02, ML-04, ML-16, ML-18 |
| 20 | ML-19 | [Regularisation and Hyperparameter Search](sklearn-grid-search/problem.md) | advanced | ML-18 |
| 21 | ML-20 | [Ridge Regression (Closed Form) (optional deep dive)](ridge-regression/problem.md) | advanced | ML-17, ML-08 |
| 22 | ML-21 | [Decision Stump with Gini Impurity](decision-stump-gini/problem.md) | advanced | ML-06 |
| 23 | ML-22 | [Decision Trees and Random Forests](sklearn-trees-forests/problem.md) | advanced | ML-21, ML-19 |
| 24 | ML-23 | [Gradient Boosting](sklearn-gradient-boosting/problem.md) | advanced | ML-22 |
| 25 | ML-24 | [Thresholds, ROC and Precision–Recall Curves](sklearn-roc-pr/problem.md) | advanced | ML-23, ML-06 |
| 26 | ML-25 | [k-Means and Silhouette Scores](sklearn-kmeans/problem.md) | advanced | ML-24 |
| 27 | ML-26 | [k-Means Clustering by Hand (optional deep dive)](kmeans/problem.md) | advanced | ML-13 |
| 28 | ML-27 | [Capstone: an End-to-End Tabular Model](ml-capstone/problem.md) | advanced | ML-25, ML-18 |
| 29 | ML-P2 | [Project idea: Spam or Fraud Classifier](spam-fraud-classifier/project.md) | ungraded | ML-06, ML-23, ML-24, ML-27 |
| 30 | ML-P3 | [Project idea: Serve Your Model with FastAPI](serve-your-model/project.md) | ungraded | ML-27, FA-08, FA-10, FA-12, FA-15 |
