from environment_working import *

def getPlan(state):
	node = (deepcopy(state), [])
	curlayer = [node]; nextlayer = []

	# BFS planner
	for i in range(5):
		print('Depth = ', i)
		for n in curlayer:
			if checkGoal(n[0]):
				print("Result = ", n[1])
				return n[1]
			nextlayer += allNeighbours(n)
		curlayer = nextlayer
		nextlayer = []

res, state = execute(getPlan(state))

print(res)
print(state)

