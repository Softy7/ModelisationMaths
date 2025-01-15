from matplotlib import pyplot as plt
import numpy as np

from Bernstein import *
from Point import Point
from math import sqrt
from mpl_toolkits.mplot3d import Axes3D


# Variable globale alpha
alpha = (-408 + sqrt(368064)) / 360

def factoriel(n: int, produit: int = 1) -> int:
    """
    Calcule la valeur factorielle
    :param n: La valeur factorielle à calculer
    :param produit: Valeur 1 par défaut si vide
    :return: retourne la factorielle
    """
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
    """
    Calcule le coefficient binomial
    :param k:
    :param n:
    :return: retourne le coefficient binomial
    """
    if  n >= k:
        return factoriel(n) / (factoriel(k) * factoriel(n - k))
    else:
        raise Exception("n doit être supérieur ou égal à k")


def bezier(points: list[Point]):
    """
    Calcule bézier pour tous les points en x et en y
    Ne marche pas pour la 3D
    :param points: une liste de points
    :return:
    """
    return ([Bernstein(i, len(points) - 1, points[i].x) for i in range(len(points))],
            [Bernstein(i, len(points) - 1, points[i].y) for i in range(len(points))])


def tranform_list_to_point(l: list[float]) -> Point:
    """
    Transforme une liste de float en coordonnées x, y ou x, y et z
    :param l:
    :return: retourne un Point
    """
    if len(l) == 2:
        return Point(l[0], l[1])
    elif len(l) == 3:
        return Point(l[0], l[1], l[2])
    else:
        raise Exception("La liste doit avoir 2 ou 3 éléments")

def transform_matrice_of_float_to_matrice_of_point(mat: list[list[list[float]]]) -> list[list[Point]]:
    """
    Transforme une matrice de liste de float en matrice de points
    :param mat:
    :return:
    """
    return [[tranform_list_to_point(cell) for cell in row] for row in mat]





def calculate_bezier_curve(points: list[Point], num_points: int = 100) -> tuple[list[float], list[float]]:
    """
    Permet de calculer les courbes de Bézier
    :param points: Une liste de points de contrôle
    :param num_points: Le nombre de points
    :return: retourne un tuple de liste de points pour les x et les y
    """
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



def controle_point_surface_bezier(points: list[list[Point]]):
    """
    Permet de créer une fonction de surface qui calcule un point 3D à partir de u et v sur une surface de Bézier
    :param points: Une matrice de points de contrôle en 2D
    :return: retourne la fonction surface qui retourne un point
    """
    n = len(points) - 1
    m = len(points[0]) - 1
    def surface(u: float, v: float) -> Point:
        """
        Retourne un point à partir des paramètres u et v de la matrice
        :param u:
        :param v:
        :return:
        """
        x, y, z = 0, 0, 0
        for i in range(n + 1):
            for j in range(m + 1):
                bernstein_u = coef_binomial(i, n) * (u ** i) * ((1 - u) ** (n - i))
                bernstein_v = coef_binomial(j, m) * (v ** j) * ((1 - v) ** (m - j))
                weight = bernstein_u * bernstein_v
                x += weight * points[i][j].x
                y += weight * points[i][j].y
                z += weight * points[i][j].z
        return Point(x, y, z)
    return surface

def calculate_surface_bezier(points: list[list[Point]], num_points: int = 100) -> tuple[list[float], list[float], list[float]]:
    """
    Permet de générer les coordonnées 3D d'une surface de Bézier
    :param points: une matrice de points de contrôle
    :param num_points: Le nombre de points à calculer
    :return: retourne un tuple de 3 listes de points pour les x, y et z
    """
    surface = controle_point_surface_bezier(points)
    u_values = np.linspace(0, 1, num_points)
    v_values = np.linspace(0, 1, num_points)
    x_vals, y_vals, z_vals = [], [], []
    for u in u_values:
        for v in v_values:
            p = surface(u, v)
            x_vals.append(p.x)
            y_vals.append(p.y)
            z_vals.append(p.z)
    return x_vals, y_vals, z_vals


def show_2D_graph(control_points: list[list[Point]], titre: str):
    """
    Permet d'afficher un graphe en 2 dimensions de différentes courbes de Bézier
    :param control_points: Une matrice de points de contrôle
    :param titre: Le titre du graph
    """
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
    plt.axis('equal')
    plt.title(titre)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    plt.grid(True)
    plt.show()

def show_3D_graph(control_points: list[list[Point]], titre: str):
    """
    Permet d'afficher un graphe en 3 dimensions de surfaces de Bézier
    :param control_points: Une matrice de points de contrôle
    :param titre: Le titre du graph
    """
    x_vals, y_vals, z_vals = calculate_surface_bezier(control_points)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x_vals, y_vals, z_vals, cmap='viridis', edgecolor='none', alpha=0.8)

    control_x = [point.x for row in control_points for point in row]
    control_y = [point.y for row in control_points for point in row]
    control_z = [point.z for row in control_points for point in row]
    ax.scatter(control_x, control_y, control_z, color='red', label='Points de contrôle')

    ax.set_title(titre)
    ax.axis('equal')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

def prog():
    """
    Le programme principal
    """

    # Test de fonctions
    print(factoriel(10))
    print(coef_binomial(5, 10))
    print(transform_matrice_of_float_to_matrice_of_point([[[0, 1], [0, 2]], [[0, 1], [0, 1]]]))

    # La lettre a
    points1 = [Point(0, 0), Point(0, alpha), Point(1-alpha, 1), Point(1,1)]
    points2 = [Point(0, 0), Point(0, -alpha), Point(1-alpha, -1), Point(1,-1)]
    points3 = [Point(2, 0), Point(2, alpha), Point(1+alpha, 1), Point(1,1)]
    points4 = [Point(2, 0), Point(2, -alpha), Point(1 + alpha, -1), Point(1, -1)]
    points5 = [Point(2, 1), Point(2, 0), Point(1.95, -0.75), Point(2.2, -1)]
    lettre_a = [points1, points2, points3, points4, points5]

    show_2D_graph(lettre_a, "Courbe de Bézier pour la lettre \"a\"")

    # La lettre P
    pointsP_1 = [Point(0, -1), Point(0, 3)]
    pointsP_2 = [Point(0, 1), Point(1, 1)]
    pointsP_3 = [Point(0, 3), Point(1, 3)]
    pointsP_4 = [Point( 2,2), Point(2, alpha + 2), Point(1 + alpha, 3), Point(1, 3)]
    points_P_5 = [Point(2, 2), Point(2, 2 - alpha), Point(1 + alpha, 1), Point(1, 1)]
    lettreP = [pointsP_1, pointsP_2, pointsP_3, pointsP_4, points_P_5]

    show_2D_graph(lettreP, "Courbe de Bézier pour la lettre \"P\"")

    # Une surface de Bézier (Partie 4 du projet)

    mat0 = [
        [[0, 0, 0], [0, 1, 0], [-1, 2, 0.5], [-1.5, 2.5, 1]],
        [[1, 0, 1], [1, 1, 1], [-1, 2, 1.5], [-1.5, 2.5, 2]],
        [[0.5, 0, 2], [1, 1, 2], [-1, 2, 2.5], [-2, 2.5, 3]],
        [[0, 0, 3], [0, 1, 3], [-1, 2, 4], [-2, 2.5, 4]],
    ]

    mat = [
        [Point(0,0,0), Point(0, 1, 0), Point(-1, 2, 0.5), Point(-1.5, 2.5, 1)],
        [Point(1, 0, 1), Point(1, 1, 1), Point(-1, 2, 1.5), Point(-1.5, 2.5, 2)],
        [Point(0.5, 0, 2), Point(1, 1, 2), Point(-1, 2, 2.5), Point(-2, 2.5, 3)],
        [Point(0, 0, 3), Point(0, 1, 3), Point(-1, 2, 4), Point(-2, 2.5, 4)]
    ]
    #show_3D_graph(transform_matrice_of_float_to_matrice_of_point(mat0), "Une surface de Bézier")
    show_3D_graph(mat, "Une surface de Bézier")






if __name__ == "__main__":
    prog()
