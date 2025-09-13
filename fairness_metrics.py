def weighted_gini(values, weights):
    # values: per-segment composite outcomes (higher is better)
    # weights: segment populations or importance weights (sum > 0)
    if len(values) == 0:
        return 0.0
    # sort by value
    paired = sorted(zip(values, weights), key=lambda x: x[0])
    cumw = 0.0
    cumval = 0.0
    totalw = sum(weights)
    total = sum(v*w for v,w in paired)
    if total == 0 or totalw == 0:
        return 0.0
    gini = 1.0
    for v,w in paired:
        prev_cumw = cumw
        cumw += w
        cumval += v*w
        gini -= (cumval/total) * ((cumw/totalw) + (prev_cumw/totalw))
    return max(0.0, min(1.0, gini))

def fairness_index(values, weights):
    # 1 - Gini (so higher is fairer)
    g = weighted_gini(values, weights)
    return 1.0 - g
