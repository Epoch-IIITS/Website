# ML-P2 · Project idea: Spam or Fraud Classifier

**Topic:** Machine Learning · ungraded

## Brief

Build a classifier for a problem where the interesting class is rare — spam messages or fraudulent
transactions — and choose a decision threshold that reflects real costs: a missed fraud is
expensive, but so is blocking a real customer.

## You will use

- ML-06 Confusion Matrix, Precision, Recall, F1
- ML-23 Gradient Boosting
- ML-24 Thresholds, ROC and Precision–Recall Curves
- ML-27 Capstone: an End-to-End Tabular Model

## Milestones

1. Load the data, measure the class imbalance and fit a majority-class baseline.
2. Train a logistic regression pipeline and a gradient-boosting model with stratified cross-validation.
3. Compare them with ROC AUC and average precision, and plot both curves.
4. Choose a threshold from the precision–recall curve on validation data for a target recall.
5. Report the confusion matrix and the cost per 1,000 cases at that threshold on the test set.

## Stretch goals

- Try class_weight='balanced' and compare it with moving the threshold.
- For SMS spam, turn the messages into TF-IDF features (see the NLP topic).
- Check how the precision changes if fraud becomes twice as rare after deployment.

## Data

* [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) (UCI): 5,574
  labelled text messages, about 13% spam.
* Synthetic transactions: `sklearn.datasets.make_classification(n_samples=20000, weights=[0.98, 0.02], random_state=0)`
  ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)).

## Run it yourself

```bash
pip install numpy pandas scikit-learn matplotlib
python fraud.py
```
