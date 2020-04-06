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
	pick_objects = ['apple', 'orange', 'banana', 'box', 'tray', 'tray2']
	surface_objects = ['table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
	state_objects = ['fridge','cupboard']
	
	act = action[0]
	n = len(action)
	obj = action[1]
	if(n==3):
		obj2 = action[2]
		
	if act not in actions or n>3 or n<2:
		return False
	
	if act == actions[0]:
		if(n!=2):
			return False
		if obj in state['close']:
			return False
		if obj not in objects:
			return False
		if obj == state['grabbed']:
			return False
		return True
	
	if act == actions[1]:
		if(n!=2):
			return False
		if obj not in state['close']:
			return False
		if obj not in pick_objects:
			return False
		for x in state['on']:
			if obj == x[1]:
				return False
		for x in state['inside']:
			if obj == x[0] and x[1] in state_objects and state[x[1]]=='Close':
				return False
		return True
	
	if act == actions[2]:
		if(n!=2):
			return False
		if obj not in state['close']:
			return False
		if obj not in surface_objects:
			return False
		if state['grabbed'] == '':
			return False
		if obj in state_objects:
			if state[obj] == 'Close':
				return False
		return True
	
	if act == actions[3]:
		if(n!=3):
			return False
		if obj not in state['close']:
			return False
		if obj not in state_objects:
			return False
		if state[obj] == obj2:
			return False
		if state['grabbed'] != '':
			return False
		return True
	
	if act == actions[4]:
		if(n!=3):
			return False
		if obj not in state['close']:
			return False
		if obj not in pick_objects:
			return False
		if state['grabbed'] != '':
			return False
		for x in state['on']:
			if obj == x[1]:
				return False
		for x in state['inside']:
			if obj == x[0] and state[x[1]]=='Close':
				return False
		if obj2 in state_objects:
			if state[obj2] == 'Close':
				return False
		return True

# An approximate environment model
def changeState(state1, action):
	state = deepcopy(state1)
	# Change state based on action
	#######################################
	######## Insert your code here ########
	#######################################
	
	inside_obj = ['fridge','cupboard', 'box']
	
	act = action[0]
	n = len(action)
	obj = action[1]
	
	if(n==3):
		obj2 = action[2]
	
	if act == actions[0]:
		state['close'] = [obj]
		return state
	
	if act == actions[1]:
		t = list()
		for x in state['on']:
			if obj != x[0]:
				t.append(x)
		state['on'] = t
		t = list()
		for x in state['inside']:
			if obj != x[0]:
				t.append(x)
		state['inside'] = t
		state['grabbed'] = obj
		state['close'] = []
	
	if act == actions[2]:
		x = state['grabbed']
		state['grabbed'] = ''
		if obj in inside_obj:
			state['inside'].append((x,obj))
		else:
			state['on'].append((x,obj))
	
	if act == actions[3]:
		state[obj] = obj2
		state['close'] = []
	
	if act == actions[4]:
		state_1 = changeState(state, ['pick',obj])
		state_2 = changeState(state_1, ['moveTo',obj2])
		state_3 = changeState(state_2, ['drop',obj2])
		state = state_3
	return state

# An approximate goal checker
def checkGoal(state):
	# return ('apple', 'fridge') in state['inside'] and \
	# 	   ('orange', 'fridge') in state['inside'] and \
	# 	   ('banana', 'fridge') in state['inside'] and \
	# 	   state['fridge'] == 'Close'

	inside_obj = ['fridge','cupboard', 'box']
	state_objects = ['fridge','cupboard']
	pick_objects = ['apple', 'orange', 'banana', 'box', 'tray', 'tray2']

	x = json.load(open(args.goal))

	condition = True
	
	for t in x['goals']:
		if t['object'] in state_objects:
			condition = condition and state[t['object']].lower() == t['state']
			continue
		if t['object'] in pick_objects:
			if t['target'] in inside_obj:
				condition = condition and (t['object'],t['target']) in state['inside']
			else:
				condition = condition and (t['object'],t['target']) in state['on']
	return condition

