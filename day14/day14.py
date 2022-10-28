import copy
import os
from typing import Dict, List, Tuple


def get_data(path: str) -> Tuple[str, Dict[str, str]]:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    start: str = data[0].rstrip("\n")
    i = 2
    n = len(data)
    #
    pair_to_char: Dict[str, str] = {}
    #
    for i in range(2, n):
        beg, end = data[i].rstrip("\n").split("->")
        beg = beg.strip()
        end = end.strip()
        pair_to_char[beg] = end

    return start, pair_to_char


def insert_chars(word: str, pair_to_char: Dict[str, str]) -> str:
    char_to_insert: List[str] = []
    n = len(word)
    for i in range(n - 1):
        char_to_insert.append(pair_to_char[word[i : i + 2]])
    #
    new_word: str = ""
    #
    for i in range(n - 1):
        new_word += word[i]
        new_word += char_to_insert[i]
    new_word += word[-1]

    return new_word


def measure(word: str) -> int:
    list_chars = list(set(list(word)))
    scores: List[int] = [word.count(char) for char in list_chars]
    #
    maxval = max(scores)
    minval = min(scores)
    res = maxval - minval
    return res


def brute_force(start: str, n_steps: int) -> int:
    word = start
    for i in range(n_steps):
        word = insert_chars(word, pair_to_char)
        print(f"step={i:3}   len(word)={len(word):4}")
    score = measure(word)
    print(f"step={i:3}   len(word)={len(word):4}   score={score:4}")
    return score


def get_list_all_possible_chars(pair_to_char: Dict[str, str]) -> List[str]:
    chars: List[str] = []
    #
    for k, v in pair_to_char.items():
        chars.extend(list(k))
        chars.append(v)
        chars = list(set(chars))

    return chars


def update_count(
    pairs_to_count: Dict[str, int], pairs_to_plus: Dict[str, Tuple[str, str]]
) -> Dict[str, int]:
    res = copy.deepcopy(pairs_to_count)
    #
    for p, count in pairs_to_count.items():
        #
        if count == 0:
            continue
        new0, new1 = pairs_to_plus[p]
        #
        res[p] += -count
        res[new0] += count
        res[new1] += count
    return res


def count(
    chars: List[str], pairs_to_count: Dict[str, int], start_word: str
) -> Dict[str, int]:
    res: Dict[str, int] = {c: 0 for c in chars}
    res[start_word[-1]] += 1
    #
    for pair, count in pairs_to_count.items():
        c = pair[0]
        res[c] += count
    return res


def score_from_dict(char_to_count: Dict[str, int]) -> int:
    scores = list(char_to_count.values())
    return max(scores) - min(scores)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    start, pair_to_char = get_data(path)
    #
    n_steps = 40
    # res = brute_force(start, n_steps)
    # print(f"The result is {res}.")
    chars = get_list_all_possible_chars(pair_to_char)
    #
    list_pairs = list(pair_to_char.keys())

    pairs_to_plus: Dict[str, Tuple[str, str]] = {}
    for p in list_pairs:
        a = p[0]
        b = pair_to_char[p]
        c = p[1]
        pairs_to_plus[p] = (a + b, b + c)

    # Initialize
    pairs_to_count: Dict[str, int] = {p: 0 for p in list_pairs}
    for i in range(len(start) - 1):
        pair = start[i : i + 2]
        pairs_to_count[pair] += 1
    #
    char_to_count = count(chars, pairs_to_count, start)
    # print(char_to_count)
    #
    # Update
    for step in range(n_steps):
        # print(f"=== step {step} ===")
        pairs_to_count = update_count(pairs_to_count, pairs_to_plus)
        char_to_count = count(chars, pairs_to_count, start)
        print(score_from_dict(char_to_count))
        # print(char_to_count)
