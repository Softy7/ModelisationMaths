from Connexion import Connexion

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connexion = []

    def ajouterConnexion(self, connexion: Connexion):
        self.connexion.append(connexion)

    def retirerConnexion(self, connexion: Connexion):
        self.connexion.remove(connexion)

