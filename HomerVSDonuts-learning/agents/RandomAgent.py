import numpy as np

'''
Première IA : "random".  Sélectionne les actions au hasard à chaque fois!
'''

class RandomAgent():
    def __init__(self):
        self.number_of_moves = 0

    def selectAction(self, coordinates):
        self.number_of_moves += 1
        return np.random.choice(['up', 'down', 'left', 'right'])

    def display(self):
        print("===== Random Agent =====")
