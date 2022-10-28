import os
from typing import List, Tuple

import numpy as np

TYPE_RANGE = Tuple[int, int]
TYPE_RANGES = Tuple[TYPE_RANGE, TYPE_RANGE, TYPE_RANGE, bool]
TYPE_INSTRUCTIONS = List[TYPE_RANGES]


def parse_range(a: str) -> TYPE_RANGE:
    bounds = a[2:].split("..")
    return int(bounds[0]), int(bounds[1])


def parse_input(data: List[str]) -> TYPE_INSTRUCTIONS:
    res: TYPE_INSTRUCTIONS = []
    #
    for line in data:
        a = line.rstrip("\n").split(" ")
        onoff: bool
        if a[0] == "on":
            onoff = True
        elif a[0] == "off":
            onoff = False
        else:
            raise ValueError(f"Unknown '{a[0]}'")
        #
        strx, stry, strz = a[1].split(",")
        rangex = parse_range(strx)
        rangey = parse_range(stry)
        rangez = parse_range(strz)
        res.append((rangex, rangey, rangez, onoff))

    return res


def is_range_ok_for_part1(a: TYPE_RANGE) -> bool:
    cond1 = a[0] >= -50
    cond2 = a[0] <= 50
    cond3 = a[1] >= -50
    cond4 = a[1] <= 50
    return cond1 and cond2 and cond3 and cond4


def to_positives(a: TYPE_RANGE) -> TYPE_RANGE:
    return a[0] + 50, a[1] + 51


def part1(instructions: TYPE_INSTRUCTIONS) -> int:
    cube = np.zeros((101, 101, 101), dtype=bool)
    #
    for rangex, rangey, rangez, onoff in instructions:
        if not is_range_ok_for_part1(rangex):
            continue
        if not is_range_ok_for_part1(rangey):
            continue
        if not is_range_ok_for_part1(rangez):
            continue
        xmin, xmax = to_positives(rangex)
        ymin, ymax = to_positives(rangey)
        zmin, zmax = to_positives(rangez)
        #
        cube[xmin:xmax, ymin:ymax, zmin:zmax] = onoff

    return np.sum(np.sum(np.sum(cube.astype(int))))


def range_to_new_range(raw_range: TYPE_RANGE, ranges: List[TYPE_RANGE]) -> TYPE_RANGE:
    list_ok = []
    xmin = raw_range[0]
    xmax = raw_range[1]
    for i, r in enumerate(ranges):
        if (r[0] >= xmin) & (r[1] <= xmax + 1):
            # print(f"[{xmin:2}, {xmax:2}]     OK for [{r[0]:2},{r[1]:2}[")
            list_ok.append(i)
        else:
            pass
            # print(f"[{xmin:2}, {xmax:2}] not ok for [{r[0]:2},{r[1]:2}[")
    return list_ok[0], list_ok[-1] + 1


def get_list_ranges(list_points: List[int]) -> List[TYPE_RANGE]:
    res: List[TYPE_RANGE] = []
    #
    n = len(list_points)
    #
    for i in range(n - 1):
        p = list_points[i]
        p_next = list_points[i + 1]
        #
        res.append((p, p + 1))
        if p_next - p > 1:
            res.append((p + 1, p_next))
    last = list_points[n - 1]
    res.append((last, last + 1))
    return res


def get_smart_grid(instructions: TYPE_INSTRUCTIONS, crop50: bool = True) -> int:
    listx: List[int] = []
    listy: List[int] = []
    listz: List[int] = []
    #
    for rangex, rangey, rangez, _ in instructions:
        listx.extend([rangex[0], rangex[1]])
        listy.extend([rangey[0], rangey[1]])
        listz.extend([rangez[0], rangez[1]])
    #
    listx = sorted(list(set(listx)))
    listy = sorted(list(set(listy)))
    listz = sorted(list(set(listz)))
    #
    rangesx: List[TYPE_RANGE] = get_list_ranges(listx)
    rangesy: List[TYPE_RANGE] = get_list_ranges(listy)
    rangesz: List[TYPE_RANGE] = get_list_ranges(listz)
    #
    nx = len(rangesx)
    ny = len(rangesy)
    nz = len(rangesz)
    print("nx ny nz", nx, ny, nz)
    # print(rangesz)
    #
    countx = np.asarray([r[1] - r[0] for r in rangesx], dtype=int)
    county = np.asarray([r[1] - r[0] for r in rangesy], dtype=int)
    countz = np.asarray([r[1] - r[0] for r in rangesz], dtype=int)
    #
    arry = np.zeros((ny, nz), dtype=int)
    arrz = np.zeros((ny, nz), dtype=int)
    for iy in range(ny):
        arry[iy, :] = countz
    for iz in range(nz):
        arrz[:, iz] = county
    arr = arry * arrz
    #
    cube = np.zeros((nx, ny, nz), dtype=bool)
    #
    for rangex, rangey, rangez, onoff in instructions:
        if crop50:
            if not is_range_ok_for_part1(rangex):
                continue
            if not is_range_ok_for_part1(rangey):
                continue
            if not is_range_ok_for_part1(rangez):
                continue
        xmin, xmax = range_to_new_range(rangex, rangesx)
        ymin, ymax = range_to_new_range(rangey, rangesy)
        zmin, zmax = range_to_new_range(rangez, rangesz)
        cube[xmin:xmax, ymin:ymax, zmin:zmax] = onoff

    total = 0
    for ix in range(nx):
        total += np.sum(np.sum(np.squeeze(cube[ix, :, :]) * arr)) * countx[ix]
    return total


if __name__ == "__main__":
    filename = "input"
    path = os.path.join(os.getcwd(), f"{filename}.txt")
    #
    with open(path, "r") as f:
        data = f.readlines()

    instructions = parse_input(data)

    res = part1(instructions)
    print(res)
    res2 = get_smart_grid(instructions, crop50=False)
    print(res2)
