import sys

class Graph:
    def __init__(self):
        self._graph_dict = {}

    def add_vertex(self, vertex):   #dodawanie wierzchołków do danego grafu dict
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = {}

    def add_edge(self, current_vertex, next_vertex, label):       #dodawanie krawędzi do danego grafu dict
        if (next_vertex not in self._graph_dict.keys()) and (next_vertex != 'Accept'):
            self.add_vertex(next_vertex)
        if (label not in self._graph_dict[current_vertex].keys()):
            self._graph_dict[current_vertex].update({label: next_vertex})
            return True                                                 #jeżeli krawędź dodana zwracamy True
        else:
            return False                                                #jeśli nie zwracamy False

    def print(self):    #wyświetlenie grafu
        print(self._graph_dict)

    def __getitem__(self, item):    #pobranie wartości słwonik według klucza item
        return self._graph_dict[item]

    def keys(self):                 #pobranie kluczy słownika
        return self._graph_dict.keys()

    def keys_of_key(self, main_key):   #pobranie kluczy klucza state słownika
        return self._graph_dict[main_key].keys()

class AhoCorasick:
    def __init__(self, patterns):
        self._graph_dict = Graph()   #graf z liniami "grubymi"
        self.number_states, self.inside, self.position = self.build(patterns)
        self._fail_link = FailLink(self.number_states,self._graph_dict)  #graf z fail-linkami

    def print(self):    #wyświetlenie grafu
        self._graph_dict.print()

    def build(self, patterns):
        try:
            patterns = sorted(patterns, key=len)  # sortujemy wzorce od najkrótszego do najdłuższego
        except TypeError:
            print('Lista wzorców może byc wypełniona tylko napisami/stringami!')
            sys.exit()

        total_index = 0  #zredukowana liczba wierzchołków,
        position = [0]   #pozycje litery (indeksu listy) w danym słowie
        inside = {}      # słownik wzorców znajdujących się w innym wzorcu
        for word in patterns:
            current_index = 0  # aktualny index grafu, po którym sie poruszamy
            for j in range(len(word) + 1):
                if j >= len(word):
                    self._graph_dict.add_edge(current_index, 'Accept', -1)
                    break
                self._graph_dict.add_vertex(current_index)  # tworzymy w dict klucz o danym indexie
                if self._graph_dict.add_edge(current_index, total_index + 1, word[j]):
                    position.append(j + 1)          #odpowiednim indeksie (literze) nadajemy pozycje we wzorcu
                    total_index += 1                #powiększamy całkowita liczbę indeksów grafu
                    current_index = total_index     #zmieniamy biężącą pozycję na aktualnie całkowitą liczbę indeksów
                else:
                    current_index += 1
            for y in patterns:  # sprawdzamy, czy dany wzorzec zawiera inny wzorzec w jego środku badź na końcu
                if y == word: break
                if (word.find(y)) != 0 and word.find(y) != -1 and (y in word):
                    inside.update({word: len(word) - word.find(y)})

        return total_index, inside, position

    def search(self, text):
        found = []  # tablica indeksów znalezionych wzorców
        pattern_length = 0  # długośc danego wzorca
        vertex = 0  #wierzchołek w jakim aktualnie się znajdujemy
        if(isinstance(text, str)):
            for i in range(len(text)):
                while True:
                    if (self._graph_dict[vertex] == {-1: 'Accept'}) | \
                            (text[i] not in self._graph_dict[vertex].keys()):  # przechodzenie po fail-linku
                        if vertex != 0:
                            vertex = self._fail_link[vertex]
                            pattern_length = self.position[vertex]
                        else:
                            pattern_length = 0
                            break
                    elif text[i] in self._graph_dict[vertex].keys():  # znalezienie stanu wg wzorca
                        vertex = self._graph_dict[vertex][text[i]]
                        pattern_length += 1
                        if -1 in self._graph_dict[vertex].keys():  # znalezienie zakończenia wzorca
                            found.append(i + 1 - pattern_length)
                            if text[(i + 1 - pattern_length):(
                                    i + 1)] in self.inside.keys():  # sprawdzenie czy we wzorcu występuje inny
                                found.append(i + 1 - self.inside[text[(i + 1 - pattern_length):(i + 1)]])
                        break
        else:
            print('Tekst, w którym chcesz znaleźć wzory, może być tylko napisem/stringiem!\n')
            sys.exit()

        return found

    def __repr__(self):
        graph_text = ''
        for parent_vertex in range(self.number_states):
            graph_text += 'wierzchołek ' + str(parent_vertex) + ' jest '
            for edge in self._graph_dict[parent_vertex].keys():
                if edge != -1:
                    graph_text += 'połączony krawędzią "' + str(edge) + '" z wierzchołkiem ' + str(self._graph_dict[parent_vertex][edge]) + ", "
                else:
                    graph_text += 'stanem akceptującym i '
                    continue
            graph_text = graph_text[0:-2]
            graph_text += "\n"
        return graph_text

class FailLink:
    def __init__(self, total_number, dictionary):
        self.fail = self.build(total_number, dictionary)

    def __getitem__(self, item):
        return self.fail[item]

    def build(self, index, dictionary):
        self.fail = {}  #słownik fail-linków, dla każego stanu
        state = 0  #aktualna pozycja podczas szukania fail-linka dla danego stanu
        lab = ''  #etykieta

        for i in range(index):  #tworzymy w słowniku fail klucze o indeach ze słownika dict
            self.fail[i] = {}

        for vertex in dictionary.keys():
            if vertex == 0:
                self.fail[vertex] = '*'  #joker
                continue
            if vertex in dictionary[0].values():  #dzieci korzenia
                self.fail[vertex] = 0
                continue
            for parent in dictionary.keys():  #szukamy rodzica i etykiete aktualnego stanu (wierzchołka) v
                if dictionary[parent] == {-1: None}:
                    continue
                elif vertex in dictionary[parent].values():
                    state = self.fail[parent]  # znaleziony rodzic
                    lab = [key for (key, value) in dictionary[parent].items() if value == vertex]  # znaleziona etykieta
                    break

            while True:
                if state == '*':  # jak napotyka jokera, to oznacza, że już przeszło przez stan 0 i nie znalazło odpowiedniej etykiety
                    self.fail[vertex] = 0
                    break
                elif lab[0] in dictionary.keys_of_key(state):  # szukamy takiej samej etykiety
                    state = dictionary[state][lab[0]]
                    self.fail[vertex] = state
                    break
                else:
                    state = self.fail[state]  # jeżeli nie znaleźliśmy, to idziemy dalej po fail-linku

        return self.fail

if __name__ == '__main__':
    graph1 = AhoCorasick(['he','she','hers','his'])
    print(graph1.search('ahishers'))

    graph2 = AhoCorasick(['abc', 'aab', 'cba'])
    print(graph2.search('aacbabc'))

    graph3 = AhoCorasick(['abcd', 'bc'])
    print(graph3.search('abcd'))

    graph1.print()
    print(repr(graph1))