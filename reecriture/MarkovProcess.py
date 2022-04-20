import numpy as np


class Grid:
	def __init__(self, size, win_states, lose_states, obstacle_states,action = ["up", "down", "left", "right"]):
		self.size_board = size #tuple
		self.win_states = win_states
		self.lose_states= lose_states
		self.obstacle_states = obstacle_states
		#self.homer_success_rate = homer_success_rate
		self.action = action
		self.probas = self.create_probas(self.action)


	def create_probas(self,action):
		#======= Initialisation des probabilités de transition (probabilité pour Homer de se tromper):
		# /!\ Varie entre chaque exécution du code, mais pas entre chaque partie lors d'une même exécution
		probasDirectory = {}
		for line in range(self.size[0]):
			for column in range(self.size[1]):
				spot_id = str(line)+'_'+str(column)
				probasDirectory[spot_id] = {}
				for action in self.action:
					probas = np.random.rand(len(self.action))
					probas = probas / np.sum(probas)
					i  = np.argmax(probas)
					probas[i] += 0.5 # permet d'assurer que la probabilité de prendre la bonne action est >= 0.5
					probas = list(probas / np.sum(probas))
					probasDirectory[spot_id][action] = {}
					probasDirectory[spot_id][action][action] = max(probas)
					probas.remove(max(probas))
					for x in self.action:
						if x != action:
							proba = np.random.choice(probas)
							probasDirectory[spot_id][action][x] = proba
							probas.remove(proba)
			return probasDirectory

	def get_reward(self, current_state):
		if current_state in self.win_states:
			return 100
		elif current_state in self.lose_states:
			return -100
		else:
			return -1

	def is_end(self, current_state):
		if (current_state in self.win_states) or (current_state in self.lose_states):
			return True
		return False

	def homer_action(self, current_state, action):
		if action == "up":
			actions_probas = [self.probas[str(current_state[0])+'_'+str(current_state[1])]["up"][a] for a in self.probas[str(current_state[0])+'_'+str(current_state[1])]["up"]]
			return np.random.choice(self.action, p=actions_probas)
		if action == "down":
			actions_probas = [self.probas[str(current_state[0])+'_'+str(current_state[1])]["down"][a] for a in self.probas[str(current_state[0])+'_'+str(current_state[1])]["down"]]
			return np.random.choice(self.action, p=actions_probas)
		if action == "left":
			actions_probas = [self.probas[str(current_state[0])+'_'+str(current_state[1])]["left"][a] for a in self.probas[str(current_state[0])+'_'+str(current_state[1])]["left"]]
			return np.random.choice(self.action, p=actions_probas)
		if action == "right":
			actions_probas = [self.probas[str(current_state[0])+'_'+str(current_state[1])]["right"][a] for a in self.probas[str(current_state[0])+'_'+str(current_state[1])]["right"]]
			return np.random.choice(self.action, p=actions_probas)
		else:
			raise Exception("fct homer_action did not get a correct parameter :",action)

	def get_next_state(self, current_state, action):
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
	def __init__(self, starting_state, grid):
		self.starting_state = starting_state
		self.current_state = starting_state
		self.history_states = []
		self.grid = grid
		self.actions = ["up", "down", "left", "right"]
		self.lr = 0.1
		self.exploration_rate = 0.3
		self.decay_gamma = 0.9
		self.Q_values = {}
		for i in range(self.grid.size_board[0]):
			for j in range(self.grid.size_board[1]):
				self.Q_values[(i, j)] = {}
				for a in self.actions:
					self.Q_values[(i, j)][a] = 0
					if i == 0: #si on est au bord, on met une proba extreme pour ne pas qu'il choisisse cette action
						self.Q_values[(i, j)]["left"] = -1e6
					if i == self.grid.size_board[0]-1:
						self.Q_values[(i, j)]["right"] = -1e6
					if j == 0:
						self.Q_values[(i, j)]["up"] = -1e6
					if j == self.grid.size_board[1]-1:
						self.Q_values[(i, j)]["down"] = -1e6

	def select_action(self, exploitation = False):
		action = ""
		if np.random.uniform(0,1) > self.exploration_rate or exploitation: # exploitation
			max_next_reward = -100
			for a in self.actions:
				next_reward = self.Q_values[self.current_state][a]
				if next_reward >= max_next_reward:
					action = a
					max_next_reward = next_reward

		if action == "": # exploration or no best choice
			action = np.random.choice(self.actions)

		return action

	def get_max_Q(self,state):
		if self.grid.is_end(state):
			return self.grid.get_reward(state)
		max_Q = -1
		for a in self.actions:
			if self.Q_values[state][a] > max_Q :
				max_Q = self.Q_values[state][a]
		return max_Q

	def play_to_win(self):
		action = self.select_action(exploitation=True)
		self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
		print(f"You chose {action}, Homer did {homer_decision}")
		if self.grid.is_end(self.current_state):
			self.current_state = self.starting_state


	def play_to_learn_step(self):
		if not self.grid.is_end(self.current_state):
			action = self.select_action()
			self.history_states.append([self.current_state, action])
			self.current_state,homer_decision = self.grid.get_next_state(self.current_state, action)
			self.history_states[-1].append(self.grid.get_reward(self.current_state))
			print(f"You chose {action}, Homer did {homer_decision}")
		else:
			reward = 0
			previous_state = self.current_state
			for history_state in reversed(self.history_states):
				state = history_state[0]
				action = history_state[1]
				new_reward = history_state[2]
				print(state,action,self.get_max_Q(previous_state))
				print(self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state) - self.Q_values[state][action]))
				self.Q_values[state][action] += self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state) - self.Q_values[state][action])
				previous_state = state

			self.current_state = self.starting_state
			self.history_states = []
		
	def play_to_learn(self):
		self.current_state = self.starting_state
		self.history_states = []
		over = False
		while not over:	
			if not self.grid.is_end(self.current_state):
				action = self.select_action()
				self.history_states.append([self.current_state, action])
				self.current_state, homer_decision = self.grid.get_next_state(self.current_state, action)
				self.history_states[-1].append(self.grid.get_reward(self.current_state))
			else:
				reward = 0
				previous_state = self.current_state
				for history_state in reversed(self.history_states):
					state = history_state[0]
					action = history_state[1]
					new_reward = history_state[2]
					self.Q_values[state][action] += self.lr*( new_reward + self.decay_gamma*self.get_max_Q(previous_state) - self.Q_values[state][action])
					previous_state = state
				over = True
		self.current_state = self.starting_state
		self.history_states = []

	def play_to_learn_step2(self):
		action = self.select_action()
		previous_state = self.current_state
		self.current_state,homer_decision = self.grid.get_next_state(self.current_state, action)
		reward = self.grid.get_reward(self.current_state)
		self.Q_values[previous_state][action] += self.lr*( reward + self.decay_gamma*self.get_max_Q(self.current_state) - self.Q_values[previous_state][action])
		print(f"You chose {action}, Homer did {homer_decision}")
		if self.grid.is_end(self.current_state):
			self.current_state = self.starting_state