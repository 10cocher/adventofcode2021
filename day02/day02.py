import os
from typing import List, Tuple

import numpy as np


def compute_final_pos(list_instr: List[Tuple[str, int]]) -> np.ndarray:
    a = np.zeros((3,))
    #
    for direction, increment in list_instr:
        if direction == "forward":
            a[0] = a[0] + increment
            a[1] = a[1] + increment * a[2]
        elif direction == "up":
            a[2] = a[2] - increment
        elif direction == "down":
            a[2] = a[2] + increment
    #
    print(a, a[0] * a[1])
    return a


def compute_final_pos_2(list_instr: List[Tuple[str, int]]) -> np.ndarray:
    a = np.zeros((2,))
    #
    for direction, increment in list_instr:
        if direction == "forward":
            da = np.asarray([1, 0])
        elif direction == "up":
            da = np.asarray([0, -1])
        elif direction == "down":
            da = np.asarray([0, 1])
        a = a + increment * da
    #
    print(a, a[0] * a[1])
    return a


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    print(os.path.exists(path))
    #
    with open(path, "r") as f:
        data = f.readlines()

    list_instr = []
    for i in data:
        temp = i.rstrip("\n").split(" ")
        pos = temp[0]
        a = int(temp[1])
        list_instr.append((pos, a))
        # list_instr.append(
        #    (temp[0], int(temp[1])
        # )

    a = compute_final_pos(list_instr)
