import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Bydowanie wykresu
def rysuj_wykres_ciagly(df):
    if df is not None:
        dane_ciagle = df.values.flatten()

        plt.figure(figsize=(15, 5))

        # 2. Rysujemy jedną linię
        plt.plot(dane_ciagle, marker='o', linestyle='-', color='darkcyan', markersize=4)

        # 3. Dodajemy opisy
        plt.title('Ciągły przebieg wszystkich pomiarów (kolumna po kolumnie)')
        plt.xlabel('Całkowita liczba punktów pomiarowych')
        plt.ylabel('Wartość')
        plt.grid(True, alpha=0.3)

        # Pionowe linie oddzielające dane z różnych kolumn
        liczba_wierszy = len(df)
        for i in range(1, len(df.columns)):
            plt.axvline(x=i * liczba_wierszy, color='red', linestyle='--', alpha=0.5)

        plt.show()
    else:
        print("Błąd: Brak danych!")




def menu_glowne():
    df = None

    while True:
        print("\n Analiza NT-proBNP")
        print("1. Wczytaj plik (CSV/JSON)")
        print("2. Pokaż podsumowanie danych")
        print("3. Wyświetl statystyki") #do zrobienia
        print("4. Generuj wykres")
        print("0. Wyjście")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            sciezka = input("Podaj nazwę pliku: ")
            try:
                if sciezka.endswith('.csv'):
                    df = pd.read_csv(sciezka, header=None)
                    print("CSV wczytany pomyślnie!")
                elif sciezka.endswith('.json'):
                    df = pd.read_json(sciezka, header=None)
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
                # pandas.describe() korzysta z numpy do obliczeń/ zamienić na numpy + dodać komunikat o anomaliach
                print(df.describe())
            else:
                print("Błąd: Brak danych do analizy!")

        elif wybor == '4':
            rysuj_wykres_ciagly(df)

        elif wybor == '0':
            print("Do widzenia.")
            break

        else:
            print("Nieprawidłowy wybór.")


if __name__ == "__main__":
    menu_glowne()
