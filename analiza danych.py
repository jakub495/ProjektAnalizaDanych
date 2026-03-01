import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QLabel)

# budowa api
class OknoGlowne(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Analiza NT-proBNP")
        self.setGeometry(100, 100, 800, 600)


        layout = QVBoxLayout()
        centralny_widget = QWidget()
        centralny_widget.setLayout(layout)
        self.setCentralWidget(centralny_widget)

        # przyciski
        self.przycisk_wczytaj = QPushButton("1. Wczytaj plik (CSV/JSON)")
        self.przycisk_wczytaj.clicked.connect(self.wczytaj_plik)
        layout.addWidget(self.przycisk_wczytaj)

        self.przycisk_statystyki = QPushButton("2. Analiza statystyczna")
        self.przycisk_statystyki.clicked.connect(self.oblicz_statystyki)
        layout.addWidget(self.przycisk_statystyki)

        self.przycisk_wykres = QPushButton("3. Generuj wykres")
        self.przycisk_wykres.clicked.connect(self.rysuj_wykres)
        layout.addWidget(self.przycisk_wykres)

        self.tabela = QTableWidget()
        layout.addWidget(QLabel("Podgląd danych:"))
        layout.addWidget(self.tabela)

    def wczytaj_plik(self):
        sciezka, _ = QFileDialog.getOpenFileName(self, "Otwórz plik", "", "Dane (*.csv *.json)")
        if sciezka:
            try:
                if sciezka.endswith('.csv'):
                    self.df = pd.read_csv(sciezka, header=None)
                elif sciezka.endswith('.json'):
                    self.df = pd.read_json(sciezka)

                self.df = self.df.apply(pd.to_numeric, errors='coerce') # zamiana na liczby i  usuwanie liter
                self.odswiez_tabele()
                QMessageBox.information(self, "Plik wczytany pomyślnie.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać pliku: {e}")

    def odswiez_tabele(self):
        if self.df is not None:
            df_display = self.df.head(10)  # pierwsze 10 wierszy
            self.tabela.setRowCount(df_display.shape[0])
            self.tabela.setColumnCount(df_display.shape[1])
            for i in range(df_display.shape[0]): # przenoszenie danych z df do tabelki w api
                for j in range(df_display.shape[1]):
                    self.tabela.setItem(i, j, QTableWidgetItem(str(df_display.iloc[i, j])))

    def oblicz_statystyki(self):
        if self.df is None:
            return QMessageBox.warning(self, "Błąd", "Najpierw wczytaj dane!")

        zakres, ok = QInputDialog.getText(self, "Zakres", f"Podaj zakres kolumn (1-{len(self.df.columns)}), np. 1-2:")
        if ok and zakres:
            try:
                start, end = map(int, zakres.split('-'))
                wycinek = self.df.iloc[:, start - 1: end].values.flatten()
                dane = pd.Series(wycinek).dropna()

                if len(dane) == 0:
                    QMessageBox.warning(self, "Błąd", "Brak danych w tym zakresie")
                    return

                wyniki = (f"Średnia: {np.mean(dane):.2f}\n"
                          f"Odchylenie std.: {np.std(dane):.2f}\n"
                          f"Minimum: {np.min(dane):.2f}\n"
                          f"Maximum: {np.max(dane):.2f}\n"
                          f"Liczba pomiarów: {len(dane)}")

                QMessageBox.information(self, f"Wyniki dla {zakres}", wyniki)
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nieprawidłowy zakres lub dane: {e}")

# Bydowanie wykresu
def rysuj_wykres_ciagly(df):
    if df is not None:
        dane_ciagle = df.values.flatten()

        plt.figure(figsize=(15, 5))

        # Wykres jako jedna linia
        plt.plot(dane_ciagle, marker='o', linestyle='-', color='darkcyan', markersize=4)

        # 3. Dodajemy opisy
        plt.title('Analiza NT-proBNP')
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



# do usunięcia potem
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
