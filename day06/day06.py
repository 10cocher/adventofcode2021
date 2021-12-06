import os

import numpy as np


def get_data(path: str) -> np.ndarray:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    list_numbers = np.asarray(data[0].rstrip("\n").split(","), dtype=int)

    n = 9
    arr = np.zeros((n,), dtype=int)
    #
    for i in range(n):
        arr[i] = np.sum(list_numbers == i)

    return arr


def update(arr: np.ndarray) -> np.ndarray:
    #
    n = 9
    arr2 = np.zeros((n,), dtype=int)
    #
    for i in range(6):
        arr2[i] = arr[i + 1]
    arr2[6] = arr[0] + arr[7]
    arr2[7] = arr[8]
    arr2[8] = arr[0]
    return arr2


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    arr = get_data(path)
    print(arr)

    n_iter = 256
    for i in range(n_iter):
        arr2 = update(arr)
        arr = np.copy(arr2)
    print(np.sum(arr))
