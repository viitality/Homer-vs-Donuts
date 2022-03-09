from agents.RandomAgent import *
from agents.HumanAgent import *

"""
AgentInterface permet juste de faire la liaison entre les agents et le jeu de façon plus "propre". 
Avec le bon argument pour "agent_type", le bon type d'agent est créé.
Pour jouer au jeu vous même avec les touches du clavier, sélectionnez "human" pour agent_type
"""

class AgentInterface():
    def __init__(self, agent_type, agent_params): # agent_params pas nécessaire pour le moment, mais pourra être utile pour les futurs algorithmes
        self.agent_type = agent_type
        self.choice = ''

        if agent_type == 'random':
            self.agent = RandomAgent()
        elif agent_type == 'human':
            self.agent = HumanAgent()

    def selectAction(self,coordinates):
        if self.agent_type != 'human': # pour 'human', le choix d'action est directement fait dans Game.py (avec les touches du clavier, grâce à pygame)
            self.choice = self.agent.selectAction(coordinates)


    def display(self):
        self.agent.display()

