import numpy as np
import time
import csv


combined = []

with open('Ex1-1.txt', mode='r', encoding='utf-8', newline='') as file:
    csv_reader = csv.reader(file, delimiter='\t')
    for row in csv_reader:
        row = [int(val) if val.strip() != '' else 0 for val in row]
        combined += row  # ajoute les éléments de row à la suite de combined

combined = np.array(combined)
print(combined)




"""
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
"""