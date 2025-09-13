from math import sqrt, log

class UCB1:
    def __init__(self, n_arms, c=1.41421356237):
        self.n = [0]*n_arms
        self.s = [0.0]*n_arms
        self.c = c
        self.t = 0

    def select(self):
        self.t += 1
        values = []
        for i in range(len(self.n)):
            if self.n[i] == 0:
                values.append(float("inf"))
            else:
                avg = self.s[i] / self.n[i]
                bonus = self.c * sqrt(log(self.t) / self.n[i])
                values.append(avg + bonus)
        return max(range(len(values)), key=lambda i: values[i])

    def update(self, arm, reward):
        self.n[arm] += 1
        self.s[arm] += reward
