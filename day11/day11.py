import os
from typing import Tuple

import numpy as np


def get_data(path: str) -> np.ndarray:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    n1 = len(data)
    n2 = len(data[0].rstrip("\n"))
    #
    arr = np.zeros((n1, n2), dtype=int)
    for i1 in np.arange(n1):
        arr[i1] = np.asarray(list(data[i1].rstrip("\n")))
    #
    return arr


def apply_one_step(grid_in: np.ndarray, debug: bool = False) -> Tuple[np.ndarray, int]:
    n1_temp, n2_temp = grid_in.shape
    n1 = n1_temp + 2
    n2 = n2_temp + 2
    grid = np.zeros((n1, n2), dtype=int)
    grid[1 : n1_temp + 1, 1 : n2_temp + 1] = grid_in
    #
    flashed = np.zeros((n1, n2), dtype=bool)
    n_flashed = 0
    #
    to_add = np.ones((n1, n2), dtype=int)
    #
    cond = True
    cpt = 0
    #
    while cond:
        cpt += 1
        grid += to_add
        #
        grid[0, :] = 0
        grid[n1 - 1, :] = 0
        grid[:, 0] = 0
        grid[:, n2 - 1] = 0
        #
        flashes = np.logical_and((grid > 9), np.logical_not(flashed))
        #
        n_new_flashes = np.sum(np.sum(flashes))
        cond = n_new_flashes > 0
        if cond:
            n_flashed += n_new_flashes
            #
            flashed = np.logical_or(flashed, flashes)
            #
            list_points = np.argwhere(flashes)
            #
            to_add = np.zeros((n1, n2), dtype=int)
            for i_point in range(list_points.shape[0]):
                to_add_indiv = np.zeros((n1, n2), dtype=bool)
                x1, x2 = list_points[i_point, :]
                to_add_indiv[x1 - 1, x2 - 1 : x2 + 2] = True
                to_add_indiv[x1 + 1, x2 - 1 : x2 + 2] = True
                to_add_indiv[x1 - 1 : x1 + 2, x2 - 1] = True
                to_add_indiv[x1 - 1 : x1 + 2, x2 + 1] = True
                to_add += to_add_indiv.astype(int)
    #
    grid[flashed] = 0
    grid_out = np.zeros((n1_temp, n2_temp), dtype=int)
    grid_out = grid[1 : n1_temp + 1, 1 : n2_temp + 1]
    #
    return grid_out, n_flashed


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    grid = get_data(path)
    #
    total: int = 0
    n_steps = 100
    #
    cond = True
    i = 0
    while cond:
        i += 1
        grid, n_flashed = apply_one_step(grid, debug=False)
        # print(i, n_flashed, grid.shape[0], grid.shape[1])
        if n_flashed == grid.size:
            cond = True
            print("result", i)
            break
        total += n_flashed
