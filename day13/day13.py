import os
from typing import List, Tuple

import numpy as np

TYPE_COORD = Tuple[int, int]
TYPE_LIST_COORD = List[TYPE_COORD]
TYPE_FOLD = Tuple[str, int]
TYPE_LIST_FOLD = List[TYPE_FOLD]


def get_data(path: str) -> Tuple[TYPE_LIST_COORD, TYPE_LIST_FOLD]:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    list_coordinates: TYPE_LIST_COORD = []
    list_folds: TYPE_LIST_FOLD = []
    #
    is_coordinate = True
    #
    for line in data:
        if line == "\n":
            is_coordinate = False
            continue
        if is_coordinate:
            x, y = line.rstrip("\n").split(",")
            new_coord = (int(x), int(y))
            list_coordinates.append(new_coord)
        else:
            beg, end = line.rstrip("\n").split("=")
            direction = beg[-1]
            offset = int(end)
            list_folds.append((direction, offset))
    #
    return list_coordinates, list_folds


def fill_grid(list_coords: TYPE_LIST_COORD) -> np.ndarray:
    #
    xmax = 0
    ymax = 0
    for x, y in list_coords:
        xmax = max(x, xmax)
        ymax = max(y, ymax)
    #
    xmax += 1
    ymax += 1
    #
    arr = np.zeros((ymax, xmax), dtype=bool)
    #
    for x, y in list_coords:
        arr[y, x] = True

    return arr


def fold_y(arr: np.ndarray, yfold: int) -> np.ndarray:
    y, x = arr.shape
    #
    if yfold < ((y - 1) / 2):
        raise ValueError("yfold too small")
    #
    n_below = y - yfold

    for i in range(n_below):
        arr[yfold - i, :] = np.logical_or(arr[yfold - i, :], arr[yfold + i])

    return arr[:yfold, :]


def fold_x(arr: np.ndarray, xfold: int) -> np.ndarray:
    y, x = arr.shape
    #
    if xfold < ((x - 1) / 2):
        raise ValueError("xfold too small")
    #
    n_right = x - xfold

    for i in range(n_right):
        arr[:, xfold - i] = np.logical_or(arr[:, xfold - i], arr[:, xfold + i])

    return arr[:, :xfold]


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    list_coords, list_folds = get_data(path)
    #
    arr = fill_grid(list_coords)
    #
    n_folds = len(list_folds)
    for i, (direction, fold) in enumerate(list_folds):
        if direction == "y":
            arr = fold_y(arr, fold)
        elif direction == "x":
            arr = fold_x(arr, fold)
        print("===========")
        print(np.sum(np.sum(arr)))
        if i == n_folds - 1:
            print(arr.astype(int))
            z = arr.shape[0]
            for j in range(z):
                line = arr[j, :].astype(int).tolist()
                # print(line)
                word = ""
                for k in line:
                    if k == 1:
                        word += "#"
                    else:
                        word += "."
                print(word)
