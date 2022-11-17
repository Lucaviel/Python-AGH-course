def build(patterns):
    #tworzymy automat
    try:
        patterns = sorted(patterns, key=len)    #sortujemy wzorce od najkrótszego do najdłuższego
    except TypeError:
        print('Wpisuje się we wzorcu tylko napisy/stringiem!')
    # wyjątek "obsłużony", funkcja działa dalej
    dict = {}   #automat  # przesłonięcie nazwy wbudowanej
    fail = {}   #fail-linki
    inside = {} #wzorzec zawierający w środku/na końcu inny wzorzec
    length = [0]
    i = 0       #liczy ilosc wszystkich indexow
    for x in patterns:
        a = 0   #aktualny index  # jeśli trzeba skomentować nazwę zmiennej, to to jest zła nazwa
        for j in range(len(x)+1):
            if not j in x:
                dict[a] = {-1: None}
                break
            if a not in dict.keys():    #tworzymy w dict klucz o danym indexie, jeżeli wcześniej nie istniał
                dict[a] = {}
            if x[j] not in dict[a].keys():
                dict[a].update({x[j]: i+1})
                length.append(j+1)      #pozycje litery w danym słowie
                i += 1
                a = i
            else: a +=1
        for y in patterns:      #sprawdzamy, czy dany wzorzec zawiera inny wzorzec w jego środku badź na końcu
            if y == x: break
            if (x.find(y)) != 0 & x.find(y) != -1 & (y in x):
                inside.update({x: len(x)-x.find(y)})

   #nastepnie słownik fail-linków, dla każego stanu
    state = 0           #aktualna pozycja podczas szukania fail-linka dla danego stanu
    lab = ''            #etykieta

    for x in range(i):  #tworzymy w słowniku fail klucze o indeach ze słownika dict
        fail[x] = {}

    for v in dict.keys():
        if v == 0:
            fail[v] = '*'             #joker
            continue
        if v in dict[0].values():     #dzieci korzenia
            fail[v] = 0
            continue
        for p in dict.keys():         #szukamy rodzica i etykiete aktualnego stanu (wierzchołka) v
            if dict[p] == {-1: None}:
                continue
            elif v in dict[p].values():
                state = fail[p]   #znaleziony rodzic
                lab = [key for (key, value) in dict[p].items() if value == v]   #znaleziona etykieta
                break

        while True:
            if state == '*':    #jak napotyka jokera, to oznacza, że już przeszło przez stan 0 i nie znalazło odpowiedniej etykiety
                fail[v] = 0
                break
            elif lab[0] in dict[state].keys():  #szukamy takiej samej etykiety
                state = dict[state][lab[0]]
                fail[v] = state
                break
            else:
                state = fail[state]     #jeżeli nie znaleźliśmy, to idziemy dalej po fail-linku

    return dict, fail, length, inside

def search(automat, text):
    dict, fail, length, inside = automat
    find = []   #tablica indeksów znalezionych wzorców
    l = 0       #długośc danego wzorca
    s = 0       #stan w jakim się znajdujemy
    try:
        len(text)
    except TypeError:
        print('Tekst może być tylko napisem/stringiem!')  # lista też ma długość
    for i in range(len(text)):
        while True:
            if (dict[s] == {-1: None}) | (text[i] not in dict[s].keys()):   #przechodzenie po fail-linku
                if s != 0:
                    s = fail[s]
                    l = length[s]
                else:
                    l = 0
                    break
            elif text[i] in dict[s].keys():     #znalezienie stanu wg wzorca
                s = dict[s][text[i]]
                l += 1
                if -1 in dict[s].keys():    #znalezienie zakończenia wzorca
                    find.append(i+1-l)
                    if text[(i+1-l):(i+1)] in inside.keys():    #sprawdzenie czy we wzorcu występuje inny
                        find.append(i + 1 - inside[text[(i+1-l):(i+1)]])
                break

    return find

print(search(build(['abc', 'aab', 'cba']), 'aacbabc'))
print(search(build(['he','she','hers','his']), 'ahishers'))
print(search(build(['abcd', 'bc']), 'abcd'))
