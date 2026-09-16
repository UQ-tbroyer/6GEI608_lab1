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

#print(depthSearch(np.array([0,2,3,1,4,5,6,7,8])))


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

#print(breadthSearch(np.array([0,2,3,1,4,5,6,7,8])))


def depthLimitedSearch(grid, limit):
    # Même principe que depthSearch : les nouveaux états sont ajoutés
    # AU DÉBUT de frontier (comportement pile / profondeur d'abord).
    # Une colonne de plus (la 10e) sert à mémoriser la profondeur de
    # chaque état, pour pouvoir couper l'exploration à `limit`.
    frontier = np.empty((0, 10), dtype=int)
    tailleFrontier = []
    nbStateExplored = 0

    visited = set()

    startRow = np.append(grid, 0).reshape(1, 10)  # profondeur 0
    frontier = np.concatenate((startRow, frontier), axis=0)

    found = False

    while frontier.shape[0] > 0:

        j = 0
        while tuple(frontier[j][:9]) in visited:
            j += 1
            if j >= frontier.shape[0]:
                # plus aucun état non visité dans la frontière :
                # cette limite de profondeur ne mène pas à l'objectif
                return grid, False, tailleFrontier, nbStateExplored

        grid = frontier[j][:9]
        depth = frontier[j][9]

        visited.add(tuple(grid))

        nbStateExplored += 1
        print(nbStateExplored)

        if np.array_equal(grid, goalState):
            found = True
            break

        if depth < limit:
            posZero = int(np.where(grid == 0)[0][0])
            possibleMoves = legalMoves(posZero, 3)

            for i in range(len(possibleMoves)):
                nextGrid = move(grid, posZero, possibleMoves[i])

                if tuple(nextGrid) in visited:
                    continue

                frontierAddition = np.append(nextGrid, depth + 1).reshape(1, 10)
                frontier = np.concatenate((frontierAddition, frontier), axis=0)

        tailleFrontier.append(frontier.size)

    return grid, found, tailleFrontier, nbStateExplored


def iterativeDeepning(grid, maxLimit=31):
    # maxLimit = garde-fou : 31 est la profondeur maximale possible
    # pour n'importe quel état solvable du 8-puzzle.
    tailleFrontier = []
    nbStateExplored = 0
    executionTime = 0
    startTime = time.time_ns()

    limit = 0
    found = False
    currentGrid = grid

    while not found and limit <= maxLimit:
        currentGrid, found, tailleFrontierLimit, nbStateLimit = depthLimitedSearch(grid, limit)

        tailleFrontier += tailleFrontierLimit
        nbStateExplored += nbStateLimit

        limit += 1

    executionTime = time.time_ns() - startTime

    return currentGrid, executionTime, tailleFrontier, nbStateExplored

#print(iterativeDeepning(np.array([0,2,3,1,4,5,6,7,8])))