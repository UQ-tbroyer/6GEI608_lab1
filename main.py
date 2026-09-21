import os

import numpy as np

import data
import search


def read_puzzle(file_path):
    values = []
    with open(file_path, mode='r', encoding='utf-8', newline='') as file:
        for line in file:
            raw = line.rstrip('\r\n')
            if not raw.strip():
                continue

            if '\t' in raw:
                row = [int(value) if value.strip() else 0 for value in raw.split('\t')]
            else:
                row = [int(value) if value.strip() else 0 for value in raw.replace(' ', '\t').split('\t')]

            values.extend(row)

    if len(values) != 9:
        raise ValueError(f"Puzzle file '{file_path}' does not contain 9 cells: {values}")

    return np.array(values, dtype=int)


#index = 4
for index in range(1,5):
    puzzle_file = f'Ex1-{index}.txt'
    start_state = read_puzzle(puzzle_file)

    # Dossier propre à cet exercice : sert de signature (puisque le nom des
    # fichiers produits par writeData ne contient plus l'index de l'exercice).
    output_dir = os.path.join("resultats", f"Ex1-{index}")

    algorithms = [
        ('depth', search.depthSearch),
        ('breadth', search.breadthSearch),
        ('iterative', search.iterativeDeepning),
    ]

    # 1) Chemin des actions à suivre pour atteindre l'état objectif
    #    (exigence principale de l'énoncé), une résolution par algorithme.
    print(f"État initial (Ex1-{index}) :", start_state)
    print("\n=== Chemin des actions ===")
    for name, algo in algorithms:
        final_grid, execution_time, frontier_sizes, nb_state_explored, path = algo(
            start_state, output_path=True
        )
        if path is not None:
            print(f"{name:>10} : {len(path)} mouvements -> {path}")
            data.writePath(name, path, outputDir=output_dir)
        else:
            print(f"{name:>10} : objectif NON trouvé")

    # 2) 10 exécutions par algorithme pour les statistiques de performance
    #    (temps, taille de frontière, nombre d'états explorés).
    NB_RUNS = 10
    print("\n=== Statistiques (10 exécutions par algorithme) ===")
    for name, algo in algorithms:
        print(f"\n--- {name} ---")
        for run in range(1, NB_RUNS + 1):
            final_grid, execution_time, frontier_sizes, nb_state_explored = algo(start_state)
            file_path = data.writeData(
                run, name, execution_time, frontier_sizes, nb_state_explored, outputDir=output_dir
            )

            status = "trouvé" if final_grid is not None else "NON trouvé"
            print(
                f"Essai {run:2d} | temps: {execution_time / 1_000_000_000:.6f} s | "
                f"états explorés: {nb_state_explored:>6} | objectif {status} | -> {file_path}"
            )