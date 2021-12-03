import os

import numpy as np

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "input.txt")
    print(os.path.exists(path))
    #
    with open(path, "r") as f:
        data = f.readlines()

    numbers = []
    for ii in data:
        numbers.append(int(ii))
    n = len(numbers)
    numbers_shift = np.asarray(numbers[1:n])
    numbers_prev = np.asarray(numbers[0 : n - 1])
    diff = numbers_shift - numbers_prev
    res = (diff > 0).sum()
    print(res)
    #
    numbers = np.asarray(numbers)
    numbers_avg = np.zeros((n - 2,), dtype=int)
    for i in range(n - 2):
        numbers_avg[i] = sum(numbers[i : i + 3])
    print(numbers_avg)
    numbers_avg_prev = numbers_avg[0 : n - 3]
    numbers_avg_shift = numbers_avg[1 : n - 2]
    diff = numbers_avg_shift - numbers_avg_prev
    res = (diff > 0).sum()
    print(res)
