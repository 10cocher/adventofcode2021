import os
from typing import List, Tuple

import numpy as np


def is_grid_finished(a: np.ndarray) -> bool:
    ok1 = np.sum(np.all(a, axis=0)) > 0
    ok2 = np.sum(np.all(a, axis=1)) > 0
    return ok1 or ok2


def compute_score(a: np.ndarray, ok: np.ndarray) -> int:
    a2 = np.copy(a)
    a2[ok] = 0
    return np.sum(np.sum(a2, axis=0), axis=0)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    numbers = np.asarray(data[0].split(","), dtype=int)
    #
    n = 5
    n_grids = int((len(data) - 1) / 6)
    #
    grids: List[Tuple[np.ndarray, np.ndarray]] = []
    #
    for i_grid in range(n_grids):
        grid = np.zeros((n, n), dtype=int)
        row_start = (n + 1) * i_grid + 2
        row_end = row_start + n
        for row in range(row_start, row_end):
            row_numbers = data[row].rstrip("\n").split(" ")
            row_numbers = np.asarray([r for r in row_numbers if len(r) > 0], dtype=int)
            grid[row - row_start, :] = row_numbers
        grids.append((grid, np.zeros((5, 5), dtype=bool)))
    #
    finished = False
    grid_wins = np.zeros((n_grids,), dtype=bool)
    for number in numbers:
        for i_grid in range(n_grids):
            grid, ok = grids[i_grid]
            mask = grid == number
            ok[mask] = True
            #
            if is_grid_finished(ok):
                score = compute_score(grid, ok)
                grid_wins[i_grid] = True
                finished = np.sum(grid_wins) == n_grids
                if finished:
                    print(score, number, score * number)
                    break
            else:
                grids[i_grid] = (grid, ok)
        if finished:
            break
