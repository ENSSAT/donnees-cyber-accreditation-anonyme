import numpy as np
import hashlib
from collections import defaultdict

class Graphe3Coloriable:
    size: int
    labels = ['r', 'v', 'b']
    colors: np.array
    matrix: np.array

    def __init__(self, size=20):
        self.size = size
        self.random_colors()
        self.random_adjacency()


    def random_colors(self):
        """
        Choisi des couleurs aléatoires pour les noeuds du graphe.
        """
        self.colors = np.random.randint(0, 3, self.size)


    def random_adjacency(self):
        """
        Calcule aléatoirement une matrice d'adjacence.
        """
        self.matrix = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(0, i):
                if self.colors[i] != self.colors[j]:
                    self.matrix[i, j] = self.matrix[j, i] = 1 * (np.random.rand()<0.5)
    

    def random_adjacent_nodes(self):
        """
        Renvoie les indices de 2 noeuds adjacents du graphe
        """
        rows, cols = self.matrix.nonzero()

        # recupere le nombre de ces noeuds
        n = rows.shape

        # tire aleatoirement un couple de noeuds adjacents
        # ie de couleur differente
        r = np.random.randint(0, n, size=1)[0]
        i, j = rows[r], cols[r]
        return i, j


    def __str__(self):
        """
        Utile pour afficher la matrice du graphe
        """
        string = "  " + " ".join(map(lambda clr: self.labels[clr], self.colors)) + '\n'
        for i in range(self.size):
            string += self.labels[self.colors[i]] + ' '
            string += ' '.join([' ' if self.matrix[i, j] == 0 else 'x' for j in range(self.size)]) + '\n'
        return string


def generer_graphe_3_coloriable():
    return Graphe3Coloriable(20)


def salt_hash(color, rand_bytes):
    return hashlib.sha256(color + rand_bytes).hexdigest()


def miseEnGageColoriage(couleurs, rand_array):
    return list(
        map(
            lambda couple: salt_hash(*couple), 
            zip(couleurs, rand_array)
        )
    )


def preuveColoriage(matrice, coloriage, i, j, ri, ci, rj, cj):
    return salt_hash(ci, ri) == coloriage[i] and salt_hash(cj, rj) == coloriage[j] and ci != cj


def genererGraphe3Coloriable():
    return Graphe3Coloriable()


class Utilisateur:
    """
    Objet simulant un utilisateur permettant
    de tester l'algorithme d'échange de 3-coloriage
    """

    def __init__(self, graphe):
        """
        Construit un utilisateur ayant connaissance
        d'un 3-coloriage du graphe donné.
        """
        self.graphe = graphe

    def envoyerMiseEnGage(self, verificateur):
        """
        Envoie les hashés des noeuds à un verificateur.
        """
        # genere une permutation d'un ensemble a 3 elts
        permutation = np.random.permutation(3)

        # permute les couleurs des noeuds
        self.c = [graphe.labels[permutation[color]].encode('utf-8') for color in graphe.colors]
        
        # genere 128 bits aleatoire pour chaque noeud
        self.r = [np.random.bytes(128) for _ in range(graphe.size)]

        # calcul un hash associe à chaque noeud
        self.y = miseEnGageColoriage(self.c, self.r)

        # envoie la mise en gage
        verificateur.misesEnGage[self] = self.y

    def donnerCouleurs(self, i, j):
        """
        Renvoie les couleurs permutées et le hashés des noeuds i et j.
        """
        reponse = [self.r[i], self.c[i], self.r[j], self.c[j]]
        return reponse


class Verificateur:
    """
    Objet simulant un utilisateur permettant
    de tester l'algorithme d'échange de 3-coloriage
    """
    # stock les mises en gage pour chaque utilisateur
    misesEnGage = {}
    # compte les success par utilisateur
    success = defaultdict(int)
    # compte les echecs par utilisateur
    echecs = defaultdict(int)

    def __init__(self, graphe):
        """
        Construit un vérificateur ayant connaissance
        d'un 3-coloriage du graphe donné.
        """
        self.graphe = graphe

    def choisirNoeuds(self):
        """
        Choisi aléatoirement un couple de noeuds adjacent.
        """
        return self.graphe.random_adjacent_nodes()

    def demanderCouleurs(self, utilisateur, i, j):
        """
        Demande la couleur du noeud i,j à l'utilisateur.
        """
        return utilisateur.donnerCouleurs(i, j)

    def verifierMiseEnGage(self, utilisateur, i, j, reponse):
        """
        Recupere la reponse de l'utilisateur pour le défi.
        """
        # verifie que le coloriage est valide
        success = preuveColoriage(self.graphe.matrix, self.misesEnGage[utilisateur], i, j, *reponse)
        # incremente le compteur de success ou d'echec
        if success:
            self.success[utilisateur] += 1
        else:
            self.echecs[utilisateur] += 1
        # renvoie le resultat pour verification
        return success

help(Utilisateur)
help(Verificateur)

if __name__ == '__main__':
    # genere un graphe 3 coloriable
    graphe = genererGraphe3Coloriable()
    
    # cree un utilisateur et un verificateur 
    # tout 2 connaissant le même graphe
    utilisateur = Utilisateur(graphe)
    verificateur = Verificateur(graphe)

    # effectue suffisament de verification pour se
    # convaincre que l'utilisateur dit vrai
    for k in range(400):
        utilisateur.envoyerMiseEnGage(verificateur)

        i, j = verificateur.choisirNoeuds()
        reponse = verificateur.demanderCouleurs(utilisateur, i, j)
        # la reponse est un quadruplet de la forme [ri, ci, rj, cj]

        resultat = verificateur.verifierMiseEnGage(utilisateur, i, j, reponse)
    
    print('success: %s, echec: %s'%(
        verificateur.success[utilisateur],
        verificateur.echecs[utilisateur]
    ))
