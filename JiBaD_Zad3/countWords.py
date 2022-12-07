import operator
MARKS = [',', '.', ';', ':', '?','!', '-', '"', '(', ')', '/', '\x84']

def gen_tokens(filename, n):  # przydałaby się jakaś dekompozycja  # myląca nazwa
    with open(filename, 'r', encoding='utf-8') as infile:  #może też być encoding='iso-8859-2', usuwa '\x84' jednak nie odczytuje polskich liter poprawnie
        words_number = {}  # polecam klasę collections.Counter
        for line in infile:
            text = line.split()
            for word in text:
                for mark in MARKS:  #usuwamy znaki interpunkcyjne znajdujce się w liście MARKS
                    if mark in word:
                        word = word.replace(mark, '')  # warto użyć re.sub, albo regex.sub
                word = word.strip()
                if word == '':      #omijanie pustych wyrazów, które powstały poprzez usunięcie pojedynczego znaku interpunkcyjnego
                    continue        #który był uważany jako pojedynczy wyraz
                word = word.lower()
                if word not in words_number.keys():   #jeżeli token nie wystąpił, to dodajemy go do słownika
                    words_number[word] = 1
                else: words_number[word] = words_number[word] + 1   #w innym wypadku zwiększamy ilość jeso wystąpień

        words_number = sorted(words_number.items(), key = operator.itemgetter(1), reverse=True)    #posortowany słownik według wystąpień

        index = 0                   #numer wyrazu w posorotwanej liście
        for place in range(n):      #miejsce w "rankingu" o n miejscach
            try:
                print(str(place+1) + ": " + words_number[index][0] + ", liczba wystąpień: " + str(words_number[index][1]))
                index +=1               #przechodzimy do kolejnego wyrazu
                while True:
                    if(words_number[index-1][1] == words_number[index][1]):     #sprawdzamy, czy jeszcze kolejny wyraz ma tyle samo wystapień
                        print(str(place+1) + ": " + words_number[index][0] + ", liczba wystąpień: " + str(words_number[index][1]))
                        index += 1              #jeśli tak, to przechodzimy do kolejnego
                    else:
                        break
            except IndexError:       #index może wyjść poza listę w dwóch miejscach, co bedzie oznaczało, że skończyły się nam wyrazy w słowniku
                print("Wszystkie wyrazy pokryły mniejszą ilość miejsc.")
                break

if __name__ == '__main__':
    #gen_tokens("tratata.txt", 3)
    #gen_tokens("nkjp.txt", 5)
    gen_tokens("potop.txt", 5)
