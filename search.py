import csv
import os
import time
from collections import deque

import numpy as np

goalState = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

# Déplacement de la case vide : delta de position -> direction
DIRECTIONS = {-3: "haut", 3: "bas", -1: "gauche", 1: "droite"}


# --------------------------------------------------------------------------
# Déplacement par matrice de permutation (conservé tel quel)
# --------------------------------------------------------------------------
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


def isMovelegal(basePos, endPos, lenSide):
    baseRow, baseCol = divmod(basePos, lenSide)
    endRow, endCol = divmod(endPos, lenSide)
    return abs(baseRow - endRow) + abs(baseCol - endCol) == 1


def legalMoves(basePos, lenSide=3):
    return [endPos for endPos in range(lenSide * lenSide)
            if endPos != basePos and isMovelegal(basePos, endPos, lenSide)]


def getChildren(grid):
    """Retourne les états voisins de `grid`, chacun avec l'action (direction
    du déplacement de la case vide) qui y mène."""
    posZero = int(np.where(grid == 0)[0][0])
    children = []
    for endPos in legalMoves(posZero):
        newGrid = move(grid, posZero, endPos)
        action = DIRECTIONS[endPos - posZero]
        children.append((newGrid, action))
    return children


def reconstructPath(cameFrom, startState, goalState_):
    """Remonte cameFrom depuis l'état objectif jusqu'à l'état initial pour
    obtenir la liste ordonnée des actions à suivre."""
    actions = []
    state = goalState_
    while state != startState:
        parentState, action = cameFrom[state]
        actions.append(action)
        state = parentState
    actions.reverse()
    return actions


def writeStatsFile(outputFile, tailleFrontier, nbStateExplored, executionTime):
    """Format demandé par l'énoncé :
    - une ligne par itération : numéro_itération \t taille_de_frontiere
    - avant-dernière ligne     : nombre total d'états explorés
    - dernière ligne           : temps d'exécution
    """
    with open(outputFile, mode='w', encoding='utf-8') as f:
        for iteration, taille in enumerate(tailleFrontier, start=1):
            f.write(f"{iteration}\t{taille}\n")
        f.write(f"{nbStateExplored}\n")
        f.write(f"{executionTime}\n")


def writePathFile(outputFile, path, exerciseName=None):
    with open(outputFile, mode='w', encoding='utf-8') as f:
        if exerciseName:
            f.write(f"Exercice : {exerciseName}\n\n")
        for action in path:
            f.write(f"{action}\n")
        f.write(f"Nombre de mouvements : {len(path)}\n")


# --------------------------------------------------------------------------
# Recherche en profondeur (DFS) — frontière = vraie pile (list.pop())
# --------------------------------------------------------------------------
def depthSearch(grid, outputFile=None):
    startState = tuple(int(x) for x in grid)
    frontier = [startState]
    tailleFrontier = []
    nbStateExplored = 0
    visited = set()
    cameFrom = {}

    startTime = time.time_ns()
    found = None

    while frontier:
        tailleFrontier.append(len(frontier))

        currentState = frontier.pop()  # LIFO -> profondeur
        if currentState in visited:
            continue
        visited.add(currentState)
        nbStateExplored += 1

        if currentState == tuple(int(x) for x in goalState):
            found = currentState
            break

        for childGrid, action in getChildren(np.array(currentState)):
            childState = tuple(int(x) for x in childGrid)
            if childState not in visited:
                if childState not in cameFrom:
                    cameFrom[childState] = (currentState, action)
                frontier.append(childState)

    executionTime = time.time_ns() - startTime
    path = reconstructPath(cameFrom, startState, found) if found else None

    if outputFile:
        writeStatsFile(outputFile, tailleFrontier, nbStateExplored, executionTime)

    return found, path, executionTime, tailleFrontier, nbStateExplored


# --------------------------------------------------------------------------
# Recherche en largeur (BFS) — frontière = vraie file (deque.popleft())
# --------------------------------------------------------------------------
def breadthSearch(grid, outputFile=None):
    startState = tuple(int(x) for x in grid)
    frontier = deque([startState])
    tailleFrontier = []
    nbStateExplored = 0
    visited = {startState}
    cameFrom = {}

    goalTuple = tuple(int(x) for x in goalState)

    startTime = time.time_ns()
    found = None

    while frontier:
        tailleFrontier.append(len(frontier))

        currentState = frontier.popleft()  # FIFO -> largeur
        nbStateExplored += 1

        if currentState == goalTuple:
            found = currentState
            break

        for childGrid, action in getChildren(np.array(currentState)):
            childState = tuple(int(x) for x in childGrid)
            if childState not in visited:
                visited.add(childState)
                cameFrom[childState] = (currentState, action)
                frontier.append(childState)

    executionTime = time.time_ns() - startTime
    path = reconstructPath(cameFrom, startState, found) if found else None

    if outputFile:
        writeStatsFile(outputFile, tailleFrontier, nbStateExplored, executionTime)

    return found, path, executionTime, tailleFrontier, nbStateExplored


# --------------------------------------------------------------------------
# Recherche en profondeur limitée + approfondissement itératif (IDDFS)
# --------------------------------------------------------------------------
def depthLimitedSearch(grid, limit):
    startState = tuple(int(x) for x in grid)
    frontier = [(startState, 0)]  # (état, profondeur)
    tailleFrontier = []
    nbStateExplored = 0
    visited = set()
    cameFrom = {}

    goalTuple = tuple(int(x) for x in goalState)

    found = None

    while frontier:
        tailleFrontier.append(len(frontier))

        currentState, depth = frontier.pop()
        if currentState in visited:
            continue
        visited.add(currentState)
        nbStateExplored += 1

        if currentState == goalTuple:
            found = currentState
            break

        if depth < limit:
            for childGrid, action in getChildren(np.array(currentState)):
                childState = tuple(int(x) for x in childGrid)
                if childState not in visited:
                    if childState not in cameFrom:
                        cameFrom[childState] = (currentState, action)
                    frontier.append((childState, depth + 1))

    path = reconstructPath(cameFrom, startState, found) if found else None
    return found, path, tailleFrontier, nbStateExplored


def iterativeDeepning(grid, outputFile=None, maxLimit=31):
    # maxLimit = garde-fou : 31 est la profondeur maximale possible
    # pour n'importe quel état solvable du 8-puzzle.
    limit = 0
    tailleFrontier = []
    nbStateExplored = 0
    found = None
    path = None

    startTime = time.time_ns()

    while found is None and limit <= maxLimit:
        found, path, tailleFrontierLimit, nbStateLimit = depthLimitedSearch(grid, limit)
        tailleFrontier += tailleFrontierLimit
        nbStateExplored += nbStateLimit
        limit += 1

    executionTime = time.time_ns() - startTime

    if outputFile:
        writeStatsFile(outputFile, tailleFrontier, nbStateExplored, executionTime)

    return found, path, executionTime, tailleFrontier, nbStateExplored


# --------------------------------------------------------------------------
# Lecture de l'état initial, chemin d'actions, puis 10 exécutions/algorithme
# --------------------------------------------------------------------------
if __name__ == "__main__":
    INPUT_FILE = 'Ex1-1.txt'
    RESULTS_DIR = 'resultats'
    # Signature : nom de l'exercice déduit du fichier d'entrée (ex. "Ex1-1")
    EXERCISE_NAME = os.path.splitext(os.path.basename(INPUT_FILE))[0]

    os.makedirs(RESULTS_DIR, exist_ok=True)

    combined = []
    with open(INPUT_FILE, mode='r', encoding='utf-8', newline='') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        for row in csv_reader:
            row = [int(val) if val.strip() != '' else 0 for val in row]
            combined += row

    combined = np.array(combined)
    print(f"Exercice : {EXERCISE_NAME}")
    print("État initial :", combined)

    algorithms = [
        ("depth", depthSearch),
        ("breadth", breadthSearch),
        ("iterative", iterativeDeepning),
    ]

    # 1) Exigence principale de l'énoncé : le chemin des actions à suivre
    #    pour aller de l'état initial à l'état objectif.
    print("\n=== Chemin des actions (une résolution par algorithme) ===")
    for name, algo in algorithms:
        found, path, execTime, _, nbState = algo(combined)
        if found is not None:
            print(f"{name:>10} : {len(path)} mouvements -> {path}")
            pathFile = os.path.join(RESULTS_DIR, f"{EXERCISE_NAME}_{name}_chemin.txt")
            writePathFile(pathFile, path, exerciseName=EXERCISE_NAME)
        else:
            print(f"{name:>10} : objectif NON trouvé")

    # 2) N.B. de l'énoncé : 10 exécutions par algorithme, un fichier de
    #    statistiques distinct par exécution (temps, taille de frontière,
    #    nombre d'états explorés). Le format de ce fichier est imposé par
    #    l'énoncé (1re ligne = itération 1, avant-dernière = nb d'états,
    #    dernière = temps) : la signature ne peut donc pas être ajoutée
    #    en en-tête sans casser ce format. Elle est plutôt intégrée dans
    #    le nom du fichier lui-même.
    NB_RUNS = 10
    print("\n=== Statistiques (10 exécutions par algorithme) ===")
    for name, algo in algorithms:
        print(f"\n--- {name} ---")
        for run in range(1, NB_RUNS + 1):
            outFile = os.path.join(RESULTS_DIR, f"{EXERCISE_NAME}_{name}_run_{run}.txt")
            found, _, execTime, tailleFrontier, nbState = algo(combined, outputFile=outFile)

            status = "trouvé" if found is not None else "NON trouvé"
            print(
                f"Run {run:2d} | temps: {execTime:>12} ns | "
                f"états explorés: {nbState:>6} | objectif {status} | -> {outFile}"
            )