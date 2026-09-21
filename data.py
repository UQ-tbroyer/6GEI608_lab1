import csv
import os


def writeData(numTry, searchName, executionTime, tailleFrontier, nbStateExplored, outputDir="resultats"):
    fileName = os.path.join(outputDir, f"{searchName}_essai{numTry}.csv")

    with open(fileName, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")

        for numIteration, taille in enumerate(tailleFrontier, start=1):
            writer.writerow([numIteration, taille])

        writer.writerow([nbStateExplored])
        writer.writerow([executionTime / 1_000_000_000])

    return fileName


def writePath(searchName, path, outputDir="resultats"):

    fileName = os.path.join(outputDir, f"{searchName}_chemin.csv")

    with open(fileName, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        for action in path:
            writer.writerow([action])
        writer.writerow([f"Nombre de mouvements : {len(path)}"])

    return fileName