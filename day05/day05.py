import os
from typing import List, Tuple

import numpy as np

TYPE_COORDS = Tuple[int, int]
TYPE_SEGMENT = Tuple[TYPE_COORDS, TYPE_COORDS]
TYPE_SEGMENT_LIST = List[TYPE_SEGMENT]


def get_data(path: str) -> TYPE_SEGMENT_LIST:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    segments: List[Tuple[TYPE_COORDS, TYPE_COORDS]] = []
    #
    for line in data:
        beg, end = line.rstrip("\n").split("->")
        temp0, temp1 = beg.split(",")
        x0 = int(temp0)
        y0 = int(temp1)
        #
        temp0, temp1 = end.split(",")
        x1 = int(temp0)
        y1 = int(temp1)
        #
        segments.append(((x0, y0), (x1, y1)))
    return segments


def get_xmax_ymax(segments: TYPE_SEGMENT_LIST) -> Tuple[float, float]:
    xmax = 0
    ymax = 0
    #
    for (x0, y0), (x1, y1) in segments:
        xmax = max(x0, xmax)
        xmax = max(x1, xmax)
        ymax = max(y0, ymax)
        ymax = max(y1, ymax)
    #
    return xmax, ymax


def count_grid(segments: TYPE_SEGMENT_LIST, skip_slanted: bool = True) -> int:
    xmax, ymax = get_xmax_ymax(segments)
    #
    grid = np.zeros((ymax + 1, xmax + 1), dtype=int)
    #
    for (x0, y0), (x1, y1) in segments:
        if x0 == x1:
            ymin = min(y0, y1)
            ymax = max(y0, y1)
            for y in range(ymin, ymax + 1, 1):
                grid[y, x0] += 1
        elif y0 == y1:
            xmin = min(x0, x1)
            xmax = max(x0, x1)
            for x in range(xmin, xmax + 1, 1):
                grid[y0, x] += 1
        else:
            if x0 < x1:
                xbeg, ybeg = x0, y0
                xend, yend = x1, y1
            else:
                xbeg, ybeg = x1, y1
                xend, yend = x0, y0
            if (yend - ybeg) > 0:
                coeff = 1
            else:
                coeff = -1
            for i in range(0, xend - xbeg + 1, 1):
                x = xbeg + i
                y = ybeg + coeff * i
                grid[y, x] += 1
    #
    res = np.sum(np.sum(grid >= 2))
    return res


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    segments = get_data(path)
    #
    res = count_grid(segments, skip_slanted=True)
    print(res)
