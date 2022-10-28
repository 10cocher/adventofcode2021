from typing import Tuple

import numpy as np


def move(xpos: int, ypos: int, xvel: int, yvel: int) -> Tuple[int, int, int, int]:
    xpos += xvel
    ypos += yvel
    if xvel != 0:
        xvel -= np.sign(xvel)
    yvel -= 1
    return xpos, ypos, xvel, yvel


def is_in_area(
    xpos: int, ypos: int, xmin: int, xmax: int, ymin: int, ymax: int
) -> Tuple[bool, bool]:
    condx = (xpos >= xmin) and (xpos <= xmax)
    condy = (ypos >= ymin) and (ypos <= ymax)
    cond = condx & condy
    #
    too_late_x = xpos > xmax
    too_late_y = ypos < ymin
    too_late = too_late_x or too_late_y

    return cond, too_late


def simulate_traj(
    xpos: int,
    ypos: int,
    xvel: int,
    yvel: int,
    xmin: int,
    xmax: int,
    ymin: int,
    ymax: int,
) -> Tuple[bool, int]:
    cond = False
    too_late = False
    #
    highest_y = ypos
    #
    while (not cond) and (not too_late):
        xpos, ypos, xvel, yvel = move(xpos, ypos, xvel, yvel)
        highest_y = max(ypos, highest_y)
        cond, too_late = is_in_area(xpos, ypos, xmin, xmax, ymin, ymax)
        # print(
        #     f"xpos = {xpos:2} ; ypos = {ypos:2} ; cond={cond} ; too_late = {too_late}"
        # )

    return cond, highest_y


def simulate_several_traj(
    xmin: int,
    xmax: int,
    ymin: int,
    ymax: int,
    xvel_min: int,
    xvel_max: int,
    yvel_min: int,
    yvel_max: int,
) -> None:
    best = 0
    count = 0
    for xvel in range(xvel_min, xvel_max):
        print(xvel, xvel_min, xvel_max)
        for yvel in range(yvel_min, yvel_max):
            xpos = 0
            ypos = 0
            cond, highest_y = simulate_traj(
                xpos, ypos, xvel, yvel, xmin, xmax, ymin, ymax
            )
            if cond:
                if highest_y >= best:
                    pass
                    #print(
                    #    f"With xvel={xvel:4} and yvel={yvel:4} cond={cond} and best={best}"
                    #)
                best = max(best, highest_y)
                count += 1
            else:
                pass
                #print(f"With xvel={xvel:4} and yvel={yvel:4} cond={cond}")
    print(f"highest y: {best} (should be 45/19503)")
    print(f"count: {count} (should be 112)")
    return


if __name__ == "__main__":
    if True:
        xmin = 57
        xmax = 116
        ymin = -198
        ymax = -148
    else:
        xmin = 20
        xmax = 30
        ymin = -10
        ymax = -5
    #
    xpos = 0
    ypos = 0
    xvel = 7
    yvel = 2
    #
    # simulate_traj(xpos, ypos, xvel, yvel, xmin, xmax, ymin, ymax)
    xvel_min = -10
    xvel_max = xmax+1
    yvel_min = ymin-1
    yvel_max = 300
    simulate_several_traj(
        xmin, xmax, ymin, ymax, xvel_min, xvel_max, yvel_min, yvel_max
    )
