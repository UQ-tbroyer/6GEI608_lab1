import time
import heapq
from collections import deque

import numpy as np

goal_state = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

DIRECTIONS = {-3: "haut", 3: "bas", -1: "gauche", 1: "droite"}

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

    pos_zero = int(np.where(grid == 0)[0][0])
    children = []
    for end_pos in legalMoves(pos_zero):
        new_grid = move(grid, pos_zero, end_pos)
        action = DIRECTIONS[end_pos - pos_zero]
        children.append((new_grid, action))
    return children


def reconstruct_path(came_from, start_state, goal_state_tuple):

    actions = []
    state = goal_state_tuple
    while state != start_state:
        parent_state, action = came_from[state]
        actions.append(action)
        state = parent_state
    actions.reverse()
    return actions


def _to_state(grid):
    return tuple(int(x) for x in grid)


def is_solvable(grid):
    values = [v for v in grid if v != 0]
    inversions = sum(
        1
        for i in range(len(values))
        for j in range(i + 1, len(values))
        if values[i] > values[j]
    )
    return inversions % 2 == 0


def depthSearch(start_state, output_path=False):
    start_state_tuple = _to_state(start_state)
    goal_state_tuple = _to_state(goal_state)

    frontier = [start_state_tuple]
    pending = [0]
    frontier_sizes = []
    generated_states = 1
    nb_state_explored = 0
    visited = set()
    came_from = {}

    start_time = time.time_ns()
    final_state = None

    while pending:
        frontier_sizes.append(generated_states)

        current_state = frontier[pending.pop()]
        if current_state in visited:
            continue
        visited.add(current_state)
        nb_state_explored += 1

        if current_state == goal_state_tuple:
            final_state = current_state
            break

        for child_grid, action in getChildren(np.array(current_state)):
            child_state = _to_state(child_grid)
            if child_state not in visited:
                if child_state not in came_from:
                    came_from[child_state] = (current_state, action)
                frontier.append(child_state)
                pending.append(len(frontier) - 1)
                generated_states += 1

    execution_time = time.time_ns() - start_time
    final_grid = np.array(final_state) if final_state is not None else None

    if output_path:
        path = reconstruct_path(came_from, start_state_tuple, final_state) if final_state else None
        return final_grid, execution_time, frontier_sizes, nb_state_explored, path

    return final_grid, execution_time, frontier_sizes, nb_state_explored


def breadthSearch(start_state, output_path=False):
    start_state_tuple = _to_state(start_state)
    goal_state_tuple = _to_state(goal_state)

    frontier = [start_state_tuple]
    next_frontier_index = 0
    frontier_sizes = []
    generated_states = 1
    nb_state_explored = 0
    visited = {start_state_tuple}
    came_from = {}

    start_time = time.time_ns()
    final_state = None

    while next_frontier_index < len(frontier):
        frontier_sizes.append(generated_states)

        current_state = frontier[next_frontier_index]
        next_frontier_index += 1
        nb_state_explored += 1

        if current_state == goal_state_tuple:
            final_state = current_state
            break

        for child_grid, action in getChildren(np.array(current_state)):
            child_state = _to_state(child_grid)
            if child_state not in visited:
                visited.add(child_state)
                came_from[child_state] = (current_state, action)
                frontier.append(child_state)
                generated_states += 1

    execution_time = time.time_ns() - start_time
    final_grid = np.array(final_state) if final_state is not None else None

    if output_path:
        path = reconstruct_path(came_from, start_state_tuple, final_state) if final_state else None
        return final_grid, execution_time, frontier_sizes, nb_state_explored, path

    return final_grid, execution_time, frontier_sizes, nb_state_explored



OPPOSITE_ACTION = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}


def _depth_limited_search(start_state_tuple, goal_state_tuple, limit):

    frontier = [(start_state_tuple, 0, None)]
    pending = [0]
    frontier_sizes = []
    generated_states = 1
    nb_state_explored = 0


    best_depth = {start_state_tuple: 0}
    came_from = {}

    final_state = None

    while pending:
        frontier_sizes.append(generated_states)

        current_index = pending.pop()
        current_state, depth, last_action = frontier[current_index]
        nb_state_explored += 1

        if current_state == goal_state_tuple:
            final_state = current_state
            break

        if depth < limit:
            for child_grid, action in getChildren(np.array(current_state)):

                if last_action is not None and action == OPPOSITE_ACTION[last_action]:
                    continue

                child_state = _to_state(child_grid)
                new_depth = depth + 1

                if child_state not in best_depth or new_depth < best_depth[child_state]:
                    best_depth[child_state] = new_depth
                    came_from[child_state] = (current_state, action)
                    frontier.append((child_state, new_depth, action))
                    pending.append(len(frontier) - 1)
                    generated_states += 1

    return final_state, came_from, frontier_sizes, nb_state_explored


def iterativeDeepning(start_state, output_path=False, max_limit=31):

    start_state_tuple = _to_state(start_state)
    goal_state_tuple = _to_state(goal_state)

    limit = 0
    frontier_sizes = []
    nb_state_explored = 0
    final_state = None
    came_from = {}

    start_time = time.time_ns()

    while final_state is None and limit <= max_limit:
        final_state, came_from, sizes_at_limit, nb_at_limit = _depth_limited_search(
            start_state_tuple, goal_state_tuple, limit
        )
        previous_generated = frontier_sizes[-1] if frontier_sizes else 0
        frontier_sizes += [previous_generated + size for size in sizes_at_limit]
        nb_state_explored += nb_at_limit
        limit += 1

    execution_time = time.time_ns() - start_time
    final_grid = np.array(final_state) if final_state is not None else None

    if output_path:
        path = reconstruct_path(came_from, start_state_tuple, final_state) if final_state else None
        return final_grid, execution_time, frontier_sizes, nb_state_explored, path

    return final_grid, execution_time, frontier_sizes, nb_state_explored

def manhattan(state):
    distance = 0
    for index, value in enumerate(state):
        if value != 0:
            row, col = divmod(index, 3)
            goal_row, goal_col = divmod(value - 1, 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
    return distance


def misplaced_tiles(state):
    return sum(1 for index, value in enumerate(state) if value != 0 and value != index + 1)


HEURISTICS = {"manhattan": manhattan, "tuiles_mal_placees": misplaced_tiles}


def aStarSearch(start_state, output_path=False, heuristic=manhattan):
    start_state_tuple = _to_state(start_state)
    goal_state_tuple = _to_state(goal_state)

    frontier = [(heuristic(start_state_tuple), 0, start_state_tuple)]
    explored_sizes = []          
    nb_iterations = 0
    visited = set()
    best_cost = {start_state_tuple: 0}
    came_from = {}

    start_time = time.time_ns()
    final_state = None

    while frontier:
        _, cost, current_state = heapq.heappop(frontier)
        if current_state in visited:
            continue
        visited.add(current_state)
        nb_iterations += 1
        explored_sizes.append(len(visited))

        if current_state == goal_state_tuple:
            final_state = current_state
            break

        for child_grid, action in getChildren(np.array(current_state)):
            child_state = _to_state(child_grid)
            new_cost = cost + 1
            if child_state not in visited and new_cost < best_cost.get(child_state, float("inf")):
                best_cost[child_state] = new_cost
                came_from[child_state] = (current_state, action)
                heapq.heappush(frontier, (new_cost + heuristic(child_state), new_cost, child_state))

    execution_time = time.time_ns() - start_time
    final_grid = np.array(final_state) if final_state is not None else None

    if output_path:
        path = reconstruct_path(came_from, start_state_tuple, final_state) if final_state else None
        return final_grid, execution_time, explored_sizes, nb_iterations, path

    return final_grid, execution_time, explored_sizes, nb_iterations