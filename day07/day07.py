import os
from typing import Tuple

import numpy as np


def get_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    list_numbers = np.asarray(data[0].rstrip("\n").split(","), dtype=int)
    unique, counts = np.unique(list_numbers, return_counts=True)
    #

    return unique, counts


def get_distance(target: int, unique: np.ndarray, counts: np.ndarray) -> int:
    distance = np.abs(unique - target)
    cost = np.zeros((distance.shape[0],), dtype=int)
    for i in range(distance.shape[0]):
        dist = distance[i]
        cost[i] = np.sum(np.arange(dist + 1))
    return np.sum(counts * cost)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    unique, counts = get_data(path)
    #
    best = get_distance(0, unique, counts)
    pos = 0
    for i in np.arange(unique[0], unique[-1], step=1):
        distance = get_distance(i, unique, counts)
        if distance < best:
            best = distance
            pos = i
    print(pos, best)
