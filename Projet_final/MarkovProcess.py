import numpy as np


class Grid:
	def __init__(self, size, win_states, lose_states, obstacle_states, probasDirectory,reward):
		self.size_board = size #tuple
		self.win_states = win_states
		self.lose_states= lose_states
		self.obstacle_states = obstacle_states
		#self.homer_success_rate = homer_success_rate
		self.action = ["up", "down", "left", "right"]
		self.probas = probasDirectory
		self.reward = reward

	def get_reward(self, current_state):
		'''retourne le score à ajouter à celui de l'agent'''
		if current_state in self.win_states:
			return 100
		elif current_state in self.lose_states:
			return -100
		else:
			return -1

	def is_end(self, current_state,reward):
		''' Fonction qui vérifie si la partie est finie :
		si l'agent est sur les donnuts ou si il a touché des ennemis ou si le score est inférieur à -30''' 
		if (current_state in self.win_states) or (current_state in self.lose_states) or (reward <= -30):
			return True
		return False

	def is_win_state(self, current_state):
		'''Fonction qui vérifie si l'agent a gagné'''
		if current_state in self.win_states:
			return True
		return False

	def homer_action(self, current_state, action):
		'''Fonction qui détermine l'action de l'agent en fonction :
  		- de la position de l'agent
    	- des actions possibles
     	- des probabilités de succès'''
		if action == "up":
			actions_probas = [self.probas[str(current_state[1])+'_'+str(current_state[0])]["up"][a] for a in self.action]
			return np.random.choice(self.action, p=actions_probas)
		if action == "down":
			actions_probas = [self.probas[str(current_state[1])+'_'+str(current_state[0])]["down"][a] for a in self.action]
			return np.random.choice(self.action, p=actions_probas)
		if action == "left":
			actions_probas = [self.probas[str(current_state[1])+'_'+str(current_state[0])]["left"][a] for a in self.action]
			return np.random.choice(self.action, p=actions_probas)
		if action == "right":
			actions_probas = [self.probas[str(current_state[1])+'_'+str(current_state[0])]["right"][a] for a in self.action]
			return np.random.choice(self.action, p=actions_probas)
		else:
			raise Exception("fct homer_action did not get a correct parameter :",action)

	def get_next_state(self, current_state, action):
		'''Fonction qui détermine le prochain état de l'agent'''
		homer_decision = self.homer_action(current_state, action)
		if (homer_decision == "up"):
			next_state = (current_state[0], current_state[1] - 1)
		elif (homer_decision == "down"):
			next_state = (current_state[0], current_state[1] + 1)
		elif (homer_decision == "left"):
			next_state = (current_state[0]-1, current_state[1])
		elif (homer_decision == "right"):
			next_state = (current_state[0]+1, current_state[1])
		else:
			next_state = current_state

		if (next_state[0] >= 0) and (next_state[0] < self.size_board[0]):
			if (next_state[1] >= 0) and (next_state[1] < self.size_board[1]):
				if next_state not in self.obstacle_states:
					return next_state, homer_decision
		return current_state, homer_decision


class Agent:
	def __init__(self, starting_state, grid,reward):
		self.starting_state = starting_state
		self.current_state = starting_state
		self.history_states = []
		self.grid = grid
		self.actions = ["up", "down", "left", "right"]
		self.lr = 0.1
		self.exploration_rate = 0.3
		self.decay_gamma = 0.9
		self.reward = reward
		self.reward_history = reward #permet de récupérer le dernier score obtenu
		self.Q_values = {}
		self.nb_victories = 0
		for i in range(self.grid.size_board[0]):
			for j in range(self.grid.size_board[1]):
				self.Q_values[(i, j)] = {}
				for a in self.actions:
					self.Q_values[(i, j)][a] = 0

	def select_action(self, exploitation = False, softmax = False): #voir softmax
		'''Sélection de l'action à effectuer'''
		action = ""
		#si on exploite les résultats précédents :
		if np.random.uniform(0,1) > self.exploration_rate or exploitation:
			max_next_reward = -100
			for a in self.actions: # On choisit la plus grande Q-value parmi les 4 de la position actuelle
				next_reward = self.Q_values[self.current_state][a]
				if next_reward >= max_next_reward:
					action = a
					max_next_reward = next_reward
		if softmax:
			action = self.softmax(self.current_state)
		#sinon on choisit unce action aléatoire
		if action == "": # exploration or no best choice
			action = np.random.choice(self.actions)  # avec proba égale à softmax de toutes les Qvalues

		return action

	def get_max_Q(self,state,reward):
		'''Retourne la Q-value maximale de la position actuelle'''
		if self.grid.is_end(state,reward):
			return self.grid.get_reward(state)
		max_Q = -1
		for a in self.actions:
			if self.Q_values[state][a] > max_Q :
				max_Q = self.Q_values[state][a]
		return max_Q

	def softmax(self, state):        
		return np.random.choice(self.actions, weights = self.Q_values[state])

	def play_to_win(self):
		'''Joue à la recherche de la victoire en exploitant les résultats obtenus.
    	Joue case par case, requiert un input de la part de l'utilisateur pour continuer
     	/!\ à n'utiliser que si on a déjà fait apprendre à l'agent'''
		action = self.select_action(exploitation=True)
		self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
		#permet de savoir si on a fait l'action demandée ou pas
		print(f"You chose {action}, Homer did {homer_decision}")
		self.reward += self.grid.get_reward(self.current_state)
		if self.grid.is_end(self.current_state,self.reward):
			self.current_state = self.starting_state
			self.reward = 0
 
	def play_to_learn_step(self):
		'''Exploration aléatoire par l'agent pour calculer les Q-values
  		Joue case par case, requiert un input de la part de l'utilisateur pour continuer'''
		if not self.grid.is_end(self.current_state,self.reward):
			action = self.select_action()
			self.history_states.append([self.current_state, action]) # On ajoue dans une liste une liste contenant : [position, action prise]
			self.current_state,homer_decision = self.grid.get_next_state(self.current_state, action)
			self.history_states[-1].append(self.grid.get_reward(self.current_state)) # On ajoue dans la liste la récompense reçue
			print(f"You chose {action}, Homer did {homer_decision}")
			self.reward = self.reward + self.grid.get_reward(self.current_state)
			self.reward_history = self.reward
		else: #Homer est soit sur un ennemi, soit sur un donut
			# print("REWARD OF THIS GAME = ")
			# print(self.reward)
			self.reward = 0
			reward = 0
			previous_state = self.current_state
			for history_state in reversed(self.history_states): # on parcourt le chemin en partant de la fin 
				state = history_state[0]
				action = history_state[1]
				new_reward = history_state[2]
				print(state,action,self.get_max_Q(previous_state,reward))
				print(self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state,reward) - self.Q_values[state][action]))
				self.Q_values[state][action] += self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state,reward) - self.Q_values[state][action])
				previous_state = state

			self.current_state = self.starting_state
			self.history_states = []
		
	def play_to_learn(self):
		'''Exploration aléatoire par l'agent pour calculer les Q-values
  		Joue une partie par une partie, ne requiert pas d'input'''
		self.current_state = self.starting_state
		self.history_states = [] # on initilise une liste 
		over = False
		while not over:	
			if not self.grid.is_end(self.current_state,self.reward): # si la partie n'est pas finie
				action = self.select_action()
				self.history_states.append([self.current_state, action])
				self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
				self.history_states[-1].append(self.grid.get_reward(self.current_state))
				self.reward = self.reward + self.grid.get_reward(self.current_state)
			else: #Homer est soit sur un ennemi, soit sur un donut
				# print("REWARD OF THIS GAME = ")
				# print(self.reward)
				self.reward = 0
				reward = 0
				previous_state = self.current_state
				for history_state in reversed(self.history_states): # on parcourt le chemin en partant de la fin...
					state = history_state[0]
					action = history_state[1]
					new_reward = history_state[2]
					# ...et on met à jour les Q-values
					self.Q_values[state][action] += self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state,reward) - self.Q_values[state][action])
					previous_state = state
				over = True
		self.current_state = self.starting_state
		self.history_states = []
  
	def play_to_learn_test(self):
		'''Joue une partie par une partie, ne requiert pas d'input
  		permet de calculer le nombre de victoires'''
		self.current_state = self.starting_state
		over = False
		while not over:	
			if not self.grid.is_end(self.current_state,self.reward): # si la partie n'est pas finie
				action = self.select_action(exploitation=True)
				self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
				#permet de savoir si on a fait l'action demandée ou pas
				# print(f"You chose {action}, Homer did {homer_decision}")
				self.reward += self.grid.get_reward(self.current_state)
			else: #Homer est soit sur un ennemi, soit sur un donut
				self.reward = 0
				reward = 0
				over = True
			if self.grid.is_win_state(self.current_state):
				self.nb_victories += 1
		self.current_state = self.starting_state


	def play_to_win_test(self):
		'''Joue à la recherche de la victoire en exploitant les résultats obtenus.
		Joue case par case, requiert un input de la part de l'utilisateur pour continuer
		/!\ à n'utiliser que si on a déjà fait apprendre à l'agent'''
		over = False
		while not over:
			action = self.select_action(exploitation=True)
			self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
			#permet de savoir si on a fait l'action demandée ou pas
			# print(f"You chose {action}, Homer did {homer_decision}")
			self.reward += self.grid.get_reward(self.current_state)
			if self.grid.is_end(self.current_state,self.reward):
				if self.grid.is_win_state(self.current_state) == 1:
					self.nb_victories += 1
				self.current_state = self.starting_state
				self.reward = 0
				over = True
 

	def play_to_learn_step2(self):
		'''Exploration aléatoire par l'agent pour calculer les Q-values
		Joue case par case, requiert un input de la part de l'utilisateur pour continuer'''
		action = self.select_action()
		previous_state = self.current_state
		self.current_state,homer_decision = self.grid.get_next_state(self.current_state, action)
		reward = self.grid.get_reward(self.current_state)
		self.Q_values[previous_state][action] += self.lr*( reward + self.decay_gamma*self.get_max_Q(self.current_state,self.reward) - self.Q_values[previous_state][action])
		print(f"You chose {action}, Homer did {homer_decision}")
		self.reward = self.reward + self.grid.get_reward(self.current_state)
		if self.grid.is_end(self.current_state,self.reward): #Homer est soit sur un ennemi, soit sur un donut
			self.current_state = self.starting_state
			# print("REWARD OF THIS GAME = ")
			# print(self.reward)
			self.reward = 0