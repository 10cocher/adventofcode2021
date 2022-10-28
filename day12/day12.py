import copy
import os
from typing import Dict, List

import numpy as np


def add_connection(
    cave_to_neighbours: Dict[str, List[str]], start: str, end: str
) -> Dict[str, List[str]]:
    if start not in cave_to_neighbours:
        cave_to_neighbours[start] = []
    cave_to_neighbours[start].append(end)
    return cave_to_neighbours


def get_data(path: str) -> np.ndarray:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    res: Dict[str, List[str]] = {}
    #
    for line in data:
        beg, end = line.rstrip("\n").split("-")
        if beg == "start" or end == "end":
            res = add_connection(res, beg, end)
        elif beg == "end" or end == "start":
            res = add_connection(res, end, beg)
        else:
            res = add_connection(res, beg, end)
            res = add_connection(res, end, beg)
    #
    return res


path = os.path.join(os.getcwd(), "input.txt")
cave_to_neighbours = get_data(path)


def loop_over_neighbours(
    pos: str,
    small_visited: List[str],
    small_visited_twice: List[str],
    count: int,
    caves: List[str],
) -> int:
    # print(f"caves = {caves}")
    list_to_visit = cave_to_neighbours[pos]
    # print(list_to_visit)
    for i in list_to_visit:
        caves_copy = copy.deepcopy(caves)
        small_visited_copy = copy.deepcopy(small_visited)
        small_visited_twice_copy = copy.deepcopy(small_visited_twice)
        if i in small_visited_copy:
            if len(small_visited_twice) > 0:
                continue
            else:
                small_visited_twice_copy.append(i)
        caves_copy.append(i)
        if i == "end":
            # print(f"caves = {caves_copy}")
            count += 1
            continue
        if i.islower():
            small_visited_copy.append(i)
        count = loop_over_neighbours(
            i, small_visited_copy, small_visited_twice_copy, count, caves_copy
        )

    return count


if __name__ == "__main__":
    for k, v in cave_to_neighbours.items():
        print(k, v)
    print("====")

    count: int = 0
    small_visited: List[str] = []
    small_visited_twice: List[str] = []
    caves: List[str] = []
    caves.append("start")
    pos = "start"
    count = loop_over_neighbours(pos, small_visited, small_visited_twice, count, caves)
    print(count)
