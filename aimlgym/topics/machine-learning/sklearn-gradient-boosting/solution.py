r"""Reference solution for ML-23 Gradient Boosting.

`staged_predict_proba` replays the ensemble one tree at a time, so a single fit yields the whole
loss curve. Training loss keeps falling as trees are added, while validation loss bottoms out;
its minimum marks how many trees to keep.
"""
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss


def boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0):
    if max_iter < 1 or learning_rate <= 0:
        raise ValueError("need max_iter >= 1 and learning_rate > 0")
    model = HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=learning_rate,
                                           early_stopping=False, random_state=seed)
    model.fit(X_train, y_train)
    train_loss = [float(log_loss(y_train, p, labels=[0, 1])) for p in model.staged_predict_proba(X_train)]
    val_loss = [float(log_loss(y_val, p, labels=[0, 1])) for p in model.staged_predict_proba(X_val)]
    return {"train_loss": train_loss, "val_loss": val_loss,
            "best_iteration": val_loss.index(min(val_loss)) + 1,
            "val_accuracy": float(model.score(X_val, y_val))}
