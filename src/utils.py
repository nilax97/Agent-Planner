from __future__ import print_function
import sys
import threading
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread
import pybullet as p
import math
import operator 
import json
from scipy.spatial import distance
import matplotlib.pyplot as plt
import time 
import numpy as np
import os
import glob

current_milli_time = lambda: int(round(time.time() * 1000))

camTargetPos = [0, 0, 0]
cameraUp = [0, 0, 2]
cameraPos = [0, 0, 5]
roll = -30
upAxisIndex = 2
camDistance = 5
pixelWidth = 400
pixelHeight = 300
aspect = pixelWidth / pixelHeight
nearPlane = 0.01
farPlane = 100
fov = 60
img_arr = []; img_arr2 = []

projectionMatrix = p.computeProjectionMatrixFOV(fov, aspect, nearPlane, farPlane)

# Dirt clean
dirtClean = False

def initDisplay(display):
    plt.axis('off')
    plt.rcParams["figure.figsize"] = [8,6]
    cam = plt.figure()
    plt.axis('off')
    ax = plt.gca()
    return ax, cam

def initLogging():
    plt.axis('off')
    fig = plt.figure(figsize = (38.42,21.6))
    return fig

names = {}

def keepHorizontal(object_list):
    """
    Keep the objects horizontal
    """
    for obj_id in object_list:
        pos = p.getBasePositionAndOrientation(obj_id)[0]
        pos = (pos[0], pos[1], max(0.01, pos[2]))
        p.resetBasePositionAndOrientation(obj_id,
                                          pos,
                                          p.getQuaternionFromEuler((0,0,0)))

def keepOnGround(object_list):
    """
    Keep the objects on ground
    """
    for obj_id in object_list:
        p.resetBasePositionAndOrientation(obj_id,
                                          (p.getBasePositionAndOrientation(obj_id)[0][0],
                                          p.getBasePositionAndOrientation(obj_id)[0][1], 0.01),
                                          p.getBasePositionAndOrientation(obj_id)[1])

def keepOrientation(objects):
    """
    keeps the orientation fixed
    """
    for obj_id in objects.keys():
        p.resetBasePositionAndOrientation(obj_id,
                                          p.getBasePositionAndOrientation(obj_id)[0],
                                          objects[obj_id])

def moveKeyboard(x1, y1, o1, object_list):
    """
    Move robot based on keyboard inputs
    """
    flag = False; delz = 0
    keys = p.getKeyboardEvents()
    if ord(b'm') in keys:
        if 65297 in keys:
            x1 += math.cos(o1)*0.001
            y1 += math.sin(o1)*0.001
            flag= True
        if 65298 in keys:
            x1 -= math.cos(o1)*0.001
            y1 -= math.sin(o1)*0.001
            flag= True
        if ord(b'o') in keys:
            delz = 0.001
            flag = True
        if ord(b'l') in keys:
            delz = -0.001
            flag = True
        if 65295 in keys:
            o1 += 0.005
            flag= True
        if 65296 in keys:
            o1 -= 0.005
            flag= True
    q = p.getQuaternionFromEuler((0,0,o1))
    for obj_id in object_list:
        (x, y, z1) = p.getBasePositionAndOrientation(obj_id)[0]
        z1 = max(0, z1+delz)
        if p.getBasePositionAndOrientation(obj_id)[0] != ((x1, y1, z1), (q)):
            p.resetBasePositionAndOrientation(obj_id, [x1, y1, z1], q)
    return  x1, y1, o1, flag

def moveUR5Keyboard(robotID, wings, gotoWing):
    """
    Change UR5 arm position based on keyboard input
    """
    keys = p.getKeyboardEvents()
    if ord(b'h') in keys:
        gotoWing(robotID, wings["home"])
        return
    if ord(b'u') in keys:
        gotoWing(robotID, wings["up"])
        return
    if ord(b'n') in keys:
        gotoWing(robotID, wings["down"])
    return

def changeCameraOnKeyboard(camDistance, yaw, pitch, x,y):
    """
    Change camera zoom or angle from keyboard
    """
    mouseEvents = p.getMouseEvents()
    keys = p.getKeyboardEvents()
    if ord(b'a') in keys:
        camDistance += 0.01
    elif ord(b'd') in keys:
        camDistance -= 0.01
    if ord(b'm') not in keys:
        if 65297 in keys:
            pitch += 0.2
        if 65298 in keys:
            pitch -= 0.2
        if 65295 in keys:
            yaw += 0.2
        if 65296 in keys:
            yaw -= 0.2
    return camDistance, yaw, pitch, 0,0

def changeCameraOnInput(camDistance, yaw, deltaDistance, deltaYaw):
    """
    Change camera zoom or angle from input
    """
    return (camDistance + 0.5 * deltaDistance, yaw + 5 * deltaYaw)

def mentionNames(id_lookup):
    """
    Add labels of all objects in the world
    """
    if len(names.keys()) == 0:
        for obj in id_lookup.keys():
            id = p.addUserDebugText(obj, 
                            (0, 0, 0.2),
                            parentObjectUniqueId=id_lookup[obj])

def getAllPositionsAndOrientations(id_lookup):
    """
    Get position and orientation of all objects for dataset
    """
    metrics = dict()
    for obj in id_lookup.keys():
        metrics[obj] = p.getBasePositionAndOrientation(id_lookup[obj])
    return metrics


def restoreOnKeyboard(world_states, x1, y1, o1):
    """
    Restore to last saved state when 'r' is pressed
    """
    keys = p.getKeyboardEvents()
    if ord(b'r') in keys:
        print("Pressed R")
        if len(world_states) != 0:
            print("Restoring state")
            world_states.pop()
            id1, x, y, o = world_states[-1]
            p.restoreState(stateId=id1)
            # q=p.getQuaternionFromEuler((0,0,0))
            # p.resetBasePositionAndOrientation(([0, 0, 0], q)) # Get robot to home when undo
            return x, y, o, world_states
    return x1, y1, o1, world_states

def restoreOnInput(world_states, x1, y1, o1, constraints):
    """
    Restore to last saved state when this function is called
    """
    print(world_states)
    if len(world_states) != 0:
        world_states.pop()
        id1, x, y, o, cids_old = world_states[-1]
        cids_list_old = []
        for obj in cids_old.keys():
            cids_list_old.append(cids_old[obj][1])
        for obj in constraints.keys():
            if not constraints[obj][1] in cids_list_old:
                p.removeConstraint(constraints[obj][1])
                del(constraints[obj])
        p.restoreState(stateId=id1)
        # q=p.getQuaternionFromEuler((0,0,0))
        # p.resetBasePositionAndOrientation(([0, 0, 0], q)) # Get robot to home when undo
        # return 0, 0, 0, world_states
        return x, y, o, constraints, world_states
    return x1, y1, o1, constraints, world_states

def findConstraintTo(obj1,constraints):
    if obj1 in constraints.keys():
        return constraints[obj1][0]
    return ""

def findConstraintWith(obj1,constraints):
    l = []
    for obj in constraints.keys():
        if obj1 in constraints[obj][0]:
            l.append(obj)
    return l

def checkGoal(goal_file, constraints, states, id_lookup, light, dirtClean):
    """
    Check if goal conditions are true for the current state
    """
    if not goal_file:
        return False
    with open(goal_file, 'r') as handle:
        file = json.load(handle)
    goals = file['goals']
    success = True
    print(constraints, goals)

    for goal in goals:
        obj = goal['object']
        if obj == 'light':
            if light:
                success = False

        if 'paper' in obj and goal['target'] == "":
            tgt = findConstraintWith(obj, constraints)
            print('Paper target = ' + str(tgt))
            heavy = False
            for t in tgt:
                if not (t == "" or 'paper' in t):
                    heavy = True
            success = success and heavy

        if obj == 'dirt':
            success = success and dirtClean

        if goal['target'] != "":
            tgt = findConstraintTo(obj, constraints)
            while not (tgt == "" or tgt == goal['target']):
                tgt = findConstraintTo(tgt, constraints)
            success = success and (tgt == goal['target'])

        if goal['state'] != "":
            positionAndOrientation = states[obj][goal['state']]
            q=p.getQuaternionFromEuler(positionAndOrientation[1])
            ((x1, y1, z1), (a1, b1, c1, d1)) = p.getBasePositionAndOrientation(id_lookup[obj])
            ((x2, y2, z2), (a2, b2, c2, d2)) = (positionAndOrientation[0], q)
            done = (True and 
                abs(x2-x1) <= 0.01 and 
                abs(y2-y1) <= 0.01 and 
                abs(a2-a1) <= 0.01 and 
                abs(b2-b2) <= 0.01 and 
                abs(c2-c1) <= 0.02)
            success = success and done

        if goal['position'] != "":
            pos = p.getBasePositionAndOrientation(id_lookup[obj])[0]
            goal_pos = p.getBasePositionAndOrientation(id_lookup[goal['position']])[0]
            if abs(distance.euclidean(pos, goal_pos)) > abs(goal['tolerance']):
                success = False
    return success

def checkUR5constrained(constraints):
    """
    Check if UR5 gripper is already holding something
    """
    for obj in constraints.keys():
        if constraints[obj][0] == 'ur5':
            return True
    return False

def checkInside(constraints, states, id_lookup, obj, enclosures):
    """
    Check if object is inside cupboard or fridge
    """
    for enclosure in enclosures:
        if isClosed(enclosure, states, id_lookup):
            (x1, y1, z1) = p.getBasePositionAndOrientation(id_lookup[obj])[0]
            (x2, y2, z2) = p.getBasePositionAndOrientation(id_lookup[enclosure])[0]
            (l, w, h) = 1.0027969752543706, 0.5047863562602029, 1.5023976731489332
            inside = abs(x2-x1) < l and abs(y2-y1) < 1.5*w and abs(z1-z2) < h
            print(l, w, h, abs(x2-x1), abs(y2-y1), abs(z1-z2))
            tgt = findConstraintTo(obj, constraints)
            while not (tgt == "" or tgt == enclosure):
                tgt = findConstraintTo(tgt, constraints)        
            if inside or (tgt == enclosure): return True
    return False

def isClosed(enclosure, states, id_lookup):
    """
    Check if enclosure is closed or not
    """
    positionAndOrientation = states[enclosure]["close"]
    q=p.getQuaternionFromEuler(positionAndOrientation[1])
    ((x1, y1, z1), (a1, b1, c1, d1)) = p.getBasePositionAndOrientation(id_lookup[enclosure])
    ((x2, y2, z2), (a2, b2, c2, d2)) = (positionAndOrientation[0], q)
    closed = (abs(x2-x1) <= 0.01 and 
            abs(y2-y1) <= 0.01 and 
            abs(a2-a1) <= 0.01 and 
            abs(b2-b2) <= 0.01 and 
            abs(c2-c1) <= 0.01 and 
            abs(d2-d2) <= 0.01)
    return closed

def isInState(enclosure, state, position):
    """
    Check if enclosure is closed or not
    """
    positionAndOrientation = state
    q=p.getQuaternionFromEuler(positionAndOrientation[1])
    ((x1, y1, z1), (a1, b1, c1, d1)) = position
    ((x2, y2, z2), (a2, b2, c2, d2)) = (positionAndOrientation[0], q)
    closed = (abs(x2-x1) <= 0.07 and 
            abs(y2-y1) <= 0.07 and 
            abs(a2-a1) <= 0.07 and 
            abs(b2-b2) <= 0.07 and 
            abs(c2-c1) <= 0.07 and 
            abs(d2-d2) <= 0.07)
    return closed

def objDistance(obj1, obj2, id_lookup):
    (x, y, z), _ = p.getBasePositionAndOrientation(id_lookup[obj1])
    (x2, y2, z2), _ = p.getBasePositionAndOrientation(id_lookup[obj2])
    return math.sqrt((x-x2)**2 + (y-y2)**2 + (z-z2)**2)

def saveImage(lastTime, imageCount, display, ax, o1, cam, dist, yaw, pitch, camTargetPos, wall_id, light):
    current = current_milli_time()
    if (current - lastTime) < 100:
        return lastTime, imageCount
    img_arr = []; img_arr2 = []; rgb = []
    if display == "fp" or display == "both":
        camPos = [camTargetPos[0] - dist*math.cos(o1), camTargetPos[1] - dist*math.sin(o1)]
        if wall_id > -1 and (abs(camPos[0]) > 4 or abs(camPos[1]) > 5):
            p.changeVisualShape(wall_id, -1, rgbaColor = [1, 1, 1, 0.4])
        viewMatrixFP = p.computeViewMatrixFromYawPitchRoll(camTargetPos, dist, -90+(o1*180/math.pi), -35,
                                                                roll, upAxisIndex)
        img_arr = p.getCameraImage(pixelWidth,
                                      pixelHeight,
                                      viewMatrixFP,
                                      projectionMatrix,
                                      shadow=1,
                                      lightDirection=[1, 1, 1],
                                      renderer=p.ER_BULLET_HARDWARE_OPENGL,
                                      flags=p.ER_NO_SEGMENTATION_MASK)
        if wall_id > -1:
            p.changeVisualShape(wall_id, -1, rgbaColor = [1, 1, 1, 1])
    if display == "tp" or display == "both":
        viewMatrixTP = p.computeViewMatrixFromYawPitchRoll(camTargetPos,
                                                            dist, yaw, pitch,
                                                            roll, upAxisIndex)
        img_arr2 = p.getCameraImage(pixelWidth,
                                      pixelHeight,
                                      viewMatrixTP,
                                      projectionMatrix,
                                      shadow=1,
                                      lightDirection=[1, 1, 1],
                                      renderer=p.ER_BULLET_HARDWARE_OPENGL,
                                      flags=p.ER_NO_SEGMENTATION_MASK)

    if display:
        if display == "fp":
            rgb = img_arr[2]
        elif display == "tp":
            rgb = img_arr2[2]
        if not light:
            rgb = np.divide(rgb, 2)
        plt.imsave("logs/"+str(imageCount)+".jpg", arr=np.reshape(rgb, (pixelHeight, pixelWidth, 4)) * (1. / 255.))
    return current, imageCount+1

def deleteAll(path):
    filesToRemove = [os.path.join(path,f) for f in os.listdir(path)]
    for f in filesToRemove:
        os.remove(f) 

# Datapoint utils

def globalIDLookup(objs, objects):
    gidlookup = {}
    for i in range(len(objects)):
        if objects[i]['name'] in objs:
            gidlookup[objects[i]['name']] = i
    return gidlookup

def checkNear(obj1, obj2, metrics, dist):
    (x1, y1, z1) = metrics[obj1][0]
    (x2, y2, z2) = metrics[obj2][0]
    return abs(distance.euclidean((x1, y1, z1), (x2, y2, z2))) < dist

def checkIn(obj1, obj2, obj1G, obj2G, metrics, constraints):
    if 'Container' in obj2G['properties']:
        (x1, y1, z1) = metrics[obj1][0]
        (x2, y2, z2) = metrics[obj2][0]
        (l, w, h) = obj2G['size']
        inside = abs(x2-x1) < l and abs(y2-y1) < 1.5*w and abs(z1-z2) < h
        tgt = findConstraintTo(obj1, constraints)
        while not (tgt == "" or tgt == obj2):
            tgt = findConstraintTo(tgt, constraints)        
        return inside or (tgt == obj2)
    return False

def checkOn(obj1, obj2, obj1G, obj2G, metrics, constraints):
    if 'Surface' in obj2G['properties']:
        (x1, y1, z1) = metrics[obj1][0]
        (x2, y2, z2) = metrics[obj2][0]
        (l, w, h) = obj2G['size']
        on = abs(x2-x1) < l + 0.2 and abs(y2-y1) < w + 0.2 and z1 > z2 + 0.75*h
        tgt = findConstraintTo(obj1, constraints)
        while not (tgt == "" or tgt == obj2):
            tgt = findConstraintTo(tgt, constraints)        
        return on or (tgt == obj2)
    return False

def getDirectedDist(obj1, obj2, metrics):
    """
    Returns delX, delY, delZ, delO from obj1 to obj2
    """
    (x1, y1, z1) = metrics[obj1][0]
    (x2, y2, z2) = metrics[obj2][0]
    return [x2-x1, y2-y1, z2-z1, math.atan2((y2-y1),(x2-x1))%(2*math.pi)]


def grabbedObj(obj, constraints):
    """
    Check if object is grabbed by robot
    """
    return (obj in constraints.keys() and constraints[obj][0] == 'ur5')

def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def deadline(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer