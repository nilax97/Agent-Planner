from environment import *

forward_plain = False

@deadline(120)
def getPlan():
	#######################################
	######## Insert your code here ########
	#######################################

	objects = ['apple', 'orange', 'banana', 'table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
	enclosures = ['fridge', 'cupboard']
	actions = ['moveTo', 'pick', 'drop', 'changeState', 'pushTo']

	pick_objects = ['apple', 'orange', 'banana', 'box', 'tray', 'tray2']
	surface_objects = ['table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
	state_objects = ['fridge','cupboard']
	
	state = getCurrentState()

	goal = json.load(open(args.goal))
	goal_objects = set()
	for x in goal['goals']:
		goal_objects.add(x['object'])
		goal_objects.add(x['target'])

	# for x in state['on']:
	# 	if x[0] in goal_objects or x[1] in goal_objects:
	# 		goal_objects.add(x[0])
	# 		goal_objects.add(x[1])

	for x in state['inside']:
		if x[0] in goal_objects:
			goal_objects.add(x[1])

	goal_objects = list(goal_objects)

	if '' in goal_objects:
		goal_objects.remove('')

	if (forward_plain==True):
		goal_objects = objects

	possible_actions = list()
	for x in objects:
		if(x not in goal_objects):
			continue
		possible_actions.append(['moveTo',x])
	for x in pick_objects:
		if(x not in goal_objects):
			continue
		possible_actions.append(['pick',x])
	for x in surface_objects:
		if(x not in goal_objects):
			continue
		possible_actions.append(['drop',x])
	for x in state_objects:
		if(x not in goal_objects):
			continue
		possible_actions.append(['changeState',x,'Open'])
		possible_actions.append(['changeState',x,'Close'])
	# for x in pick_objects:
	#	 if(x not in goal_objects):
	#		 continue
	#	 for y in surface_objects:
	#		 if(x not in goal_objects):
	#			 continue
	#		 possible_actions.append(['pushTo',x,y])


	def state_string(state):
		state['inside'] = sorted(state['inside'])
		state['on'] = sorted(state['on'])
		state['close'] = sorted(state['close'])
		return json.dumps(state)

	visited = dict()
	queue = list()
	queue.append(state)
	visited[state_string(state)] = (0,0)
	solution = list()
	while(len(queue) != 0):
		state = queue.pop(0)
		if checkGoal(state):
			while(state != 0):
				ans = visited[state_string(state)]
				solution.append(ans[0])
				state = ans[1]
			solution = [x for x in reversed(solution) if x!=0]
			break
		for x in possible_actions:
			if checkAction(state,x):
				state1 = changeState(state,x)
				state1_s = state_string(state1)
				if state1_s not in visited:
					visited[state1_s] = [x,state]
					queue.append(state1)
	for x in solution:
		if x[-1] == 'Open':
			x[-1] = 'open'
		if x[-1] == 'Close':
			x[-1] = 'close'
	return solution

# Execute function takes in a plan as input and returns if goal constraints 
# are valid and the final state after plan execution
res, state = execute(getPlan())

print(res)
print(state)