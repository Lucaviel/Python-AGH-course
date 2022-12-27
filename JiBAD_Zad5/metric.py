from math import sqrt


def euclidian_distance(vector1, vector2):  # odległość euklidesowa
    difference = vector1 - vector2
    vectors_power = difference * difference
    return sqrt(vectors_power.sum())


def taxicab_distance(vector1, vector2):  # odległość taksówkowa
    difference = abs(vector1 - vector2)
    return difference.sum()


def maximum_distance(vector1, vector2):  # odległość maksimum
    difference = abs(vector1 - vector2)
    return difference.max()


def cosine_distance(vector1, vector2):  # odległość cosinusowa
    vectors_power = (vector1 * vector2).sum()
    power1 = sqrt((vector1 * vector1).sum())
    power2 = sqrt((vector2 * vector2).sum())
    return vectors_power / (power1 * power2)
