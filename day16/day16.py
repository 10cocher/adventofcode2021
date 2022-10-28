import copy
import os
from typing import List, Tuple, Union

import numpy as np

TYPE_LITERAL = Tuple[List[int], int, str]

HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def get_data(path: str) -> str:
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    return data[0].rstrip("\n")


def convert_to_bin(hex_str: str) -> str:
    list_char = list(hex_str)
    res = ""
    for char in list_char:
        res += HEX_TO_BIN[char]
    return res


def decode_literal(a: str) -> Tuple[int, str]:
    numbers = copy.deepcopy(a)
    #
    ok = True
    res_bin = ""
    while ok:
        ok = numbers[0] == "1"
        res_bin += numbers[1:5]
        numbers = numbers[5:]
    return int(res_bin, 2), numbers


def decode_subpackets_0(
    a: str, memory_version: List[int]
) -> Tuple[List[int], List[int], str]:
    remaining = copy.deepcopy(a)
    list_numbers: List[int] = []
    #
    while len(remaining) > 0:
        print(remaining)
        res = decode(remaining, memory_version)
        if len(res) == 3:
            memory_version, literal, remaining = res
            list_numbers.append(literal)
        elif len(res) == 4:
            memory_version, remaining, result, _ = res
            list_numbers.append(result)
            # print("debug0", memory_version, remaining)
            # raise ValueError("I do not know subpackets_0!")
    # print(f"list_versions = {list_versions}")
    return memory_version, list_numbers, remaining


def decode_subpackets_1(
    a: str, n_subpackets: int, memory_version: List[int]
) -> Tuple[List[int], List[int], str]:
    remaining = copy.deepcopy(a)
    list_numbers: List[int] = []
    # list_version: List[int] = []
    #
    for subpacket in range(n_subpackets):
        res = decode(remaining, memory_version)
        if len(res) == 3:
            memory_version_temp, literal, remaining = res
            # memory_version.extend(memory_version_temp)
            # list_version.append(version)
            list_numbers.append(literal)
        elif len(res) == 4:
            memory_version_temp, remaining, result, _ = res
            list_numbers.append(result)
            # print("debug1", memory_version, remaining)
            # raise ValueError("I do not know subpackets_1!")
    return memory_version, list_numbers, remaining


def decode(
    a: str, memory_version: List[int]
) -> Union[TYPE_LITERAL, Tuple[List[int], str, int, int]]:
    version = int(a[0:3], 2)
    type_id = int(a[3:6], 2)
    memory_version.append(version)
    print("==========")
    print(f"version = {version}")
    print(f"type_id = {type_id}")
    print(f"memory_version = {memory_version}")
    if type_id == 4:
        literal, remaining = decode_literal(a[6:])
        print(f"literal = {literal} ; remaining = {remaining}")
        return memory_version, literal, remaining
    else:
        length_type_id = a[6]
        print(f"length_tpye_id = {length_type_id}")
        if length_type_id == "0":
            length = int(a[7:22], 2)
            print(f"length={length}")
            list_version, list_numbers, _ = decode_subpackets_0(
                a[22 : 22 + length], memory_version
            )
            print(list_numbers)
            remaining = a[22 + length :]
        elif length_type_id == "1":
            n_subpackets = int(a[7:18], 2)
            print(f"n_subpackets={n_subpackets}")
            remaining = a[18:]
            list_version, list_numbers, remaining = decode_subpackets_1(
                a[18:], n_subpackets, memory_version
            )
            print(list_numbers)
        array = np.asarray(list_numbers, dtype=int)
        if type_id == 0:
            print(f"I am making the sum of {array}")
            result = np.sum(array)
        elif type_id == 1:
            print(f"I am making the prod of {array}")
            result = np.prod(array)
        elif type_id == 2:
            result = np.amin(array)
        elif type_id == 3:
            result = np.amax(array)
        elif type_id == 5:
            assert array.shape[0] == 2
            result = int(array[0] > array[1])
        elif type_id == 6:
            assert array.shape[0] == 2
            result = int(array[0] < array[1])
        elif type_id == 7:
            print("array", array)
            assert array.shape[0] == 2
            result = int(array[0] == array[1])
        else:
            raise ValueError("unkown type_id")
    return memory_version, remaining, result, 0


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    input_hex = get_data(path)
    # input_hex = "C200B40A82"
    # input_hex = "04005AC33890"
    # input_hex = "880086C3E88112"
    # input_hex = "CE00C43D881120"
    # input_hex = "D8005AC2A8F0"
    # input_hex = "F600BC2D8F"
    # input_hex = "9C005AC2F8F0"
    # input_hex = "9C0141080250320F1802104A08"
    print(input_hex)
    input_bin = convert_to_bin(input_hex)
    print(input_bin)
    #
    memory_version: List[int] = []
    #
    res = decode(input_bin, memory_version)
    if len(res) == 4:
        (memory_version, remaining, result, _) = res
        sum_versions = np.sum(np.asarray(memory_version), dtype=int)
        print(f"sum_versions = {sum_versions}, result = {result}")
