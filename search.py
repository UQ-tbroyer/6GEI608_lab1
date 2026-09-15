import numpy as np

import time

goalState = np.array([1,2,3,4,5,6,7,8,0])

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

def isMovelegal(basePos, endPos, lenSide):
    baseRow, baseCol = divmod(basePos, lenSide)
    endRow, endCol = divmod(endPos, lenSide)

    return abs(baseRow - endRow) + abs(baseCol - endCol) == 1


def legalMoves(basePos, lenSide):

    row, col = divmod(basePos, lenSide)
    moves = []

    for dRow, dCol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        newRow, newCol = row + dRow, col + dCol
        if 0 <= newRow < lenSide and 0 <= newCol < lenSide:
            moves.append(newRow * lenSide + newCol)

    return moves  

def depthSearch(grid):
    frontier = np.empty((0, 9), dtype=int)
    tailleFrontier = []
    nbStateExplored = 0

    visited = set()   

    executionTime = 0
    startTime = time.time_ns()

    
    while (not(np.array_equal(grid, goalState))):

        visited.add(tuple(grid)) 

        posZero = int(np.where(grid == 0)[0][0])
        possibleMoves = legalMoves(posZero, 3)

        for i in range(len(possibleMoves)):
            frontierAddition = move(grid, posZero, possibleMoves[i]).reshape(1, 9)

            if tuple(frontierAddition[0]) in visited: 
                continue

            frontier = np.concatenate((frontierAddition, frontier), axis=0)

        j = 0                                          
        while tuple(frontier[j]) in visited:
            j += 1
        grid = frontier[j]

        tailleFrontier.append(frontier.size)

        nbStateExplored += 1
        print(nbStateExplored)

    executionTime = time.time_ns() - startTime

    return grid, executionTime, tailleFrontier, nbStateExplored

print(depthSearch(np.array([0,2,3,1,4,5,6,7,8])))


def breadthSearch(grid):
    frontier = np.empty((0, 9), dtype=int)
    tailleFrontier = []
    nbStateExplored = 0

    visited = set()   

    executionTime = 0
    startTime = time.time_ns()

    
    while (not(np.array_equal(grid, goalState))):

        visited.add(tuple(grid)) 

        posZero = int(np.where(grid == 0)[0][0])
        possibleMoves = legalMoves(posZero, 3)

        j = 0 

        for i in range(len(possibleMoves)):
            frontierAddition = move(grid, posZero, possibleMoves[i]).reshape(1, 9)

            if tuple(frontierAddition[0]) in visited: 
                continue

            frontier = np.concatenate((frontier, frontierAddition), axis=0)

                                                 
        while tuple(frontier[j]) in visited:
            j += 1
        grid = frontier[j]

        tailleFrontier.append(frontier.size)

        nbStateExplored += 1
        print(nbStateExplored)

    executionTime = time.time_ns() - startTime

    return grid, executionTime, tailleFrontier, nbStateExplored

print(breadthSearch(np.array([0,2,3,1,4,5,6,7,8])))

def iterativeDeepning():
    pass
