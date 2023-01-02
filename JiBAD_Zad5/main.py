import numpy as np
from reader import read_data
from collections import Counter
import metric
import view  # circular import
from warnings import warn

SET = "bazadanych.txt"
PROBA = "proba.txt"


class Neighbours:               # klasa opisująca punkty/sąsiadów

    def __init__(self, style, distance):
        self.style = style
        self.distance = distance


def train(sample, function_name):  # a to nie powinna być metoda? train nie robi tego, co miało robić
    data, labels = read_data(SET)           # pobranie danych - współrzędne punktów i etykiety  # a czemu z pliku, którego nazwy nie kontroluję?
    func = getattr(metric, function_name)   # ustalenie metryki z modułu metric  # nazwa func
    sort_distances = []                     # tablica obiektów klasy Neighbours
    count = len(data)                               # liczenie sąsiadów
    for row in data:
        distance = func(sample, row)        # policzenie odległości wg wybranej wcześniej metryki
        sort_distances.append(Neighbours(labels[count], distance))
    sort_distances.sort(key=lambda x: x.distance, reverse=False)    # posortowanie tablicy wg długości od najmniejsze
    return sort_distances


def predict(vectors):
    count_sets = Counter(x.style for x in vectors)      # liczymy ilość sąsiadów dla danej etykiety
    return max(count_sets, key=count_sets.get)          # zwracamy etykietę o największej liczbie sąsiadów


def kNN(k, sample):
    neighbourhood = view.menu(sample)
    try:
        last_neighbour = neighbourhood[k - 1]           # znalezienie k-tego sąsiada
    except IndexError:
        warn("Nie ma tylu sąsiadów. Obliczenia zostaną przeprowadzone dla wszystkich punktów.")
        last_neighbour = neighbourhood[len(neighbourhood)-1]
    # wybranie sąsiadów, którzy są w odległości mniejszej bądź równej od k-tego sąsiada
    selected_neighbourhood = [x for x in neighbourhood if x.distance <= last_neighbour.distance]
    return predict(selected_neighbourhood)


if __name__ == "__main__":
    parameter = input("Podaj liczbę sąsiadów: ")             # np. 5
    example = input("Podaj trzy informacje o próbce: ")      # np. 0.54 0.76 0.43
    example_vector = list(map(float, example.split()))
    example_class = kNN(int(parameter), np.array(example_vector))
    print("Próbka należy do klasy " + str(example_class))
