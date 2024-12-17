from matplotlib import pyplot as plt
import numpy as np

from Bernstain import *
import Point
from math import sqrt


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


def bezier(points: list[Point.Point]):
    return ([Bernstain(i, len(points) - 1, points[i].x) for i in range(len(points))],
            [Bernstain(i, len(points) - 1, points[i].y) for i in range(len(points))])


def calculate_bezier_curve(points: list[Point.Point], num_points: int = 100) -> tuple[list[float], list[float]]:
    x_points = []
    y_points = []
    bernstains = bezier(points)
    t_values = np.linspace(0, 1, num_points)
    for t in t_values:
        x = sum(b.calculate(t) for b in bernstains[0])
        y = sum(b.calculate(t) for b in bernstains[1])
        x_points.append(x)
        y_points.append(y)
    return x_points, y_points

def prog():
    #plt.ion()
    #plt.plot()
    #plt.show()
    alpha = (-408 + sqrt(368064)) / 360
    print(factoriel(10))
    print(coef_binomial(5, 10))
    points = [Point.Point(0, 0), Point.Point(0, alpha), Point.Point(1-alpha, 1), Point.Point(1,1)]


    x_points, y_points = calculate_bezier_curve(points)

    plt.figure(figsize=(8, 6))
    plt.plot(x_points, y_points, label='Courbe de Bézier')

    # Tracer les points de contrôle
    control_x = [p.x for p in points]
    control_y = [p.y for p in points]
    plt.plot(control_x, control_y, 'ro--', label='Points de contrôle')

    # Ajouter des titres et des labels
    plt.title('Courbe de Bézier')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Afficher la grille
    plt.grid(True)

    # Afficher le graphe
    plt.show()




if __name__ == "__main__":
    prog()
