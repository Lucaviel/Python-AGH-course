import pandas as pd
import matplotlib.pyplot as plt

file1 = "Plant_1_Generation_Data.csv"
file2 = "Plant_2_Generation_Data.csv"


def readcsv(args):
    return pd.read_csv(args, header=0, parse_dates=['DATE_TIME'])


if __name__ == "__main__":
    df1 = readcsv(file1)
    df2 = readcsv(file2)

    # wczytywanie i połączenie dwóch plików
    df = pd.concat([df1, df2])

    # usuwanie wierszy mających null/na
    df = df.dropna().reset_index(drop=True)

    # tworzenie wykresu
    start_day = pd.to_datetime('15.05.2020')
    end_day = pd.to_datetime('21.05.2020')
    df_week = df[df['DATE_TIME'].between(start_day, end_day)]
    df_week_ind = df_week.set_index('DATE_TIME')
    df_gen1 = df_week_ind.loc[df_week_ind['SOURCE_KEY'] == '1BY6WEcLGh8j5v7']

    # średnie AC_POWER dla wszystkich generatorów
    df_all_means = df_week.groupby(['SOURCE_KEY', "DATE_TIME"], as_index=False)['AC_POWER'].mean()
    df_all_means_plot = df_all_means.plot(x='DATE_TIME', y='AC_POWER', label="Średnie wszystkich")
    df_gen1.AC_POWER.plot(ax=df_all_means_plot, color="yellow", label="1 generator")
    # df_gen1.AC_POWER.plot(color="blue", label="1 generator")
    #
    # means = df_week.groupby(by='SOURCE_KEY').agg(means_power = ("AC_POWER", "mean"))
    #
    # for generator in means.index:
    #     plt.axhline(y=means.loc[generator][0], color='red', label=generator)

    plt.legend()
    plt.show()

    # kiedy AC_POWER któregoś z generatorów było na poziomie < 80% średniej
    mean = df_week.AC_POWER.mean()
    df_mean_most = df_week[df_week['AC_POWER'] < 0.8 * mean].groupby('SOURCE_KEY').size().sort_values(ascending=False)
    print("Najczęstsze generatory o wartościach mniejszej od 80% średniej: ")
    print(df_mean_most.head())
