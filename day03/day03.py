import os

import numpy as np
import pandas as pd


def bin_to_dec(a: np.ndarray) -> int:
    n = len(a)
    powers = 2 ** np.flip(np.arange(n))
    res = np.sum(a * powers)
    print(res)
    return res


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    print(os.path.exists(path))
    #
    with open(path, "r") as f:
        data = f.readlines()
    #
    #
    n = len(data)
    n2 = len(data[0].rstrip("\n"))
    print(n, n2)
    arr = np.zeros((n2,), dtype=int)
    #
    df = pd.DataFrame(columns=range(n2))
    for word in data:
        digits = list(word.rstrip("\n"))
        digits = np.asarray(digits, dtype=int)
        s = pd.Series(data=digits, index=range(n2))
        df = df.append(s, ignore_index=True)
        arr += digits
    print(df)
    #
    most_common = np.zeros((n2,), dtype=int)
    least_common = np.ones((n2,), dtype=int)
    for i in range(n2):
        if arr[i] > n / 2.0:
            most_common[i] = 1
            least_common[i] = 0
    # print(most_common)
    # print(least_common)

    gamma = bin_to_dec(most_common)
    epsilon = bin_to_dec(least_common)
    # print(gamma*epsilon)
    #
    df2 = df.copy()
    for i in range(n2):
        # print(f"digit {i}")
        s = df2[i].sum()
        # print(df2[i])
        # print(s)
        if s >= len(df2) / 2:
            mask = df2[i] == 1
            # print("keep 1")
        else:
            mask = df2[i] == 0
            # print("keep 0")
        df2 = df2.loc[mask, :]
        # print(df2)
        if len(df2) < 2:
            break
    print("===========")
    print(df2)
    oxygen = df2.iloc[0, :].to_numpy()
    print(oxygen)

    #
    df3 = df.copy()
    for i in range(n2):
        # print(f"digit {i}")
        s = df3[i].sum()
        # print(df3[i])
        # print(s)
        if s >= len(df3) / 2:
            mask = df3[i] == 0
            # print("keep 0")
        else:
            mask = df3[i] == 1
            # print("keep 1")

        df3 = df3.loc[mask, :]
        # print(df3)
        if len(df3) < 2:
            break
    print("===========")
    print(df3)
    co2 = df3.iloc[0, :].to_numpy()
    #
    a = bin_to_dec(oxygen)
    b = bin_to_dec(co2)
    print(a)
    print(b)
    print(a * b)
