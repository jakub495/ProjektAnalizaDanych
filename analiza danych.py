import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox, QLabel)

# budowa api
class OknoGlowne(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.wyniki_statystyk = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Analiza statystyczna pomiarów")
        self.setGeometry(100, 100, 900, 700)


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

        self.btn_eksport = QPushButton("4. Eksportuj wyniki do CSV")
        self.btn_eksport.clicked.connect(self.eksportuj_wyniki)
        layout.addWidget(self.btn_eksport)

        self.btn_pdf = QPushButton("5. Eksportuj raport do PDF")
        self.btn_pdf.clicked.connect(self.eksportuj_pdf)
        layout.addWidget(self.btn_pdf)

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
            items = self.df.columns.tolist()
            item, ok1 = QInputDialog.getItem(self, "Wybór kolumny", "Wybierz kolumnę do analizy:", items, 0, False)

            if not (ok1 and item):
                return

            kol_idx = items.index(item) + 1

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

                self.wyniki_statystyk = {
                    "Kolumna": kol_idx,
                    "Wiersze_od": start_w,
                    "Wiersze_do": end_w,
                    "Średnia": np.mean(dane),
                    "Mediana": np.median(dane),
                    "Odchylenie_std": np.std(dane),
                    "Minimum": np.min(dane),
                    "Maximum": np.max(dane),
                    "Liczba_pomiarów": len(dane)
                }

                wyniki = (f"Statystyki dla Kolumny {kol_idx} (wiersze {start_w}-{end_w}):\n\n"
                          f"Średnia: {self.wyniki_statystyk['Średnia']:.2f}\n"
                          f"Mediana: {self.wyniki_statystyk['Mediana']:.2f}\n"
                          f"Odchylenie std.: {self.wyniki_statystyk['Odchylenie_std']:.2f}\n"
                          f"Minimum: {self.wyniki_statystyk['Minimum']:.2f}\n"
                          f"Maximum: {self.wyniki_statystyk['Maximum']:.2f}\n"
                          f"Liczba pomiarów: {self.wyniki_statystyk['Liczba_pomiarów']}")

                QMessageBox.information(self, "Wyniki analizy", wyniki)

        except ValueError:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowy format zakresu. Użyj formatu np. '1-10'.")
        except Exception as e:
            QMessageBox.critical(self,  "Błąd", f"Wystąpił nieoczekiwany błąd: {e}")

    def eksportuj_wyniki(self):
        if self.wyniki_statystyk is None:
            return QMessageBox.warning(self, "Błąd", "Najpierw wykonaj analizę statystyczną!")

        sciezka, _ = QFileDialog.getSaveFileName(self, "Zapisz wyniki", "wyniki.csv", "CSV (*.csv)")
        if sciezka:
            # tymczasowy DataFrame z wyników słownika
            df_wyniki = pd.DataFrame([self.wyniki_statystyk])
            df_wyniki.to_csv(sciezka, index=False, sep=';', encoding='utf-8-sig')
            QMessageBox.information(self, "Sukces", "Wyniki zapisane.")

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

    def eksportuj_pdf(self):
        if self.wyniki_statystyk is None or self.df is None:
            return QMessageBox.warning(self, "Błąd", "Najpierw wykonaj analizę i wygeneruj dane!")

        sciezka, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz raport PDF",
            "raport.pdf",
            "PDF (*.pdf)"
        )

        if not sciezka:
            return

        try:
            # zapis wykresu do pdf
            wykres_path = "wykres_tmp.png"

            kol_idx = self.wyniki_statystyk["Kolumna"]
            start_w = self.wyniki_statystyk["Wiersze_od"]
            end_w = self.wyniki_statystyk["Wiersze_do"]

            dane = self.df.iloc[start_w - 1:end_w, kol_idx - 1]
            dane = pd.to_numeric(dane, errors='coerce').dropna()

            plt.figure(figsize=(8, 4))
            plt.plot(dane.values, marker='o')
            plt.title("Wykres danych")
            plt.xlabel("Pomiar")
            plt.ylabel("Wartość")
            plt.grid(True)

            plt.savefig(wykres_path)
            plt.close()

            doc = SimpleDocTemplate(sciezka)
            styles = getSampleStyleSheet()
            elements = []

            # tytuł
            elements.append(Paragraph("Raport analizy statystycznej", styles['Title']))
            elements.append(Spacer(1, 12))

            # statystyki
            for key, value in self.wyniki_statystyk.items():
                elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
                elements.append(Spacer(1, 8))

            elements.append(Spacer(1, 20))

            # wykres
            elements.append(Paragraph("Wykres danych:", styles['Heading2']))
            elements.append(Spacer(1, 10))

            img = Image(wykres_path, width=400, height=200)
            elements.append(img)

            doc.build(elements)

            QMessageBox.information(self, "Sukces", "Raport PDF z wykresem zapisany!")

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Błąd zapisu PDF: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OknoGlowne()
    window.show()
    sys.exit(app.exec())