from husky_ur5 import *
from copy import deepcopy

state = getCurrentState()
print(state)

objects = ['apple', 'orange', 'banana', 'table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
enclosures = ['fridge', 'cupboard', 'box']
actions = ['moveTo', 'pick', 'drop', 'changeState', 'pushTo']

# A checker for action feasibility
def checkAction(state, action):
	if action[0] == 'moveTo':
		return True
	elif action[0] == 'pick':
		return action[1] in state['close'] and action[1] not in ['fridge', 'table', 'table2']
	elif action[0] == 'drop':
		return not (action[0] == action[1] or \
			action[1] not in ['table', 'table2', 'box', 'fridge', 'tray', 'tray2'] or \
			(action[1] in enclosures and state[action[1]] =='Close') or \
			action[1] not in state['close'])
	elif action[0] == 'changeState':
		return not (action[1] not in enclosures or \
			action[1] not in state['close'] or \
			state[action[1]] == action[2])
	elif action[0] == 'pushTo':
		return action[1] in state['close'] and action[1] != action[2]

# An approximate environment model
def changeState(state1, action):
	state = deepcopy(state1)
	if action[0] == 'moveTo':
		state['close'] = [action[1]]
	elif action[0] == 'pick':
		state['grabbed'] = action[1]
	elif action[0] == 'drop':
		obj = state['grabbed']
		state['grabbed'] = ''
		if action[1] in ['box', 'fridge']:
			state['inside'].append((obj, action[1]))
		else:
			state['on'].append((obj, action[1]))
	elif action[0] == 'changeState':
		state['fridge'] = 'Close' if state['fridge'] == 'Open' else 'Open'
	elif action[0] == 'pushTo':
		state['close'] = [action[2]]
	return state

# An approximate goal checker
def checkGoal(state):
	# return ('apple', 'fridge') in state['inside'] and \
	# 	   ('orange', 'fridge') in state['inside'] and \
	# 	   ('banana', 'fridge') in state['inside'] and \
	# 	   state['fridge'] == 'Close'
	return ('banana', 'table') in state['on']

def allNeighbours(node):
	state = node[0]; actionList = node[1]
	neighbours = []
	for aType in ['moveTo', 'pick', 'drop']:
		for obj in objects:
			action = [aType, obj]
			if checkAction(state, action):
				neighbours.append((changeState(state, action), actionList + [action]))
	for newState in ['Open', 'Close']:
		if checkAction(state, ['changeState', 'fridge', newState]):
			neighbours.append((changeState(state, ['changeState', 'fridge', newState]), actionList + [['changeState', 'fridge', newState]]))
	for obj1 in objects:
		for obj2 in objects:
			if checkAction(state, ['pushTo', obj1, obj2]):
				neighbours.append((changeState(state, ['pushTo', obj1, obj2]), actionList + [['pushTo', obj1, obj2]]))
	return neighbours

	

