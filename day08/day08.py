import os
from typing import Dict, List, Tuple

TYPE_INPUT = List[Tuple[List[str], List[str]]]


def get_data(path: str) -> TYPE_INPUT:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    res: TYPE_INPUT = []
    #
    for i in data:
        left, right = i.rstrip("\n").split("|")
        list_left = left.split(" ")
        list_right = right.split(" ")[1:]
        res.append((list_left, list_right))

    return res


def decode_line(list_words: List[str]) -> Dict[str, str]:  # noqa: C901
    list_letters: List[str] = ["a", "b", "c", "d", "e", "f", "g"]
    possible_values: Dict[str, List[str]] = {
        letter: list_letters for letter in list_letters
    }
    digits_to_letters: Dict[int, List[str]] = {
        1: ["c", "f"],
        4: ["b", "c", "d", "f"],
        7: ["a", "c", "f"],
    }
    length_to_digits: Dict[int, int] = {2: 1, 4: 4, 3: 7}
    #
    for w in list_words:
        if len(w) in [2, 3, 4]:
            wrong_letters: List[str] = list(w)
            true_digit: int = length_to_digits[len(w)]
            true_letters: List[str] = digits_to_letters[true_digit]
            for letter in true_letters:
                possible_values[letter] = [
                    i for i in possible_values[letter] if i in wrong_letters
                ]
    # print("=================")
    if possible_values["c"] == possible_values["f"]:
        to_remove = possible_values["c"]
        for letter in list_letters:
            if letter not in ["c", "f"]:
                possible_values[letter] = [
                    i for i in possible_values[letter] if i not in to_remove
                ]
    #
    # for k, v in possible_values.items():
    #    print(k, v)
    #
    # print("=================")
    for i, values in possible_values.items():
        if len(values) == 1:
            for j in list_letters:
                if j != i:
                    possible_values[j] = [
                        k for k in possible_values[j] if k != values[0]
                    ]
    # for k, v in possible_values.items():
    #    print(k, v)
    #
    # print("=================")
    for i, values in possible_values.items():
        if len(values) == 2:
            for j, values_j in possible_values.items():
                if j > i and (values_j == values):
                    for letter in list_letters:
                        if letter not in [i, j]:
                            possible_values[letter] = [
                                k for k in possible_values[letter] if k not in values
                            ]
    # for k, v in possible_values.items():
    #    print(k, v)
    #
    # print("=================")
    cannot_be_single_missing = ["a", "b", "f", "g"]
    for w in list_words:
        if len(w) == 6:
            missing = [i for i in list_letters if i not in list(w)][0]
            for k, v in possible_values.items():
                if k in cannot_be_single_missing:
                    possible_values[k] = [j for j in v if j != missing]
    # for k, v in possible_values.items():
    #    print(k, v)
    # print("=================")
    for i, values in possible_values.items():
        if len(values) == 1:
            for j in list_letters:
                if j != i:
                    possible_values[j] = [
                        k for k in possible_values[j] if k != values[0]
                    ]
    # for k, v in possible_values.items():
    #    print(k, v)
    # print("=================")

    for k, v in possible_values.items():
        if len(v) > 1:
            raise Exception("Too many possible vals for k")
    #
    return {k: v[0] for k, v in possible_values.items()}


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    data = get_data(path)
    #
    letters_to_digits = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }
    #
    cpt = 0
    for left, right in data:
        list_letters = left
        list_letters.extend(right)
        mapping = decode_line(list_letters)
        mapping2 = {v: k for k, v in mapping.items()}
        #
        true_res = ""
        for word in right:
            wrong_letters = list(word)
            true_letters = [mapping2[letter] for letter in wrong_letters]
            true_letters.sort()
            true_string = "".join(true_letters)
            true_digit = letters_to_digits[true_string]
            true_res += true_digit
        print(true_res)
        cpt += int(true_res)
    print(cpt)
