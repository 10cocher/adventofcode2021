import os
from typing import Dict, List

close_to_open: Dict[str, str] = {">": "<", ")": "(", "]": "[", "}": "{"}
closes = list(close_to_open.keys())
opens = list(close_to_open.values())
close_to_score: Dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
close_to_score2: Dict[str, int] = {"(": 1, "[": 2, "{": 3, "<": 4}


def get_data(path: str) -> List[List[str]]:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    data_out: List[List[str]] = []
    for line in data:
        data_out.append(list(line.rstrip("\n")))
    #
    return data_out


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    data = get_data(path)
    #
    total = 0
    list_scores = []
    for line in data:
        finished = False
        a: List[str] = []
        for char in line:
            if char in opens:
                a.append(char)
            elif char in closes:
                if close_to_open[char] == a[-1]:
                    a = a[:-1]
                else:
                    # print(f"wrong char: {char}")
                    total += close_to_score[char]
                    finished = True
                    break
        if finished:
            continue
        score = 0
        for char in a[::-1]:
            score = score * 5 + close_to_score2[char]
        list_scores.append(score)
    print(total)
    print(list_scores)
    n = len(list_scores)
    n2 = int((n + 1) / 2) - 1
    print(n, n2)
    print(sorted(list_scores)[n2])
