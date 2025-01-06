from cProfile import label

from matplotlib import pyplot as plt
import numpy as np

from Bernstain import *
from Point import Point
from math import sqrt

alpha = (-408 + sqrt(368064)) / 360

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


def bezier(points: list[Point]):
    return ([Bernstain(i, len(points) - 1, points[i].x) for i in range(len(points))],
            [Bernstain(i, len(points) - 1, points[i].y) for i in range(len(points))])


def calculate_bezier_curve(points: list[Point], num_points: int = 100) -> tuple[list[float], list[float]]:
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

def show_2D_graph(control_points: list[list[Point]], titre: str):
    plt.figure(figsize=(8, 6))
    for i in range(len(control_points)):
        x_points, y_points = calculate_bezier_curve(control_points[i])

        # trace la courbe de Bézier
        plt.plot(x_points, y_points, 'k-')

        # trace les points de contrôle
        control_x = [p.x for p in control_points[i]]
        control_y = [p.y for p in control_points[i]]
        plt.plot(control_x, control_y, 'ro--')

    plt.plot([], [], 'ro--', label='Points de contrôle')
    plt.plot([], [], 'k-', label='Courbes de Bézier')
    # plt.plot(control_x, control_y, 'ro--', label=f'Points de contrôle')
    plt.title(titre)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    plt.grid(True)
    plt.show()

def prog():
    #plt.ion()
    #plt.plot()
    #plt.show()

    print(factoriel(10))
    print(coef_binomial(5, 10))
    points1 = [Point(0, 0), Point(0, alpha), Point(1-alpha, 1), Point(1,1)]
    points2 = [Point(0, 0), Point(0, -alpha), Point(1-alpha, -1), Point(1,-1)]
    points3 = [Point(2, 0), Point(2, alpha), Point(1+alpha, 1), Point(1,1)]
    points4 = [Point(2, 0), Point(2, -alpha), Point(1 + alpha, -1), Point(1, -1)]
    points5 = [Point(2, 1), Point(2, 0), Point(1.95, -0.75), Point(2.2, -1)]
    lettre_a = [points1, points2, points3, points4, points5]

    show_2D_graph(lettre_a, "Courbe de Bézier pour la lettre \"a\"")

    pointsP_1 = [Point(0, -1), Point(0, 3)]
    pointsP_2 = [Point(0, 1), Point(1, 1)]
    pointsP_3 = [Point(0, 3), Point(1, 3)]
    pointsP_4 = [Point(2, 2), Point(2, alpha + 2), Point(1 + alpha, 3), Point(1, 3)]
    # points_P_5 = [Point(0, 3), Point(0, 3)]
    lettreP = [pointsP_1, pointsP_2, pointsP_3, pointsP_4]

    show_2D_graph(lettreP, "Courbe de Bézier pour la lettre \"P\"")




if __name__ == "__main__":
    prog()
