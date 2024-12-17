from Projet import coef_binomial

class Bernstain:

    def __init__(self, i, n, factor):
        self.coef = coef_binomial(i, n)
        self.i = i
        self.n = n
        self.factor = factor


    def calculate(self, t: int):
        return self.coef * (t ** self.i) * ((1 - t)**(self.n - self.i)) * self.factor



