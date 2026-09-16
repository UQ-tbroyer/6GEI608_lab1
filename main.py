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


for index in range(1, 1):
    puzzle_file = f'Ex1-{index}.txt'
    start_state = read_puzzle(puzzle_file)
    result = search.depthSearch(start_state)
    final_grid, execution_time, frontier_sizes, nb_state_explored = result
    data.writeData(index, 'depth', execution_time, frontier_sizes, nb_state_explored)