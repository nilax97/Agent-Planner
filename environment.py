from husky_ur5 import *
from copy import deepcopy

state = getCurrentState()
print(state)

objects = ['apple', 'orange', 'banana', 'table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
enclosures = ['fridge', 'cupboard']
actions = ['moveTo', 'pick', 'drop', 'changeState', 'pushTo']

# A checker for action feasibility
def checkAction(state, action):
	# Check if action is possible for state
	#######################################
	######## Insert your code here ########
	#######################################
	return True

# An approximate environment model
def changeState(state1, action):
	state = deepcopy(state1)
	# Change state based on action
	#######################################
	######## Insert your code here ########
	#######################################
	return state

# An approximate goal checker
def checkGoal(state):
	return ('apple', 'fridge') in state['inside'] and \
		   ('orange', 'fridge') in state['inside'] and \
		   ('banana', 'fridge') in state['inside'] and \
		   state['fridge'] == 'Close'
