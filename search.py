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


# --------------------------------------------------------------------------
# Déplacement par matrice de permutation (code fourni, conservé tel quel)
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


#print(move(np.array([0,2,3,1,4,5,6,7,8]), 3, 0))
#print(move(np.array([0,2,3,1,4,5,6,7,8]), 3, 1))


def isMovelegal(basePos, endPos, lenGrid):
    """Vérifie si l'échange basePos <-> endPos correspond à un déplacement
    valide de la case vide dans une grille carrée de côté lenGrid
    (lenGrid=3 pour le 8-puzzle)."""
    rowBase, colBase = divmod(basePos, lenGrid)
    rowEnd, colEnd = divmod(endPos, lenGrid)

    # même ligne, colonnes voisines (gauche/droite)
    if rowBase == rowEnd and abs(colBase - colEnd) == 1:
        return True
    # même colonne, lignes voisines (haut/bas)
    if colBase == colEnd and abs(rowBase - rowEnd) == 1:
        return True
    return False


def getLegalMoves(grid, lenGrid=3):
    """Retourne tous les états atteignables en un seul déplacement de la
    case vide, à partir de `grid`, en utilisant move()."""
    basePos = int(np.where(grid == 0)[0][0])
    nextStates = []
    for endPos in range(len(grid)):
        if endPos != basePos and isMovelegal(basePos, endPos, lenGrid):
            nextStates.append(move(grid, basePos, endPos))
    return nextStates


# --------------------------------------------------------------------------
# Recherche en largeur (BFS)
# --------------------------------------------------------------------------
def breadthSearch(Grid, outputFile="breadth_run.txt"):
    frontier = [Grid]
    tailleFrontier = []
    nbState = 0
    executionTime = 0
    startTime = time.time_ns()

    goalState = np.array([1,2,3,4,5,6,7,8,0])

    visited = {tuple(Grid)}
    found = False
    iteration = 0

    while frontier:
        iteration += 1
        tailleFrontier.append((iteration, len(frontier)))

        currentGrid = frontier.pop(0)  # FIFO -> recherche en largeur
        nbState += 1

        if np.array_equal(currentGrid, goalState):
            found = True
            break

        for nextGrid in getLegalMoves(currentGrid):
            key = tuple(nextGrid)
            if key not in visited:
                visited.add(key)
                frontier.append(nextGrid)

    executionTime = time.time_ns() - startTime

    with open(outputFile, mode='w', encoding='utf-8') as f:
        for it, size in tailleFrontier:
            f.write(f"{it}\t{size}\n")
        f.write(f"{nbState}\n")
        f.write(f"{executionTime}\n")

    return executionTime, nbState, found


# --------------------------------------------------------------------------
# Recherche à approfondissement itératif (IDDFS)
# --------------------------------------------------------------------------
def depthLimitedSearch(Grid, limit, startIteration, startNbState, tailleFrontier):
    """Une seule passe de recherche en profondeur limitée à `limit`.
    Reprend le compteur d'itérations et le nombre d'états explorés là où
    la passe précédente (limite plus basse) s'est arrêtée, pour que le
    fichier de sortie reflète l'exécution complète de l'IDDFS."""
    goalState = np.array([1,2,3,4,5,6,7,8,0])

    stack = [(Grid, 0)]  # (état, profondeur)
    visited = {tuple(Grid)}  # réinitialisé à chaque nouvelle limite

    iteration = startIteration
    nbState = startNbState
    found = False

    while stack:
        iteration += 1
        tailleFrontier.append((iteration, len(stack)))

        currentGrid, depth = stack.pop()  # LIFO -> recherche en profondeur
        nbState += 1

        if np.array_equal(currentGrid, goalState):
            found = True
            break

        if depth < limit:
            for nextGrid in getLegalMoves(currentGrid):
                key = tuple(nextGrid)
                if key not in visited:
                    visited.add(key)
                    stack.append((nextGrid, depth + 1))

    return found, iteration, nbState


def iterativeDeepning(Grid, outputFile="iterative_run.txt", maxLimit=31):
    """Répète une recherche en profondeur limitée avec une limite qui
    augmente de 1 à chaque passe (0, 1, 2, ...), jusqu'à trouver l'état
    objectif. maxLimit est un garde-fou pour éviter une boucle infinie
    si l'état de départ n'est pas solvable."""
    startTime = time.time_ns()

    tailleFrontier = []
    iteration = 0
    nbState = 0
    found = False
    limit = 0

    while not found and limit <= maxLimit:
        found, iteration, nbState = depthLimitedSearch(
            Grid, limit, iteration, nbState, tailleFrontier
        )
        limit += 1

    executionTime = time.time_ns() - startTime

    with open(outputFile, mode='w', encoding='utf-8') as f:
        for it, size in tailleFrontier:
            f.write(f"{it}\t{size}\n")
        f.write(f"{nbState}\n")
        f.write(f"{executionTime}\n")

    return executionTime, nbState, found


# --------------------------------------------------------------------------
# 10 exécutions, un fichier distinct par exécution
# --------------------------------------------------------------------------
if __name__ == "__main__":
    NB_RUNS = 10

    print("--- Recherche en largeur (BFS) ---")
    for run in range(1, NB_RUNS + 1):
        outFile = f"breadth_run_{run}.txt"
        execTime, nbState, found = breadthSearch(combined, outputFile=outFile)

        status = "trouvé" if found else "NON trouvé"
        print(
            f"Run {run:2d} | temps: {execTime:>12} ns | "
            f"états explorés: {nbState:>6} | objectif {status} | -> {outFile}"
        )

    print("\n--- Approfondissement itératif (IDDFS) ---")
    for run in range(1, NB_RUNS + 1):
        outFile = f"iterative_run_{run}.txt"
        execTime, nbState, found = iterativeDeepning(combined, outputFile=outFile)

        status = "trouvé" if found else "NON trouvé"
        print(
            f"Run {run:2d} | temps: {execTime:>12} ns | "
            f"états explorés: {nbState:>6} | objectif {status} | -> {outFile}"
        )