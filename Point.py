from Courbe import Courbe

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connexion = []

    def ajouterConnexion(self, courbe: Courbe):
        self.connexion.append(courbe)

    def retirerConnexion(self, courbe: Courbe):
        self.connexion.remove(courbe)

