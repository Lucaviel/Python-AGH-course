from main import train


def menu(sample):  # menu pozwalające wybrać metrykę
    options = {"Euklides": (train, (sample, "euclidian_distance"), {}),
               "Taksówka": (train, (sample, "taxicab_distance"), {}),
               "Maksimum": (train, (sample, "maximum_distance"), {}),
               "Cosinusowa": (train, (sample, "cosine_distance"), {})}
    list_options = list(options.items())
    for num, option in enumerate(list_options, start=1):
        print("{}. {}".format(num, option[0]))
    correct_choices = range(1, len(list_options) + 1)
    while True:
        try:
            choice = int(input(">> "))
            assert choice in correct_choices
        except (ValueError, AssertionError):
            print("Podaj odpowiedni numer.")
            pass
        else:
            func, args, kwargs = list_options[choice - 1][1]
            return func(*args, **kwargs)
