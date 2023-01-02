# to nie jest zadanie na jeden plik

from datetime import datetime, timedelta, date

# Pliki
BOOKS = "books.txt"
READERS = "readers.txt"
R_PASSWORDS = 'readers_pass.txt'
LIBRARIANS = "librarians.txt"

# Komunikaty
WRONG_DATA = 'Zostały podane błędne dane!\n'
DATA_UPDATE = ' została zaktualizowana!\n'
INPUT_NAMES = 'Wpisz swoje nazwisko i imię: '
INPUT_PASSWORD = 'Wpisz hasło: '

# Stałe zmienne
LIBRARY = ['Wypożyczona', 'Rezerwacja', 'Data']
RENEW = 20
SEP = "$"


# Funkcje globalne
def reader_login():   # Np. Markowska Patrycja, hasło: 0000
    name, password = input_user_data()
    new_reader = Reader(name, password)
    while new_reader.reader_name is not None:  # mało czytelny sposób sygnalizacji końca
        new_reader.menu()
    del new_reader


def librarian_login():  # np. Nowak Tadeusz, hasło: 0000
    name, password = input_user_data()
    new_librarian = Librarian(name, password)
    while new_librarian.librarian_name is not None:
        new_librarian.menu()
    del new_librarian


def add_data_to_file(file, data):
    with open(file, "a", encoding='utf-8') as data_base:
        data_base.write(data)
    update_notice(file)


def delete_data_from_file(file, data):
    with open(file, "r", encoding='utf-8') as fp:
        lines = fp.readlines()
    with open(file, "w", encoding='utf-8') as fp:
        for line in lines:
            if line != str(data):
                fp.write(line)
    update_notice(file)


def change_state(file, new_state, index):  # index-miejsce w dokumencie zmiany
    with open(file, 'r', encoding='utf-8') as fp:
        data = fp.readlines()
    data[index] = new_state
    with open(file, 'w', encoding='utf-8') as fp:
        fp.writelines(data)
    update_notice(file)


def update_notice(file):  # informacja o aktualizacji bazy danych
    if file == BOOKS:
        print("Baza książek" + DATA_UPDATE)
    elif file == READERS:
        print("Baza czytelników" + DATA_UPDATE)


def input_book_data(action):  # komunikat o wprowadzeniu danych na temat autora i książki
    author = input("Podaj autora książki do " + action + ": ")
    book = input("Podaj tytuł książki do " + action + ": ")
    return author, book


def input_user_data():
    name = input(INPUT_NAMES)  # np. Stec Dawid
    password = input(INPUT_PASSWORD)
    return name, password


# Klasy
class Library:
    library = {}  # baza wszystkich książek  # to jest atrybut klasowy
    readers = {}  # baza wszystkich czytelników i ich wypożyczonych książek
    readers_passwords = {}      # baza haseł użytkowników
    authors = []  # lista z indeksami autorów
    books = []  # lista z indeksami książek
    librarians = {}  # baza bibliotekarzy
    readers_indices = []  # lista z indeksami czytelników

    def __init__(self):
        self.options = {"Czytelnik": (reader_login, (), {}),
                        "Bibliotekarz": (librarian_login, (), {}),
                        "Wyjdź": (exit, (), {})}
        if any([len(self.library.keys()), len(self.readers.keys()), len(self.readers_passwords.keys()),
               len(self.authors), len(self.books), len(self.librarians.keys()), len(self.readers_indices)]) == 0:
            self.create_library()                   # chcemy, aby te funkcje działały tylko na początku programu
            self.create_readers_library()
            self.create_readers_passwords()
            self.create_librarians()

    def create_library(self):  # tworzenie bazy książek
        with open(BOOKS, "r", encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                text = line.split(sep=SEP)
                if text[0] not in self.library.keys():
                    self.library[text[0]] = {}
                self.authors.append(text[0])
                self.library[text[0]].update({text[1]: {}})
                self.books.append(text[1])
                for i in range(2, 5, 1):
                    if text[i] == 'N':
                        self.library[text[0]][text[1]][LIBRARY[i - 2]] = None
                    else:
                        self.library[text[0]][text[1]][LIBRARY[i - 2]] = text[i]

    def create_readers_library(self):  # tworzenie bazy czytelników i ich wypożyczonych książek
        with open(READERS, "r", encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                text = line.split(sep=SEP)
                self.readers[text[0]] = {}
                self.readers_indices.append(text[0])
                for i in range(1, len(text) - 1, 2):
                    if text[i] not in self.readers[text[0]]:
                        self.readers[text[0]].update({text[i]: [text[i + 1]]})
                    else:
                        self.readers[text[0]][text[i]].append(text[i + 1])

    def create_readers_passwords(self):
        with open(R_PASSWORDS, "r", encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                text = line.split(sep=SEP)
                self.readers_passwords[text[0]] = text[1]

    def create_librarians(self):  # tworzenie bazy bibliotekarzy
        with open(LIBRARIANS, "r", encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                text = line.split(sep=SEP)
                self.librarians[text[0]] = text[1]

    def to_string_book(self, author, title):  # zamiana danych o książce z bazy na łańcuch znaków
        new_line = author + '$' + title + '$'
        for info in self.library[author][title]:
            if self.library[author][title][info] is not None:
                new_line += self.library[author][title][info] + '$'
            else:
                new_line += 'N$'
        return new_line[:-1] + '\n'

    def to_string_reader(self, reader):  # zamiana danych o czytelniku z bazy na łańcuch znaków
        new_line = reader + '$'
        for author in self.readers[reader].keys():
            for book in self.readers[reader][author]:
                new_line += author + '$' + book + '$'
        return new_line[:-1] + '\n'

    def find_book_indices(self, book, author):  # znalezienie indeksu prawidłowej książki (bo tytuł mogą się powtarzać)
        indices = [i for i in range(len(self.books)) if self.books[i] == book]
        for i in indices:
            if author == self.authors[i]:  # aby być pewnym wyboru, autor musi się zgadzać
                return i

    def menu(self):
        options = list(self.options.items())
        for num, option in enumerate(options, start=1):
            print("{}. {}".format(num, option[0]))
        correct_choices = range(1, len(options) + 1)
        while True:
            try:
                choice = int(input(">> "))
                assert choice in correct_choices
            except (ValueError, AssertionError):
                print("Podaj odpowiedni numer.")
            else:
                func, args, kwargs = options[choice - 1][1]
                return func(*args, **kwargs)

    @classmethod
    def check_users(cls, name, password, file):  # sprawdzanie istnienia bibliotekarza
        try:
            if file[name] != password:
                print("Błędne hasło.\n")
                return None
            else:
                print("Witaj " + name)
                return name
        except KeyError:
            print("Nie istnieje taki użytkownik.")
            return None

    def browse(self):  # przeglądanie katalog (wyszukiwanie po tytule, autorze lub słowach kluczowych)
        search = input("Wpisz tytuł, autora lub fragment: ")  # np. King dla
        tokens_list = search.split(sep=" ")
        with open(BOOKS, "r", encoding='utf-8') as fp:
            file = fp.readlines()
        for token in tokens_list:       # będziemy zawężać nasze wyniki wyszukiwania dla poszczególnych słów
            found = []
            for line in file:
                line = line.strip()
                text = line.split(sep=SEP)
                if token in ' '.join(text[:-3]):  # 3 ostatnie informacje są niepotrzebne w wyszukiwaniu
                    found.append(line)
            file = found
        if len(file) == 0:
            print("Brak wyników wyszukiwania.")
        else:
            for line in file:
                line = line.strip()
                text = line.split(sep=SEP)
                print("Autor: " + text[0] + ", Tytuł: " + text[1] + ", Dostępność: ", end='')
                if text[2] != 'N':
                    print("Wypożyczona do " + text[4])
                else:
                    print("Dostępna")
        self.menu()  # taka rekurencja nas wykończy przy dłuższym używaniu systemu


class Reader(Library):  # czytelnik jest szczególnym przypadkiem biblioteki?
    def __init__(self, name, password):
        super().__init__()
        self.reader_name = self.check_users(name, password, self.readers_passwords)
        self.options = {"Wypożycz": (self.__check_out, (), {}),
                        "Zarezerwuj": (self.__book_up, (), {}),
                        "Prolonguj": (self.__renew, (), {}),
                        "Katalog": (self.browse, (), {}),
                        "Wyloguj": (self.log_out, (), {})}

    def log_out(self):
        self.reader_name = None

    def __check_out(self):  # wypożyczenie książki
        author, book = input_book_data("wypożyczenia")
        try:
            if self.library[author][book][LIBRARY[0]] is not None:
                print('Książka już jest wypożyczona!\n')
            else:
                self.library[author][book][LIBRARY[0]] = self.reader_name
                new_date = date.today() + timedelta(days=RENEW)
                self.library[author][book][LIBRARY[2]] = new_date.strftime("%d-%m-%Y")
                if author not in self.readers[self.reader_name].keys():
                    self.readers[self.reader_name].update({author: [book]})
                else:
                    self.readers[self.reader_name][author].append(book)
                change_state(BOOKS, self.to_string_book(author, book), self.find_book_indices(book, author))
                change_state(READERS, self.to_string_reader(self.reader_name),
                             self.readers_indices.index(self.reader_name))
        except KeyError:
            print(WRONG_DATA)
        self.menu()

    def __renew(self):  # przedłużenie wypożyczenia
        author, book = input_book_data("przedłużenia")
        if author in self.readers[self.reader_name].keys() and book in self.readers[self.reader_name][author]:
            old_date = datetime.strptime(self.library[author][book]['Data'], '%d-%m-%Y')
            new_date = old_date + timedelta(days=RENEW)
            self.library[author][book][LIBRARY[2]] = new_date.strftime("%d-%m-%Y")
            change_state(BOOKS, self.to_string_book(author, book), self.find_book_indices(book, author))
        else:
            print("Nie wypożyczyłeś tej książki!\n")
        self.menu()

    def __book_up(self):  # zarezerwowanie książki, która jest wypożyczona
        author, book = input_book_data("rezerwacji")
        try:
            if self.library[author][book][LIBRARY[0]] is None:
                print('Książkę można wypożyczyć!\n')
            elif self.library[author][book][LIBRARY[1]] is not None:
                print('Książkę już jest zarezerwowana!\n')
            else:
                self.library[author][book][LIBRARY[1]] = self.reader_name
                change_state(BOOKS, self.to_string_book(author, book), self.find_book_indices(book, author))
        except KeyError:
            print(WRONG_DATA)
        self.menu()


class Librarian(Library):
    def __init__(self, name, password):
        super().__init__()
        self.librarian_name = self.check_users(name, password, self.librarians)
        self.options = {"Przyjmij zwrot": (self.__accept_return, (), {}),
                        "Dodaj czytelnika": (self.__add_reader, (), {}),
                        "Dodaj książkę": (self.__add_book, (), {}),
                        "Usuń książkę": (self.__remove_book, (), {}),
                        "Katalog": (self.browse, (), {}),
                        "Wyloguj": (self.log_out, (), {})}

    def log_out(self):
        self.librarian_name = None

    def __accept_return(self):  # przyjmowanie zwrotu książki
        author, book = input_book_data("zwrócenia")
        try:
            reader = self.library[author][book][LIBRARY[0]]
            self.library[author][book][LIBRARY[0]] = None
            self.library[author][book][LIBRARY[2]] = None
            if len(self.readers[reader][author]) == 1:
                del self.readers[reader][author]
            else:
                self.readers[reader][author].remove(book)
            change_state(BOOKS, self.to_string_book(author, book), self.find_book_indices(book, author))
            change_state(READERS, self.to_string_reader(reader), self.readers_indices.index(reader))
        except KeyError:
            print(WRONG_DATA)
        self.menu()

    def __add_reader(self):
        reader, password = input_user_data()
        if reader not in self.readers.keys():
            add_data_to_file(R_PASSWORDS, reader+'$'+password+'\n')
            add_data_to_file(READERS, reader+'\n')
            self.readers_passwords[reader] = password
            self.readers[reader] = {}
            self.readers_indices.append(reader)
        else:
            print("Czytelnik znajduje się już w bazie danych!\n")
        self.menu()

    def __add_book(self):
        author, book = input_book_data("dodania")
        if author in self.library.keys() and book in self.library[author].keys():
            print("Ta książka już się znajduje w bibliotece!\n")
            self.menu()
        elif author not in self.library.keys():
            self.library[author] = {}
        self.library[author].update({book: {}})
        self.authors.append(author)
        self.books.append(book)
        for i in LIBRARY:
            self.library[author][book][i] = None
        add_data_to_file(BOOKS, self.to_string_book(author, book))
        self.menu()

    def __remove_book(self):
        author, book = input_book_data("usunięcia")
        try:
            if self.library[author][book][LIBRARY[0]] is not None:
                print('Książka jest przez kogoś wypożyczona!\n')
            else:
                delete_data_from_file(BOOKS, self.to_string_book(author, book))
                if len(self.library[author].keys()) == 1:
                    del self.library[author]
                else:
                    del self.library[author][book]
                index = self.find_book_indices(book, author)
                self.authors.pop(index)
                self.books.pop(index)
        except KeyError:
            print(WRONG_DATA)
        self.menu()


if __name__ == "__main__":
    while True:
        new = Library()
        print("Kim jesteś?")
        new.menu()
        del new
