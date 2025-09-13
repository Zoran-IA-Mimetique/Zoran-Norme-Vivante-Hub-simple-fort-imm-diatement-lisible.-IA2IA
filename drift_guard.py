def guard_fairness(prev_F, curr_F, theta=0.03):
    """Return True if rollback should trigger"""
    return (curr_F < prev_F - theta)
