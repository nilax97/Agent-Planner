# COL864: Homework II
## Overview
* This exercise concerns writing a symbolic planner for an agent (mobile manipulator) capable of interacting with objects in a virtual environment. 
* The robot in the virtual environment is capable of performing a set of actions (move to, pick, place on, push to, open/close) which are described below. 
* The robot's environment can be represented as a set of objects. The robot can move towards a given object or peform interactions with it. 
* Some objects in the scene can have symbolic states. For example, a cupboard can be open or closed. Assume that the robot can determine if an object is open or closed, if an object is inside or on top of an object or if it is close to an object 
of interest. 
* The agent *does not know* the semantics of when actions are applicable and what are their effects. Hence, cannot perform tasks such as moving an object to a goal location that requires reasoning about a sequence of actions to accomplish a goal. 
* Your objective is endow the robot with a task planner enabling it to perform semantic tasks in the environment.   

## Simulation Environment
### Virtual Environment 
* The simulation environment is based on PyBullet physics simulator with a mobile manipulator (a robot called Husky with a manipulator arm. 
* The simulator consists of 10 world scenes and 5 different goals. A screenshot of the simulator appears below:
<div align="center">
<img src="https://github.com/shreshthtuli/COL864-Task-Planning/blob/master/screenshot.png" width="700" align="middle">
</div>
Note: All actions are symbolic and robot position is discretized by proximity to objects.

To setup the PyBullet (physics engine) environment please run the following (assuming python3):
```
pip install -r requirements.txt
```

A sample task execution on this simulator can be seen [here](https://youtu.be/-mIQuM3kjF4)

### World State 
The world state at any time instant can be accessed as a python dictionary of the form: 
```
{'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': []}
```
Here, the symbols denote the following:
* state\['grabbed'\] - object currently grabbed by the robot
* state\['fridge'\] - fridge state in (Open/Close)
* state\['cupboard'\] - cupboard state in (Open/Close)
* state\['inside'\] - consists of pairs of objects (a,b) where object a is inside object b
* state\['on'\] - consists of pairs of objects (a,b) where object a is on top of object b
* state\['close'\] - list of objects close to the robot

The initial state of the simulator can be initialized with different world scenes encoded in JSON format in directory *jsons/home_worlds/*. You can create new world scenes for testing.

### Agent Actions
The robot can preform the following actions: move, pick, drop, open/close doors and push objects. To simulate a plan in the simulation environment you can use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the destination object

A  symbolic plan consists of a sequence (a python list) of the afore mentioned actions parameterized with the objects in the set - (apple, orange, banana, table, table2, box, fridge, tray, tray2). You can input a plan to the *execute()* function which outputs a pair (plan success, final state after plan execution).

To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json --goal jsons/home_goals/goal0.json
```
Note: If you have a system that does not have a dedicated GPU or want to run on server or HPC with no graphics capabilities, you can add the option *--display tp* to the above command. This will save a sequence of third person perspective images in the logs folder.

## Sample state,action sequence

* t0 : {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': []}
* action = \[moveTo, apple\] 
* t1 = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': \['apple'\]}
* action = \[pick, apple\]
* t2 = {'grabbed': 'apple', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': \['apple'\]}

## Problem Statement
The goal of this exercise is to write a symbolic planner enabling the agent to perform a variety of tasks in the environment requiring navigation and interaction actions. 
1. Please implement a model of actions in terms of when they are feasible and how actions can change the world state. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file.
2. Implement a planner that can synthesize a feasible plan consisting of a sequence of actions to attain the goal state given the initial state of the world. 
 A standard goal checking function has been implemented as *checkGoal()* function. The planner should be implemented in the *getPlan()* function in *planner.py* file. You may visualize the plan in the simulator with the instructions below. The default goal in the given code is to put all fruits in the fridge (and keep the fridge closed). 
3. Formally write down the domain representation and the planning algorithm. Implement implement a forward and a backward planning strategy. Please compare the running time, branching factor and explain the advantages or disadvantages of both. 
4. Please improve the planner to synthesize feasible plans in a short amount of time. For example, return a feasible plan under 60 seconds. You may explore techniques for accelerating search ( e.g., via heuristics) building off material in the class and exploring techniques from your reading. There is extra credit for this part of the homework. 

You may review class notes and the Artificial Intelligence: A Modern Approach (AIMA) Chapter on Classical Planning for this exercise.  
<!-- You are expected to build a planner for robots in diverse environments with complex interactions. You need to develop an approximate environment model which is able to change the state corresponding to an input action with action feasibility checking. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file. A standard goal checking function has been implemented as *checkGoal()* function in the same file. The planner should be implemented in the *getPlan()* function in *planner.py* file.

The default goal in the given code is to put all fruits in the fridge (and keep the fridge closed).

Hint: You can use different search techniques like BFS, DFS, A*, or Reinforcement learning based approaches or even model it as Constrained Satisfaction Problem
-->

## Evaluation and tentative marking scheme
1. Correct implementation of *changeState()* and *checkAction()* functions for different types of actions and the ability to handle 
varied world states. (15 points)
2. Plan generation for the example goals with the *getPlan()* function (on world0) such as (30 points)
 	*  Put apple on table.
 	*  Put fruits: apple, orange and banana in box.
 	*  Put apple in fridge.
 	*  Put fruits in fridge and keep fridge closed. 
3. Evaluation of accelerated plan search for the scenarios such as the above. (20 points)
4. Evaluation of planner robustness on other world scenes. (20 points)
5. Explanation of search strategy implemented in this exercise. (15 points)

## Other Information
* This assignment is to be done individually.
* The simulator can be run on all machine configurations, however, dedicated GPU is preferable.

<!--
Your planner would be tested for different goals and different world scenes. The grading scheme would be as follows:
1. Correct implementation of *changeState()* and *checkAction()* functions for different types of actions. (15 points)
2. *getPlan()* function returns correct plan for goal0 - Put apple on table. (10 points)
3. *getPlan()* function returns correct plan for goal1 - Put fruits: apple, orange and banana in box. (10 points)
4. *getPlan()* function returns correct plan for goal2 - Put apple in fridge. (10 points)
5. *getPlan()* function returns correct plan for goal3 - Put fruits in fridge and keep fridge closed. (15 points)
6. *getPlan()* function takes less than half the deadline time (60 seconds) for each goal mentioned above. (10 points)
7. *getPlan()* function returns correct plan for goal3 on other worlds 1 and 2 as well. (15 points)
7. TBA. (15 points)
Note: The grading policy is subject to change without notice.
-->


## Developer
This exercise is based on the simulation tool developed as part of an undergraduate project at Dept. of CSE, IITD led by 
[Shreshth Tuli](www.github.com/shreshthtuli).
<br>
Shreshth will be the guest teaching assistant for this homework. He is reachable at shreshth.cs116@cse.iitd.ac.in. 

