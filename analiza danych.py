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
                    self.df = pd.read_csv(sciezka)
                elif sciezka.endswith('.json'):
                    self.df = pd.read_json(sciezka)

                self.df = self.df.apply(pd.to_numeric, errors='coerce') # zamiana na liczby i  usuwanie liter
                self.odswiez_tabele()
                QMessageBox.information(self, "Sukces", "Plik wczytany pomyślnie.")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać pliku: {e}")

    def odswiez_tabele(self):
        if self.df is not None:
            df_display = self.df
            self.tabela.setRowCount(df_display.shape[0])
            self.tabela.setColumnCount(df_display.shape[1])
            self.tabela.setHorizontalHeaderLabels(df_display.columns.astype(str))

            for i in range(df_display.shape[0]): # przenoszenie danych z df do tabelki w api
                for j in range(df_display.shape[1]):
                    self.tabela.setItem(i, j, QTableWidgetItem(str(df_display.iloc[i, j])))

    def oblicz_statystyki(self):
        if self.df is None:
            return QMessageBox.warning(self, "Błąd", "Najpierw wczytaj dane")

        try:
            kol_idx, ok1 = QInputDialog.getInt(
                self, "Wybór kolumny",
                f"Podaj numer kolumny (1-{len(self.df.columns)}):",
                value=1, min=1, max=len(self.df.columns)
            )

            if not ok1:
                return

            max_wierszy = len(self.df)
            zakres, ok2 = QInputDialog.getText(
                self, "Zakres wierszy",
                f"Podaj zakres wierszy w kolumnie {kol_idx} (1-{max_wierszy}), np. 1-10:"
            )

            if ok2 and zakres:
                start_w, end_w = map(int, zakres.split('-'))

                wycinek = self.df.iloc[start_w - 1: end_w, kol_idx - 1]
                dane = pd.to_numeric(wycinek, errors='coerce').dropna()

                if len(dane) == 0:
                    QMessageBox.warning(self, "Błąd", "Brak danych liczbowych w podanym zakresie")
                    return

                wyniki = (f"Statystyki dla kolumny {kol_idx} (wiersze {start_w}-{end_w}):\n\n"
                          f"Średnia: {np.mean(dane):.2f}\n"
                          f"Mediana: {np.median(dane):.2f}\n"
                          f"Odchylenie std.: {np.std(dane):.2f}\n"
                          f"Minimum: {np.min(dane):.2f}\n"
                          f"Maximum: {np.max(dane):.2f}\n"
                          f"Liczba pomiarów: {len(dane)}")

                QMessageBox.information(self, "Wyniki analizy", wyniki)

        except ValueError:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowy format zakresu. Użyj formatu np. '1-10'.")
        except Exception as e:
            QMessageBox.critical(self,  "Błąd", f"Wystąpił nieoczekiwany błąd: {e}")


# wykres
    def rysuj_wykres(self):
        if self.df is None:
            return QMessageBox.warning(self, "Błąd", "Najpierw wczytaj dane!")

        try:
            kol_idx, ok1 = QInputDialog.getInt(
                self, "Wybór kolumny",
                f"Podaj numer kolumny (1-{len(self.df.columns)}):",
                value=1, min=1, max=len(self.df.columns)
            )

            if not ok1:
                return

            max_wierszy = len(self.df)
            zakres, ok2 = QInputDialog.getText(
                self, "Zakres wierszy",
                f"Podaj zakres wierszy w kolumnie {kol_idx} (1-{max_wierszy}), np. 1-10:"
            )

            if ok2 and zakres:
                start_w, end_w = map(int, zakres.split('-'))

                wycinek = self.df.iloc[start_w - 1: end_w, kol_idx - 1]
                dane = pd.to_numeric(wycinek, errors='coerce').dropna()
                nazwa_kolumny = self.df.columns[kol_idx - 1]

                if len(dane) == 0:
                    QMessageBox.warning(self, "Błąd", "Brak danych liczbowych w podanym zakresie!")
                    return

            plt.figure(figsize=(10, 5))
            plt.plot(dane.values, marker='o', linestyle='-', color='darkcyan', markersize=4)
            plt.title(f'Pomiary {nazwa_kolumny}')
            plt.xlabel('Pomiar')
            plt.ylabel('Wartość pomiaru')
            plt.grid(True, alpha=0.3)

            plt.show()
        except ValueError:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowy format zakresu. Użyj formatu np. '1-10'.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OknoGlowne()
    window.show()
    sys.exit(app.exec())