from Projet import coef_binomial

class Bernstein:

    def __init__(self, i, n, factor):
        """
        Donne tous les éléments de la formule de Benstein
        :param i: valeur i
        :param n: valeur n
        :param factor: facteur
        """
        self.coef = coef_binomial(i, n)
        self.i = i
        self.n = n
        self.factor = factor


    def calculate(self, t: int | float) -> float:
        """
        Permet de calculer la formule de Benstein
        :param t: valeur t
        :return: retourne la valeur
        """
        return self.coef * (t ** self.i) * ((1 - t)**(self.n - self.i)) * self.factor
