import os
from typing import List, Tuple

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
    #
    for i, line in enumerate(data):
        arr[i, :] = np.asarray(list(line.rstrip("\n")), dtype=int)

    return arr


def get_mins_locations(arr: np.ndarray) -> int:
    n1, n2 = arr.shape
    #
    arr_up = np.zeros((n1, n2), dtype=int) + 10
    arr_up[1:, :] = arr[0 : n1 - 1, :]
    #
    arr_down = np.zeros((n1, n2), dtype=int) + 10
    arr_down[: n1 - 1, :] = arr[1:, :]
    #
    arr_left = np.zeros((n1, n2), dtype=int) + 10
    arr_left[:, : n2 - 1] = arr[:, 1:]
    #
    arr_right = np.zeros((n1, n2), dtype=int) + 10
    arr_right[:, 1:] = arr[:, : n2 - 1]
    #
    cond_up = arr_up > arr
    cond_down = arr_down > arr
    cond_left = arr_left > arr
    cond_right = arr_right > arr
    mask = cond_up & cond_down & cond_left & cond_right
    return mask


def part1(arr: np.ndarray) -> int:
    #
    n1, n2 = arr.shape
    mask = get_mins_locations(arr)
    mins = np.zeros((n1, n2), dtype=int)
    mins[mask] = arr[mask] + 1
    #
    res = np.sum(np.sum(mins))
    return res


def find_new_points(
    arr: np.ndarray, basin: np.ndarray, points: List[Tuple[int, int]]
) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    n1, n2 = arr.shape
    #
    new_points: List[Tuple[int, int]] = []
    #
    for y0, x0 in points:
        # ==============================
        for y in np.arange(y0 + 1, n1, 1):
            if arr[y, x0] == 9:
                break
            if not basin[y, x0]:
                new_points.append((y, x0))
                basin[y, x0] = True
        # ==============================
        for y in np.arange(y0 - 1, -1, -1):
            if arr[y, x0] == 9:
                break
            if not basin[y, x0]:
                new_points.append((y, x0))
                basin[y, x0] = True
        # ==============================
        for x in np.arange(x0 + 1, n2, 1):
            if arr[y0, x] == 9:
                break
            if not basin[y0, x]:
                new_points.append((y0, x))
                basin[y0, x] = True
        # ==============================
        for x in np.arange(x0 - 1, -1, -1):
            if arr[y0, x] == 9:
                break
            if not basin[y0, x]:
                new_points.append((y0, x))
                basin[y0, x] = True
    return basin, new_points


def size_basin(arr: np.ndarray, xmin: int, ymin: int) -> int:
    n1, n2 = arr.shape
    #
    basin = np.zeros((n1, n2), dtype=bool)
    #
    basin[ymin, xmin] = True
    #
    points: List[Tuple[int, int]] = []
    points.append((ymin, xmin))
    #
    cpt = 0
    while len(points) > 0:
        cpt += 1
        print(f"cpt = {cpt}")
        basin, new_points = find_new_points(arr, basin, points)
        points = new_points

    return np.sum(np.sum(basin))


def part2(arr: np.ndarray) -> int:
    n1, n2 = arr.shape
    mask = get_mins_locations(arr)
    mins = np.argwhere(mask)
    n_mins = mins.shape[0]
    #
    basin_sizes = np.zeros((n_mins,), dtype=int)
    #
    for i_min in range(n_mins):
        print(f"basin {i_min+1:3}/{n_mins:3}")
        y, x = mins[i_min, :]
        basin_sizes[i_min] = size_basin(arr, x, y)
    print(basin_sizes)
    #
    best = np.sort(basin_sizes)[-3:]
    return best[0] * best[1] * best[2]


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    arr = get_data(path)
    # res = part1(arr)
    res = part2(arr)
    print(res)
