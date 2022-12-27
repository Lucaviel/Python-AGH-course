import numpy as np


def read_data(filename):
    with open(filename) as infile:
        data = np.array([[float(i) for i in line.strip().split()] for line in infile])
        return data[:, :-1], data[:, -1]
