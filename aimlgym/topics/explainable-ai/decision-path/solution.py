r"""Reference solution for XA-03 Tracing a Decision Path.

The loop walks from the root to a leaf, recording the condition satisfied at each internal node
using the same `<=` convention as training. The leaf's value is the prediction.
"""
def predict_with_path(tree, x, feature_names):
    node, path = tree, []
    while "value" not in node:
        if not all(k in node for k in ("feature", "threshold", "left", "right")):
            raise ValueError("malformed node")
        j, t = node["feature"], node["threshold"]
        name = feature_names[j]
        if x[j] <= t:
            path.append(f"{name} <= {t}")
            node = node["left"]
        else:
            path.append(f"{name} > {t}")
            node = node["right"]
    return node["value"], path
