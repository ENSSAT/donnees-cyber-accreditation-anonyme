import numpy as np
import hashlib

class Graphe3Coloriable:
    size: int
    labels = ['r', 'v', 'b']
    colors: np.array
    graph: np.array

    def __init__(self, size=20):
        self.size = size
        self.random_colors()
        self.random_adjacency()

    def random_colors(self):
        self.colors = np.random.randint(0, 3, self.size)

    def random_adjacency(self):
        self.graph = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(0, i):
                if self.colors[i] != self.colors[j]:
                    self.graph[i, j] = self.graph[j, i] = 1 * (np.random.rand()<0.5)
    
    @property
    def colors_labels(self):
        """
        Renvoie les couleurs des noeuds sous forme d'une liste de strings
        """
        return [self.labels[self.colors[i]].encode('utf-8') for i in range(self.size)]

    def __str__(self):
        string = "  " + " ".join(map(lambda clr: self.labels[clr], self.colors)) + '\n'
        for i in range(self.size):
            string += self.labels[self.colors[i]] + ' '
            string += ' '.join([' ' if self.graph[i, j] == 0 else 'x' for j in range(self.size)]) + '\n'
        return string



def genererGraphe3Coloriable():
    return Graphe3Coloriable(20)

def miseEnGageColoriage(couleurs, rand_array):
    print(list(
        map(b''.join, zip(couleurs, rand_array))
    ))


graphe = genererGraphe3Coloriable()

# generate 128 random bytes for each node of the graph
rand_array = [np.random.bytes(128) for _ in range(graphe.size)]

# workout a hash for each node's color
miseEnGageColoriage(graphe.colors_labels, rand_array)
