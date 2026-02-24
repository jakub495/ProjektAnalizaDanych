import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Statystyka
def analiza_statystyczna_zakresu(df, start_col, end_col):
    try:
        # Wycinamy kolumny (indeksowanie od 0)
        wycinek = df.iloc[:, start_col - 1: end_col].values.flatten()

        # Usuwamy wartości NaN, żeby numpy się nie wywalił
        dane = pd.Series(wycinek).dropna()

        if len(dane) == 0:
            return "Błąd: Brak danych numerycznych w tym zakresie!"

        # Obliczenia przy użyciu NumPy
        wyniki = {
            "Średnia": np.mean(dane),
            "Odchylenie std.": np.std(dane),
            "Minimum": np.min(dane),
            "Maximum": np.max(dane),
            "Liczba pomiarów": len(dane)
        }
        return wyniki
    except Exception as e:
        return f"Błąd obliczeń: {e}"

# Bydowanie wykresu
def rysuj_wykres_ciagly(df):
    if df is not None:
        dane_ciagle = df.values.flatten()

        # Wywalanie NaN z wykresu
        dane_czyste = pd.Series(dane_ciagle).dropna()

        plt.figure(figsize=(15, 5))

        # Wykres jako jedna linia
        plt.plot(dane_czyste, marker='o', linestyle='-', color='darkcyan', markersize=4)

        # 3. Opis
        plt.title('Pomiary NT-proBNP')
        plt.xlabel('Całkowita liczba punktów pomiarowych')
        plt.ylabel('Wartość pomiaru [pg/ml]')
        plt.grid(True, alpha=0.3)

        # Pionowe linie oddzielające dane z różnych kolumn
        liczba_wierszy = len(df)
        for i in range(1, len(df.columns)):
            plt.axvline(x=i * liczba_wierszy, color='red', linestyle='--', alpha=0.5)

        plt.show()
    else:
        print("Błąd: Brak danych!")



# Menu
def menu_glowne():
    df = None

    while True:
        print("\n Analiza NT-proBNP")
        print("1. Wczytaj plik (CSV/JSON)")
        print("2. Pokaż podsumowanie danych")
        print("3. Analiza statystyczna")
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
                    df = pd.read_json(sciezka)
                    print("JSON wczytany pomyślnie!")
                else:
                    print("Błąd: Obsługujemy tylko .csv i .json")
            except Exception as e:
                print(f"BŁĄD: Nie udało się otworzyć pliku. ({e})")

            df = df.apply(pd.to_numeric, errors='coerce')


        elif wybor == '2':
            if df is not None:
                print(df.head())
            else:
                print("Błąd: Najpierw wczytaj dane!")

        elif wybor == '3':
            if df is not None:
                print(f"Dostępne kolumny: 1 - {len(df.columns)}")
                zakres = input("Podaj zakres kolumn do statystyk (np. 1-2): ")
                try:
                    start, end = map(int, zakres.split('-'))
                    # Wywołujemy funkcję
                    stats = analiza_statystyczna_zakresu(df, start, end)

                    if isinstance(stats, dict):
                        print(f"\n*** WYNIKI DLA KOLUMN {start}-{end} ***")
                        for klucz, wartosc in stats.items():
                            print(f"{klucz}: {wartosc:.2f}")  # Zaokrąglenie do dwóch miejsc po przecinku
                    else:
                        print(stats)
                except ValueError:
                    print("Błąd: Użyj formatu 'liczba-liczba'.")
            else:
                print("Błąd: Najpierw wczytaj plik!")

        elif wybor == '4':
            rysuj_wykres_ciagly(df)

        elif wybor == '0':
            print("Do widzenia.")
            break

        else:
            print("Nieprawidłowy wybór.")


if __name__ == "__main__":
    menu_glowne()
