
from Game import *
from AgentInterface import *

from optparse import OptionParser
import sys

#random.seed(0) # peut être utilisé pour "répéter" les simulations (même résultats pour les fonction random d'une exécution du code à une autre)

def manage_arguments():
    """
    Manage the arguments of the script.
    """

    usage = "usage: main.py [options] "
    parser = OptionParser(usage)
    parser.add_option("-a", "--agent_type", action="store", type="string", dest="agent_type", help="This parameters allows to select a specific algorithm for the agent", default="human")
    parser.add_option("-e", "--episodes", action="store", type="int", dest="nb_episodes",
                      help="This is the number of epochs in a training session ", default=2)

    parser.add_option("-g", "--graphics", action="store", type="string", dest="graphics",
                      help="Display or not the graphical interface of the game ", default='True')

    parser.add_option("-w", "--wait_", action="store", type="string", dest="wait_",
                      help=" wait between each action of the game ", default='True')

    (options, args) = parser.parse_args()



    return(options)

def Homer_VS_Donuts_instance(agent_interface, game_map, initial_position, probasDirectory, graphics = True, wait = True):
    """
    Lance une partie du jeu.
    :param agent_interface: L'interface déjà créée avec l'agent
    :param game_map: Le plateau initial
    :param initial_position: La position initiale de Homer sur le plateau
    :param probasDirectory: Le dictionnaire des probabilités de se tromper de déplacement
    :param graphics: Permet de lancer le jeu avec ou sans le rendu graphique
    :param wait: Force un temps d'attente entre chaque sélection d'action
    :return: les résultats du jeu (output = Tous les donuts ont étés retrouvés, score = score d'Homer)
    """

    game = LaunchGame(agent_interface, game_map, initial_position, probasDirectory, graphics, wait)
    instance_output = game.fetchOutput()
    return instance_output



def Homer_VS_Donuts(agent_type, agent_params, nb_episodes, graphics = True, wait = True):
    """
    Permet de lancer plusieurs parties du jeu à la suite.
    :param agent_type: le type de l'agent (permet de déterminer quel algo utiliser)
    :param agent_params: Permet d'utiliser des paramètres lorsque l'algo de l'agent en nécessite
    :param nb_episodes: le nombre de parties du jeu à lancer
    :param graphics: Permet de lancer le jeu avec ou sans le rendu graphique
    :param wait: Force un temps d'attente entre chaque sélection d'action
    """
    print('\n\n     ========================= Homer_VS_Donuts =========================\n')
    print('     Aide Homer à chercher les donuts en évitant les ennemis! ')
    print('     Nombre de parties: ', nb_episodes)

    #1) ========  Initialisation de l'environnement par défaut & de l'agent
    #*******************************************************************************
    Outputs = []  # list of outputs
    Scores = []  # list of scores

    game_map = [
                         ['', '', '', '', 'enemy', 'multidonuts', '', ''],
                         # ['donut', '', '', '', 'enemy', 'multidonuts', '', ''],
                         ['', '', '', 'enemy', '', '', '', ''],
                         ['', '', 'enemy', '', '', '', 'enemy', ''],
                         # ['', '', '', '', 'enemy', '', '', ''],
                         ['', '', '', '', '', 'enemy', '', ''],
                         ['Homer', '', '', '', '', 'enemy', '', '']
               ]
    available_actions = ['up', 'down', 'left', 'right']
    initial_position = [4,0] # corresponds au spot 'Homer'

    #======= Initialisation des probabilités de transition (probabilité pour Homer de se tromper):
    # /!\ Varie entre chaque exécution du code, mais pas entre chaque partie lors d'une même exécution
    probasDirectory = {}
    for line in range(len(game_map)):
        for column in range(len(game_map[line])):
            spot_id = str(line)+'_'+str(column)
            probasDirectory[spot_id] = {}
            for action in available_actions:
                probas = np.random.rand(4)
                probas = probas / np.sum(probas)
                i  = np.argmax(probas)
                probas[i] += 0.5 # permet d'assurer que la probabilité de prendre la bonne action est >= 0.5
                probas = list(probas / np.sum(probas))
                probasDirectory[spot_id][action] = {}
                probasDirectory[spot_id][action][action] = max(probas)
                probas.remove(max(probas))
                for x in available_actions:
                    if x != action:
                        proba = random.choice(probas)
                        probasDirectory[spot_id][action][x] = proba
                        probas.remove(proba)


    agent_interface = AgentInterface(agent_type, agent_params) # permet de créer l'agent à travers la classe AgentInterface
    #*******************************************************************************

    #2) ========  Jouer les parties du jeu
    #*******************************************************************************
    for episode in range(nb_episodes) :
        output, score = Homer_VS_Donuts_instance(agent_interface, game_map, initial_position, probasDirectory, graphics, wait)
        Outputs.append(output)
        Scores.append(score)
    #*******************************************************************************


    #3) ========  Affichage du résultat
    #*******************************************************************************
    print('\n\n       EPISODES OUTPUTS: ')
    print(Outputs)
    print('\n       EPISODES SCORES: ')
    print(Scores)
    #*******************************************************************************


if __name__ =='__main__':
    """
    le code d'exécution.
    /!\ mettre graphics = False avec agent_type = 'human' semble faire un bug...
    """
    # possible de mettre les paramètres de lancement du jeu directement ici
    # # agent_type = 'random'
    # agent_type = 'human'
    # nb_episodes = 2
    # graphics, wait = True,  True
    # # graphics, wait = False,  True
    # # graphics, wait = False,  False

    # possible aussi de les récupérer dans la console
    options = manage_arguments()
    agent_type, nb_episodes, graphics, wait_ = options.agent_type, options.nb_episodes, options.graphics, options.wait_

    # convert to boolean
    if graphics == 'True':
        graphics = True
    else:
        graphics = False

    if wait_ == 'True':
        wait_ = True
    else:
        wait_ = False

    # agent params for future algorithms
    agent_params = {}

    # launch episodes
    Homer_VS_Donuts(agent_type, agent_params, nb_episodes, graphics, wait_)
