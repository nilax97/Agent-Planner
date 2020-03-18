from environment import *

@deadline(120)
def getPlan():
	#######################################
	######## Insert your code here ########
	#######################################
	return [["moveTo", "fridge"], \
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
			   ]

# Execute function takes in a plan as input and returns if goal constraints 
# are valid and the final state after plan execution
res, state = execute(getPlan())

print(res)
print(state)