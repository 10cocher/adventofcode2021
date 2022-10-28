import os
from typing import Dict, List, Tuple, Union
import copy

import numpy as np

TYPE_INP = Tuple[str, str]
TYPE_OP = Tuple[str, str, Union[int, str]]
TYPE_INSTR = Union[TYPE_INP, TYPE_OP]
TYPE_LIST_INSTR = List[TYPE_INSTR]

LIST_VARS: List[str] = ["w", "x", "y", "z"]


def read_list_instr(data: List[str]) -> TYPE_LIST_INSTR:
    res: TYPE_LIST_INSTR = []
    n = len(data)
    #
    for i in range(n):
        words = data[i].rstrip("\n").split(" ")
        if len(words) == 2:
            assert words[0] == "inp"
            instr_inp: TYPE_INP = ("inp", words[1])
            res.append(instr_inp)
        else:
            assert words[0] in ["add", "mul", "div", "mod", "eql"]
            par2: Union[str, int]
            if words[2] in LIST_VARS:
                par2 = words[2]
            else:
                par2 = int(words[2])
            instr_op: TYPE_OP = (words[0], words[1], par2)
            res.append(instr_op)

    return res


class Alu:
    def __init__(self, inputs: List[int]) -> None:
        self.variables: Dict[str, int] = {
            "w": np.int32(0),
            "x": np.int32(0),
            "y": np.int32(0),
            "z": np.int32(0),
        }
        self.inputs: List[int] = inputs

    def inp(self, varname: str) -> None:
        new_input = self.inputs.pop(0)
        self.variables[varname] = new_input
        return

    def add(self, var1: str, var2: Union[str, int]) -> None:
        if isinstance(var2, str):
            self.variables[var1] += self.variables[var2]
        else:
            self.variables[var1] += var2
        return

    def mul(self, var1: str, var2: Union[str, int]) -> None:
        if isinstance(var2, str):
            self.variables[var1] *= self.variables[var2]
        else:
            self.variables[var1] *= var2
        return

    def div(self, var1: str, var2: Union[str, int]) -> None:
        num: int = self.variables[var1]
        den: int
        if isinstance(var2, str):
            den = self.variables[var2]
        else:
            den = var2
        if den == 0:
            raise ValueError("Zero denominator!")
        self.variables[var1] = np.int32(float(num) / float(den))
        return

    def mod(self, var1: str, var2: Union[str, int]) -> None:
        num: int = self.variables[var1]
        den: int
        if isinstance(var2, str):
            den = self.variables[var2]
        else:
            den = var2
        if num < 0 or den <= 0:
            raise ValueError(f"bad modulo num={num}, den={den}")
        self.variables[var1] = np.int32(num % den)
        return

    def eql(self, var1: str, var2: Union[str, int]) -> None:
        num: int = self.variables[var1]
        den: int
        if isinstance(var2, str):
            den = self.variables[var2]
        else:
            den = var2
        self.variables[var1] = np.int32(num == den)
        return

    def run_list_instr(self, instrs: TYPE_LIST_INSTR) -> None:
        # print(self.variables)
        for i in instrs:
            # print(self.variables)
            # print(i)
            if len(i) == 2:
                assert i[0] == "inp"
                self.inp(i[1])
            elif len(i) == 3:
                if i[0] == "add":
                    self.add(i[1], i[2])
                elif i[0] == "mul":
                    self.mul(i[1], i[2])
                elif i[0] == "div":
                    self.div(i[1], i[2])
                elif i[0] == "mod":
                    self.mod(i[1], i[2])
                elif i[0] == "eql":
                    self.eql(i[1], i[2])
                else:
                    raise ValueError("Unknown operation")
        return

    def run_list_instr_n(self, instrs: TYPE_LIST_INSTR, n: int) -> Tuple[int, int, int]:
        # print(self.variables)
        cpt_input = 0
        for i in instrs:
            # print(self.variables)
            #print(i)
            if len(i) == 2:
                assert i[0] == "inp"
                #
                cpt_input += 1
                if cpt_input == n+1:
                    x = self.variables["x"]
                    y = self.variables["y"]
                    z = self.variables["z"]
                    return (x, y, z)
                #
                self.inp(i[1])
            elif len(i) == 3:
                if i[0] == "add":
                    self.add(i[1], i[2])
                elif i[0] == "mul":
                    self.mul(i[1], i[2])
                elif i[0] == "div":
                    self.div(i[1], i[2])
                elif i[0] == "mod":
                    self.mod(i[1], i[2])
                elif i[0] == "eql":
                    self.eql(i[1], i[2])
                else:
                    raise ValueError("Unknown operation")

        return (-7, -7, -7)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    with open(path, "r") as f:
        data = f.readlines()
    #
    instrs = read_list_instr(data)
    #
    # number = 13579246899999
    # number_str = str(number)
    # inputs = [int(a) for a in list(number_str)]
    # print(inputs)

    #
    list_digits = [9, 8, 7, 6, 5]#, 4, 3, 2, 1]
    list_numbers = copy.deepcopy(list_digits)
    for n in range(2, 15, 1):
        list_new_numbers = []
        list_res = []
        n_to_test = len(list_numbers)
        log10 = int(np.floor(np.log10(n_to_test)))
        power10 = 10**log10
        print(n_to_test, log10, power10)
        for i_number, number in enumerate(list_numbers):
            if i_number % power10 == 0:
                print(f"  testing {i_number}/{n_to_test} ({number})")
            for digit in list_digits:
                new_number = number * 10 + digit
                new_sequence = [int(a) for a in list(str(new_number))]
                #print(len(new_sequence), new_sequence)
                alu = Alu(new_sequence)
                res = alu.run_list_instr_n(instrs, n=n)
                if res in list_res:
                    continue
                else:
                    list_res.append(res)
                    list_new_numbers.append(new_number)
        list_numbers = copy.deepcopy(list_new_numbers)
        #print(list_numbers)
        print(f"at the endof step {n}, {len(list_new_numbers)} sequences")

        
    print(f"Testing ALL remaining numbers")
    for number in list_numbers:
        inputs = [np.int32(a) for a in list(str(number))]
        if 0 in inputs:
            continue
        #
        alu = Alu(inputs)
        try:
            alu.run_list_instr(instrs)
        except ValueError:
            print(f"{number} error")
        res = alu.variables["z"]
        # if number % 10000 == 1111:
        print(f"{number} : z={res}")
        if res == 0:
            break
