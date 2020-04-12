from environment import *

forward_plain = False

@deadline(120)
def getPlan(forward_plain):
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
import os
import shutil
name = os.getcwd().replace('\\', '/').split('/')[-1]

if args.input == 'part1':
    testOutput = 'testLogs/'+args.input+'/errors.txt'
    testResult = 'testLogs/'+args.input+'/result.txt'
    errors = open(testOutput, 'w+')
    result = open(testResult, 'w+')

all_worlds = {
    0: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table2'), ('banana', 'table2'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    1: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    2: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    3: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('orange', 'cupboard'), ('banana', 'cupboard')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    4: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('apple', 'fridge'), ('orange', 'fridge'), ('banana', 'fridge')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    5: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'cupboard'), ('orange', 'cupboard'), ('banana', 'cupboard'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    6: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table'), ('orange', 'table'), ('banana', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    7: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table2'), ('banana', 'table2'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    8: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    9: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []}
}

plans = {
    0: [["moveTo", "fridge"], \
               ["changeState", "fridge", "open"], \
               ["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["moveTo", "orange"], \
               ["pick", "orange"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["moveTo", "banana"], \
               ["pick", "banana"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["changeState", "fridge", "close"], \
               ], # fruits in fridge
    1: [["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "table"], \
               ["drop", "table"], \
               ], # apple on table
    2: [["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ["moveTo", "orange"], \
               ["pick", "orange"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ["moveTo", "banana"], \
               ["pick", "banana"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ], # fruits in box
    3:  [["moveTo", "fridge"], \
               ["changeState", "fridge", "open"], \
               ["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["changeState", "fridge", "close"], \
               ] # apple in fridge
}

def checkGoalWorking(state, goal_id):
    if goal_id == 0:
        return ('apple', 'table') in state['on']
    elif goal_id == 1:
        return (('apple', 'box') in state['inside'] and 
        ('orange', 'box') in state['inside'] and
        ('banana', 'box') in state['inside'])
    elif goal_id == 2:
        return (('apple', 'fridge') in state['inside'])
    elif goal_id == 3:
        return (('apple', 'fridge') in state['inside'] and 
        ('orange', 'fridge') in state['inside'] and 
        ('banana', 'fridge') in state['inside'] and 
        state['fridge'] == 'Close')
    elif goal_id == 4:
        return (('apple', 'fridge') in state['inside'] and 
        ('orange', 'cupboard') in state['inside'] and 
        ('banana', 'box') in state['inside'] and 
        state['fridge'] == 'Close' and state['cupboard'] == 'Close')

def checkActionWorking(state, action):
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

def changeStateWorking(state1, action):
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

def checkStateEquality(statePred, stateTrue):
    return (statePred['grabbed'] == stateTrue['grabbed'] and
        statePred['fridge'] == stateTrue['fridge'] and
        statePred['cupboard'] == stateTrue['cupboard'] and
        set(statePred['inside']).issubset(set(stateTrue['inside'])) and
        set(statePred['on']).issubset(set(stateTrue['on'])) and
        set(stateTrue['close']).issubset(set(statePred['close'])))

def testCheckAction():
    total_tests = 0; incorrect = 0
    errors.writelines(["\n\n#### Testing Check Action ####\n\n"])
    result.writelines(["\n\n#### Testing Check Action ####\n\n"])
    for worldID in range(5):
        for planID in range(4):
            for goal_id in range(4):
                state = all_worlds[worldID]
                plan = plans[planID]
                for action in plan:
                    total_tests += 1
                    if checkAction(state, action) and not checkActionWorking(state, action):
                        errors.writelines(["\nERROR: planner says incorrect action for a valid action\n"])
                        errors.writelines(["State\n", state, "\nAction\n", action])
                        incorrect += 1
                    elif not checkActionWorking(state, action) and checkAction(state, action):
                        errors.writelines(["\nERROR: planner says correct action for an invalid action\n"])
                        errors.writelines(["State\n", state, "\nAction\n", action])
                        incorrect += 1
                        break
                    state = changeStateWorking(state, action) 
    result.writelines(["Total tests\n", str(total_tests), "\nTotal incorrect\n", \
        str(incorrect), "\nPercentage correct\n", str(100.0*(total_tests-incorrect)/total_tests)])

def testChangeState():
    total_tests = 0; incorrect = 0
    errors.writelines(["\n\n#### Testing Change State ####\n\n"])
    result.writelines(["\n\n#### Testing Change State ####\n\n"])
    for worldID in range(5):
        for planID in range(4):
            for goal_id in range(4):
                state = all_worlds[worldID]
                plan = plans[planID]
                for action in plan:
                    total_tests += 1
                    if checkAction(state, action):
                        statePred = changeState(state, action) 
                        stateTrue = changeStateWorking(state, action)
                        if not checkStateEquality(statePred, stateTrue):
                            errors.writelines(["\nERROR: incorrect final state\n", str(statePred), '\nTrue state\n', str(stateTrue)])
                            errors.writelines(["\nOriginal state\n", str(state)])
                            errors.writelines(["\nOriginal action\n", str(action), '\n'])
                            incorrect += 1
                        state = statePred
                    else:
                        break
    result.writelines(["Total tests\n", str(total_tests), "\nTotal incorrect\n", \
        str(incorrect), "\nPercentage correct\n", str(100.0*(total_tests-incorrect)/total_tests)])

def checkPlan(test):
    testOutput = 'testLogs/'+args.input+'/errors_G'+args.goal.split('.')[1][-1]+'_W'+args.world.split('.')[1][-1]+'.txt'
    testResult = 'testLogs/'+args.input+'/result_G'+args.goal.split('.')[1][-1]+'_W'+args.world.split('.')[1][-1]+'.txt'
    errors = open(testOutput, 'w+')
    result = open(testResult, 'w+')
    if test == 'part2':
        errors.writelines(["\n\n#### Checking forward search ####\n"])
        result.writelines(["\n\n#### Checking forward search ####\n"])
    elif test == 'part3':
        errors.writelines(["\n\n#### Checking backward search ####\n"])
        result.writelines(["\n\n#### Checking backward search ####\n"])
    elif test == 'part4' or test == 'part5':
        errors.writelines(["\n\n#### Checking accelerated search ####\n"])
        result.writelines(["\n\n#### Checking accelerated search ####\n"])
    start = time.time(); print(0)
    try:
        if test == 'part2':
            plan = getPlan(True) ####
        elif test == 'part3':
            plan = getPlan(True) ####
        else:
            plan = getPlan(False) ####
        state = getCurrentState()
        result.writelines(["\n\nInitial State: ", str(state)])
        errors.writelines(["\n\nInitial State: ", str(state)])
        errors.writelines(["\n\nPlan\n", str(plan)])
        result.writelines(["\n\nPlan\n", str(plan)])
        result.writelines(["\nPlan length: ", str(len(plan))])
        result.writelines(["\nTime: ", str(time.time() - start)])
    except Exception as e:
        errors.writelines(["\n\nERROR:\n", str(e), "\n"])
    print(time.time()-start)
    try:
        res, state = execute(plan)
        result.writelines(["\n\nFinal State: ", str(state)])
        result.writelines(["\n\nSymbolic Result: ", str(checkGoalWorking(state, int(args.goal.split('.')[1][-1])))])
        result.writelines(["\n\nExecution Result: ", str(res or checkGoalWorking(state, int(args.goal.split('.')[1][-1])))])
        errors.writelines(["\n\nFinal State\n", str(state)])
    except Exception as e:
        errors.writelines(["\n\nERROR WHILE EXECUTING PLAN:\n", str(e), "\n"])
    errors.close(); result.close()

if __name__ == '__main__':
    if args.input == 'part1':
        testCheckAction()
        testChangeState()
        errors.close(); result.close()
    else:
        checkPlan(args.input)