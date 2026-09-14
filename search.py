import numpy as np

import time


def move(grid, basePos, endPos):
    moveGrid = np.array([[1,0,0,0,0,0,0,0,0],
                        [0,1,0,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0,0],
                        [0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,1,0,0,0],
                        [0,0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,0,0,1]])


    moveGrid[basePos][basePos] = 0
    moveGrid[endPos][endPos] = 0

    moveGrid[basePos][endPos] = 1
    moveGrid[endPos][basePos] = 1

    return np.transpose(grid) @ moveGrid



#print(move(np.array([0,2,3,1,4,5,6,7,8]), 3, 0))
#print(move(np.array([0,2,3,1,4,5,6,7,8]), 3, 1))

def isMovelegal(basePos, endPos, lenGrid):
    if 
    

def depthSearch(Grid):
    frontier = []
    tailleFrontier = []
    nbState = 0
    executionTime = 0
    startTime = time.time_ns()

    goalState = np.array([1,2,3,4,5,6,7,8,0])

    executionTime = time.time_ns() - startTime


    return executionTime

print(depthSearch(np.array([0,2,3,1,4,5,6,7,8])))


def breadthSearch():
    pass

def iterativeDeepning():
    pass
