import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QLabel)

# Budowanie aplikacji
class OknoGlowne(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Analiza NT-proBNP")
        self.setGeometry(100, 100, 800, 600)

        # Główny układ
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Przyciski
        self.btn_wczytaj = QPushButton("1. Wczytaj plik (CSV/JSON)")
        self.btn_wczytaj.clicked.connect(self.wczytaj_plik)
        layout.addWidget(self.btn_wczytaj)

        self.btn_statystyki = QPushButton("2. Analiza statystyczna")
        self.btn_statystyki.clicked.connect(self.oblicz_statystyki)
        layout.addWidget(self.btn_statystyki)

        self.btn_wykres = QPushButton("3. Generuj wykres")
        self.btn_wykres.clicked.connect(self.rysuj_wykres)
        layout.addWidget(self.btn_wykres)

        # Tabela do podglądu danych (zamiast df.head())
        self.tabela = QTableWidget()
        layout.addWidget(QLabel("Podgląd danych:"))
        layout.addWidget(self.tabela)

# Bydowanie wykresu
def rysuj_wykres_ciagly(df):
    if df is not None:
        dane_ciagle = df.values.flatten()

        plt.figure(figsize=(15, 5))

        # Wykres jako jedna linia
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
