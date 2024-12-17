from matplotlib import pyplot as plt
import numpy as np


def factoriel(n: int, produit: int = 1) -> int:
    if n < 0:
        raise Exception("n doit être positif")
    if n == 0:
        return 1
    if n == 1:
        return produit
    else:
        produit *= n
        return factoriel(n - 1, produit)

def coef_binomial(k: int, n: int) -> float:
    if  n >= k:
        return factoriel(n) / (factoriel(k) * factoriel(n - k))
    else:
        raise Exception("n doit être supérieur ou égal à k")

def bernstain(i: int, n: int, t: float):
    return coef_binomial(i, n) * (t**i) * ((1-t)**(n-i))

def bezier():
    pass

def prog():
    #plt.ion()
    #plt.plot()
    #plt.show()
    print(factoriel(10))
    print(coef_binomial(5, 10))
    print(bernstain(0, 3, (1/3)))


if __name__ == "__main__":
    prog()
