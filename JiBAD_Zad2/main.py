class Graph:
    def __init__(self):     #tworzymy słownik, który bedzie grafem
        self._graph_dict = {}

    def add_vertex(self, vertex):   #dodawanie wierzchołków
        if vertex not in self._graph_dict:
            self._graph_dict.[vertex] = set()
        else: raise ValueError("Wierzchołek " + str(vertex) + " juz istnieje.")

    def del_vertex(self, vertex):   #usuwanie wierzchołka
        try:
            for x in self._graph_dict:
                if vertex in self._graph_dict[x]:       #usuwanie krawędzi wychodzących z wierzchołka
                    self._graph_dict[x].remove(vertex)
            del self._graph_dict[vertex]
        except KeyError:
            print("Nie istnieje wierzchołek " + str(vertex) + ", zatem nie mozna go usunąć.")  # zamienił stryjek siekierkę na kijek

    def add_edge(self, v1, v2):       #dodawanie krawędzi
        if (v1 in self._graph_dict.keys()) & (v2 in self._graph_dict.keys()):  # and i & to nie to samo
            for x, y in [(v1, v2), (v2, v1)]:
                self._graph_dict[x].add(y)
        else: print("Nie można dodać krawędzi (" + str(v1) + ", " + str(v2) + "). \nDodaj odpowiednie wierchołki.")

    def del_edge(self, v1, v2):       #usuwanie krawędzi
        for x, y in [(v1, v2), (v2, v1)]:
            if x not in self._graph_dict[y]:
                print("Nie można usunąć krawędzi (" + str(v1) + ", " + str(v2) + ", gdyż taka krawędź nie istnieje")
                break
            else: self._graph_dict[y].remove(x)

    def neighbourhood(self, vertex):    #pobieranie sąsiedztwa pewnego wierzchołka
        try:
            return self._graph_dict[vertex]
        except KeyError:
            print("Nie istnieje wierzchołek " + str(vertex) + ", zatem nie można pobrać jego sąsiadów.")

    def print(self):    #opcja wyświetlenia grafu
        print(self._graph_dict)

    def visiting_node(self, visited, vertex):   #funkcja dodająca odwiedzone wierzchołki w algorytmie dfs
        self.visited.append(vertex)             #oznaczamy wierzchołek v jako odwiedzony
        for v in self._graph_dict[vertex]:      #będziemy przechodzić przez dzieci wierzchołka v
            if v not in self.visited:           #i sprawdzać, czy zostały odwiedzone czy nie
                self.visiting_node(self.visited, v)

    def dfs(self, vertex):
        self.visited = []                                       #lista odwiedzonych wierzchołki
        if vertex not in self._graph_dict.keys():
            print("Nie istnieje wierzchołek" + str(vertex))
        elif (len(self._graph_dict[vertex]) != 0):
            self.visiting_node(self.visited, vertex)
        else: print(str(vertex) + " to samotny wierzchołek.")
        return GraphIterator(self.visited[::-1])

    def bfs(self, vertex):
        self.visited = []                                   #lista odwiedzonych wierzchołków
        i = 0
        if vertex not in self._graph_dict.keys():
            print("Nie istnieje wierzchołek" + str(vertex))
        elif (len(self._graph_dict[vertex]) != 0):
            self.visited.append(vertex)                     #dodajemy odwiedzony wierzchołek
            while True:
                try:
                    for n in self._graph_dict[self.visited[i]]: #przechodzimy po kolei sąsiadów odwiedzonych wierzchołkow
                        if n not in self.visited:               #jeżeli nie zostali odwiedzeni
                            self.visited.append(n)              #to oznaczamy ich jako odwiedzonych
                    i += 1                                      #sprawdzilismy jedno sąsiedztwo
                except IndexError:                              #jeżeli sprawdzimy już sąsiedztwa wszystkich
                    break                                       #kończymy
        else: print(str(vertex) + " to samotny wierzchołek.")
        return GraphIterator(self.visited[::-1])

class GraphIterator:
    def __init__(self, graph):
        self.graph = graph
        self.order = list(range(len(graph)))

    def __next__(self):
        try:
            return self.graph[self.order.pop()]
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self

if __name__ == '__main__':
    graph1 = Graph()

    for i in range(7):
        graph1.add_vertex(i + 1)

    graph1.add_edge(1, 6)
    graph1.add_edge(2, 3)
    graph1.add_edge(2, 4)
    graph1.add_edge(2, 5)
    graph1.add_edge(5, 6)
    graph1.add_edge(3, 6)
    graph1.print()

    graph1.del_vertex(10)

    hood = graph1.neighbourhood(3);
    print(hood)

    print('\n')
    for value in graph1.dfs(2):
        print(value, end=' ')

    print('\n')
    for value in graph1.bfs(2):
        print(value, end=' ')
