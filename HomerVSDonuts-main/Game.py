import pygame as py
import random
import os
import copy

# random.seed(0) # pourra être utile pour la répétition des résultats


class LaunchGame():
    def __init__(self, agentInterface, game_map, initial_position, probasDirectory, graphics = True, wait_ = True):
        """
        Ici, __init__ est utilisé pour le déroulement entier de la partie.
        :param agentInterface: L'interface déjà créée avec l'agent
        :param game_map: Le plateau initial
        :param initial_position: La position initiale de Homer sur le plateau
        :param probasDirectory: Le dictionnaire des probabilités de se tromper de déplacement
        :param graphics: Permet de lancer le jeu avec ou sans le rendu graphique
        :param wait: Force un temps d'attente entre chaque sélection d'action
        """
        print("\n\n=== Nouvelle partie ===")

        # ********************** Récupération des paramètres
        self.game_map = copy.deepcopy(game_map) # Ici, self.game_map sert d'abord à l'initialisation, puis au display sur la console.
        # note: en utilisant "deepcopy", on est sûr de ne pas altérer l'objet python game_map créé dans main.py (car self.game_map est une copie)

        self.output = False #sera mis à True si victoire
        self.probasDir = probasDirectory
        self.initialPosition = initial_position

        #********************** Données & fonctions utiles pour la représentation graphique avec pygame
        largeur = 1500
        longueur = 1000
        FPS = 12
        spot_size = 150
        Spots_col = len(game_map[0])
        Spots_line = len(game_map)
        player_size = 130

        # define colors
        WHITE = (255, 255, 255)
        # GREY = (200, 200, 200)
        GREY = (220, 220, 220)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        VIOLET = (255, 0, 255)
        LightYELLOW = (255, 255, 100)
        LightBrown = (220, 220, 150)

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, "img")

        font_name = py.font.match_font('arial')

        def draw_text(surf, text, size, x, y, color=BLACK):
            """
            Petite fonction pour la représentation graphique avec pygame
            :param surf: surface sur laquelle écrire
            :param text: texte à écrire
            :param size: taille de police
            :param x: coordonnée x de l'emplacement du texte
            :param y: coordonnée y de l'emplacement du texte
            :param color: couleur du texte
            """
            font = py.font.Font(font_name, size)
            text_surface = font.render(text, True, color)  # white for color true for anti aliased
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)  # le text surface est sur le text rectangle


        #********************** Classes définissant les différents types d'éléments ('sprites') possibles sur le plateau

        #======> Personnage principal
        class Homer(py.sprite.Sprite):
            """
            Cette classe régule l'emplacement / les caractéristiques d'Homer avec Pygame
            """
            # sprite for the Player
            def __init__(self, player_size, agentInterface, probasDir, game_map):
                """
                :param player_size: la taille de l'image d'Homer dans la représentation graphique
                :param agentInterface:  L'interface déjà créée avec l'agent
                :param probasDir: Le dictionnaire des probabilités de se tromper de déplacement
                :param game_map: Le plateau initial
                """
                py.sprite.Sprite.__init__(self)

                self.nb_steps = 0 # défini le nombre d'actions déjà prises par Homer. C'est aussi un compteur pour mettre fin au jeu
                self.game_map = game_map # le plateau mis à jour au cours de la partie
                self.probasDir = probasDir
                self.agentInterface = agentInterface

                # éléments de représentation graphique
                self.image = homer  # image
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (player_size, 4*player_size//3))
                self.rect = self.image.get_rect()
                self.rect.center = (longueur // 2, largeur // 2)

                # permet de détecter les cases voisines sur lesquelles il est possible de se déplacer
                self.current_spot_neighbors = []
                self.score = 1 # score initial

                # les coordonnées initiales d'Homer (sera initialisé juste après par "self.Initialize"
                self.line = -1
                self.col = -1 #has to be initialized

                # Display initial dans la console
                print("\nPlateau initial: ")
                initial_action, stochastic_action = '',''
                self.displayOnConsole(initial_action, stochastic_action, self.game_map, initial=True)

            def makeActionWithStochasticError(self, agent_initial_choice):
                """
                Permet de simuler les "erreurs" faites par Homer
                :param agent_initial_choice: le choix initial fait par l'agent
                :return: le choix erroné (ou non avec une probabilité >= 0.5)
                """
                actions = [ a for a in self.probasDir[str(self.line)+'_'+str(self.col)][agent_initial_choice]] # revient au même que ['up', 'down', 'left', 'right']
                # actions_probas : récupère les probabilités du dictionnaire pour cette configuration précise de case du plateau / action choisie par l'agent
                actions_probas = [ self.probasDir[str(self.line)+'_'+str(self.col)][agent_initial_choice][a] for a in self.probasDir[str(self.line)+'_'+str(self.col)][agent_initial_choice]]

                # random.choices permet de sélectionner au hasard dans une liste selon la loi de probabilité définie dans weights
                choice_with_error = random.choices(actions, weights=actions_probas)[0] # [0] car random.choices(actions, weights=actions_probas) retournait une liste de taille 1

                return choice_with_error # choice_with_error = agent_initial_choice avec une probabilité >= 0.5

            def displayOnConsole(self, initial_action, stochastic_action, game_map, initial = False):
                """
                Display dans la console
                :param initial_action: l'action non erronée initialement choisie par l'agent/l'algorithme/ l'humain
                :param stochastic_action: l'action erronée avec une certaine probabilité, et celle qui est utilisée pour de vrai
                :param game_map: la liste des cases mises à jour du plateau
                :param initial: indique si game_map correspond au plateau initial (début de partie) ou non
                """
                if not initial:
                    print('\n====> initial action choice: ',initial_action, ', stochastic action (with error): ',stochastic_action, ', score: ', self.score )
                print('***********************')
                for line in game_map:
                    print(line)
                print('***********************')

            def update(self):
                """
                Fait sélectionner à l'agent une action. Dans le cas 'human', attends que l'humain appuie sur une touche du clavier
                """
                initial_choice = ''
                if agentInterface.agent_type != 'human':
                    coordinates = (self.line)*(Spots_col) + self.col
                    self.agentInterface.selectAction(coordinates)
                    initial_choice = self.agentInterface.choice # le choix initial non erroné en ce début de tour

                elif agentInterface.agent_type == 'human':
                    keystate = py.key.get_pressed()

                    if keystate[py.K_UP]:
                        initial_choice = 'up' # le choix initial non erroné en ce début de tour
                    if keystate[py.K_DOWN]:
                        initial_choice = 'down' # le choix initial non erroné en ce début de tour
                    if keystate[py.K_LEFT]:
                        initial_choice = 'left' # le choix initial non erroné en ce début de tour
                    if keystate[py.K_RIGHT]:
                        initial_choice = 'right' # le choix initial non erroné en ce début de tour

                if initial_choice != '': # l'humain a appuyé sur une touche du clavier, ou l'agent a sélectionné une action

                    stochasticChoice = self.makeActionWithStochasticError(initial_choice) # le choix appliqué sera erroné selon ce processus, avec une probabilité <= 0.5

                    # application du choix erroné sur l'environnement de jeu
                    if stochasticChoice == 'up':
                        if self.current_spot_neighbors[0] != None:
                            self.Move_to(self.current_spot_neighbors[0])
                    if stochasticChoice == 'down':
                        if self.current_spot_neighbors[1] != None:
                            self.Move_to(self.current_spot_neighbors[1])
                    if stochasticChoice == 'left':
                        if self.current_spot_neighbors[2] != None:
                            self.Move_to(self.current_spot_neighbors[2])
                    if stochasticChoice == 'right':
                        if self.current_spot_neighbors[3] != None:
                            self.Move_to(self.current_spot_neighbors[3])

                    # Draw/render
                    #version console (pas graphique)
                    self.displayOnConsole(initial_choice, stochasticChoice, self.game_map)
                    self.nb_steps += 1

            def Initialize(self, objects, line, column):
                """
                Initialisation de l'emplacement d'Homer
                :param objects: la liste des objets (sprites) du plateau
                :param line: la ligne initiale
                :param column: la colonne initiale
                """
                self.line = line
                self.column = column
                self.Move_to(objects[line][column]) # /!\ the initial position has to be well chosen!


            def Move_to(self, spot):
                """
                Permet de déplacer Homer sur une nouvelle case
                :param spot: la nouvelle case
                """
                self.game_map[self.line][self.col] = ''# free space again as Homer moves (for console representation only)
                self.rect.center = spot.rect.center # centre du spot (pour la représentation graphique)
                self.current_spot_neighbors = spot.neighbors # mets à jour les cases voisines d'Homer, comme étant les cases voisines de la nouvelle case
                self.score += spot.reward # mise à jour du score
                # mise à jour des nouvelles coordonnées d'Homer (sur le nouveau spot)
                self.line = spot.line
                self.col = spot.col
                self.game_map[self.line][self.col] = 'Homer' #(for console representation only)
                if spot.type == 'donut' or spot.type == 'multidonuts':
                    spot.meet() # le donut est ramassé, il doit être supprimé




        # ======> Autres types de case possibles
        class Empty_spot(py.sprite.Sprite):
            """
            Case vide
            """
            def __init__(self, spot_size, spot_center,i,j):
                """
                :param spot_size: taille du carré
                :param spot_center: emplacement central du carré de la représentation graphique de la case
                :param i: la ligne de la case
                :param j: la colonne de la case
                """
                py.sprite.Sprite.__init__(self) # fait appel au framework pygame

                # éléments graphiques pour pygame
                spot_size = 2 * spot_size // 3
                self.image = py.Surface((spot_size, spot_size))
                # self.image.fill(LightYELLOW)
                self.image.fill(GREY)
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (spot_size, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center

                self.type = 'empty_spot' # type de la case
                self.reward = -1
                self.neighbors = []  # only up / down / right /left, sera initialisé après
                self.line = i #la ligne
                self.col = j # la colonne de la case

            # def surrounded_by_enemies(self): # pas utile pour le moment
            #     answer = True
            #     for x in self.neighbors:
            #         if x != None:
            #             if x.type != 'enemy':
            #                 answer = False
            #     return answer


        class Donut(py.sprite.Sprite):
            """
            Classe Donut
            """
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)

                # éléments graphiques
                self.height = spot_size  # générer des hauteurs différentes
                self.image = donut
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (3 * spot_size // 4, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center

                self.type = 'donut'
                self.reward = 50
                self.neighbors = []  # only up / down / right /left, initialisé après
                self.line = i
                self.col = j

            def meet(self):
                self.reward = -1 # change la récompense pour revenir à une case vide
                self.kill() # permet de supprimer le donut et sa récompense de la carte après récupération

        class Multidonuts(py.sprite.Sprite):
            """
            Classe multidonuts. Comme donuts, mais récompense + grande
            """
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)

                self.height = spot_size  # générer des hauteurs différentes
                self.image = multidonuts
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (spot_size, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center

                self.type = 'multidonuts'
                self.reward = 100
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j

            def meet(self):
                self.reward = -1 # change la récompense pour revenir à une case vide
                self.kill() # supprime le donuts de la représentation graphique

        class enemy(py.sprite.Sprite):
            """
            Les ennemis à éviter
            """
            def __init__(self, spot_size, spot_center,i,j):
                py.sprite.Sprite.__init__(self)

                # éléments graphiques
                self.height = spot_size  # générer des hauteurs différentes
                self.image = enemies[random.choice(enemies_list)]
                self.rect = self.image.get_rect()
                self.image = py.transform.scale(self.image, (2*spot_size//3, spot_size))
                self.rect = self.image.get_rect()
                self.rect.center = spot_center


                self.type = 'enemy'
                # dans les 2 cas de récompense, provoque la fin du jeu pour l'instant
                # self.reward = -math.inf
                self.reward = -500
                self.neighbors = []  # only up / down / right /left
                self.line = i
                self.col = j



        #********************** Fonctions additionnelles utiles pour le déroulement du jeu

        def Spot_Choice(i, j, game_map): # deterministic
            """
            Initialisation de la case i,j du tableau du jeu avec pygame, grâce aux infos initiales de game_map
            :param i: la ligne de la case
            :param j: la colonne de la case
            :param game_map: le tableau initial à reconstituer
            :return: la case
            """
            if game_map[i][j] == 'enemy' :
                spot = enemy(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i, j)
            elif game_map[i][j] == 'multidonuts' :
                spot = Multidonuts(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i, j)
            elif game_map[i][j] == 'donut':
                spot = Donut(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i, j)
            else: # '' ou Homer
                spot = Empty_spot(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i, j)

            return spot



        def Construct_neighbors(objects):
            """
            Permet d'initialiser la liste des voisins pour toutes les cases contenues dans objects
            :param objects: la liste des cases du jeu
            :return:
            """
            for i in range(len(objects)):
                for j in range(len(objects[0])):
                    obj = objects[i][j]
                    if i == 0:
                        obj.neighbors.append(None)
                    elif i != 0:
                        obj.neighbors.append(objects[i - 1][j])  # up
                    if i == Spots_line - 1:
                        obj.neighbors.append(None)
                    elif i != Spots_line - 1:
                        obj.neighbors.append(objects[i + 1][j])  # down

                    if j == 0:
                        obj.neighbors.append(None)
                    elif j != 0:
                        obj.neighbors.append(objects[i][j - 1])  # up
                    if j == Spots_col - 1:
                        obj.neighbors.append(None)
                    elif j != Spots_col - 1:
                        obj.neighbors.append(objects[i][j + 1])  # down

        def still_donuts_in_board(obj_sprite):  # is the game resolved ?
            """
            Permet de vérifier si le jeu est fini (récupération de touts les donuts)
            :param obj_sprite: la liste des cases
            :return:
            """
            answer = False
            for obj in obj_sprites:
                if obj.type == 'donut' or obj.type == 'multidonuts':
                    answer = True
            return answer



        #********************** initialize pygame and create window

        py.init()

        if graphics == True:
            screen = py.display.set_mode((largeur, longueur))
            py.display.set_caption("HOMER_VS_DONUTS")
        clock = py.time.Clock()  # pour contrôler nos FPS (frame per second)

        if graphics == True:
            background = py.image.load(os.path.join(img_folder, "officialbackground.jpg")).convert()
            background = py.transform.scale(background, (largeur, longueur))
            background_rect = background.get_rect()  # pour le background


        #charger les images des cases pour la représenation graphique
        multidonuts = py.image.load(os.path.join(img_folder, "multidonuts.png"))
        donut = py.image.load(os.path.join(img_folder, "donut.png"))
        burns = py.image.load(os.path.join(img_folder, "burns.png"))
        krusty = py.image.load(os.path.join(img_folder, "krusty.png"))
        maggie = py.image.load(os.path.join(img_folder, "maggie.png"))
        bart = py.image.load(os.path.join(img_folder, "bart.png"))
        lisa = py.image.load(os.path.join(img_folder, "lisa.png"))
        marge = py.image.load(os.path.join(img_folder, "marge.png"))
        enemies_list = ['burns', 'krusty', 'maggie', 'bart', 'lisa', 'marge']
        enemies = {'burns': burns, 'krusty':krusty, 'maggie':maggie, 'bart':bart, 'lisa':lisa, 'marge':marge}
        homer = py.image.load(os.path.join(img_folder, "homer.png"))


        # Création des groupes de sprites qui seront gérés par pygame
        obj_sprites = py.sprite.Group()
        spots_sprites = py.sprite.Group()
        homer_sprite = py.sprite.Group() # groupe juste pour Homer
        all_sprites = py.sprite.Group() # groupe pour tous les sprites

        player = Homer(player_size, agentInterface, self.probasDir, self.game_map)
        homer_sprite.add(player)

        all_sprites.add(player)

        Objects = [] # garde aussi les sprites (pas groupe pygame, juste une liste)

        for i in range(Spots_line):
            Objects_row = []
            for j in range(Spots_col):
                obj = Spot_Choice(i, j, self.game_map) # initialisation de la case grâce à l'info contenue dans game_map
                spot = Empty_spot(spot_size, (((j + 2) * spot_size, (i + 2) * spot_size)), i,j)
                Objects_row.append(obj)
                spots_sprites.add(spot)
                obj_sprites.add(obj)
                all_sprites.add(obj)
                all_sprites.add(spot)
            Objects.append(Objects_row)

        Construct_neighbors(Objects) # permet à chaque case  de garder en mémoire ses cases voisines
        player.Initialize(Objects, self.initialPosition[0], self.initialPosition[1]) # initialisation de Homer à la bonne position




        #********************** Boucle temporelle du jeu


        running = True
        NotfirstLoop = False
        if wait_ : # permet de "freeze" le jeu avant de le débuter
            py.time.wait(70)
            # py.time.wait(100)
            # py.time.wait(300)

        while running: # la boucle de jeu
            clock.tick(FPS) # avancement temporel

            if wait_: # permet de "freeze" le jeu avant de reprendre une action
                # py.time.wait(100)
                py.time.wait(70)
                # py.time.wait(300)


            # Process input (events), like keyboard action
            for event in py.event.get():
                # Check for closing window
                if event.type == py.QUIT:
                    running = False

            # Update
            if NotfirstLoop :
                all_sprites.update() # version pygame pour mettre à jour tous les objets du jeu

            # if player.score <= -20:  # met a enemy / exhaustion
            if player.score <= -30 or player.nb_steps >= 30:  # met a enemy / exhaustion
                running = False # arrêt de la boucle temporelle de la partie

            if not still_donuts_in_board(obj_sprites): # tous les donnuts ont été récupérés
                self.output = True # we won !
                running = False # arrêt de la boucle temporelle de la partie


            # Draw/render
            # version graphique
            if graphics == True:
                screen.fill(LightBrown)
                screen.blit(background, background_rect)
                spots_sprites.draw(screen)
                obj_sprites.draw(screen)
                homer_sprite.draw(screen)
                draw_text(screen, "SCORE :" + str(player.score), 50, largeur // 2, 100, RED)  # 50 = la taille
                draw_text(screen, "EAT DONUTS & AVOID ENEMIES!", 70, largeur // 2, 10, RED)  # 18 est pour la taille
                # *after* drawing everything, flip the display
                py.display.flip()  # permet de passer du background qu'on ne redraw pas à chaque fois au foreground
            NotfirstLoop = True

            if not running:
                if wait_:
                    py.time.wait(500) # bloquer le jeu à la fin de la partie pour 500 ms

            self.score = player.score # garder en mémoire de la partie le score d'Homer

        py.quit() # fin de l'utilisation de pygame



    def fetchOutput(self):
        """
        Après une session '__init__' du jeu, cette fonction permet de récupérer les résultats du jeu
        :return: output = tous les donuts ont été récupérés? score = score de Homer
        """
        return self.output, self.score

