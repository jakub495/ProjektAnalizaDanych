import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def menu_glowne():
    df = None

    while True:
        print("\n Analiza NT-proBNP")
        print("1. Wczytaj plik (CSV/JSON)")
        print("2. Pokaż podsumowanie danych")
        print("3. Wyświetl statystyki")
        print("0. Wyjście")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            sciezka = input("Podaj nazwę pliku: ")
            try:
                if sciezka.endswith('.csv'):
                    df = pd.read_csv(sciezka)
                    print("CSV wczytany pomyślnie!")
                elif sciezka.endswith('.json'):
                    df = pd.read_json(sciezka)
                    print("JSON wczytany pomyślnie!")
                else:
                    print("Błąd: Obsługujemy tylko .csv i .json")
            except Exception as e:
                print(f"BŁĄD: Nie udało się otworzyć pliku. ({e})")

        elif wybor == '2':
            if df is not None:
                print(df.head())
            else:
                print("Błąd: Najpierw wczytaj dane!")

        elif wybor == '3':
            if df is not None:
                # pandas.describe() korzysta z numpy do obliczeń
                print(df.describe())
            else:
                print("Błąd: Brak danych do analizy!")

        elif wybor == '0':
            print("Do widzenia.")
            break

        else:
            print("Nieprawidłowy wybór.")


if __name__ == "__main__":
    menu_glowne()
