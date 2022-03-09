"""
Le type d'agent à créer pour jouer vous même avec le clavier
(dans les faits cette classe est peu utile, juste créée à titre d'exemple & pour être consistante avec RandomAgent)
/!\ Le jeu avec ce mode ne marche pas sans interface graphique !
"""

class HumanAgent():
    def __init__(self):
        pass

    # Exception: pas de fonction pour sélectionner une action ici (car directement fait dans la boucle pygame, en prenant en compte les touches du clavier)


    def display(self):
        print("===== Human Agent =====")
