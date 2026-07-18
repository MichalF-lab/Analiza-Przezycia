# Analiza Przeżycia

*Modele przeżycia (Kaplan-Meier, Cox PH, Weibull AFT, proportional odds) — zadania i raporty z przedmiotu Analiza przeżycia / statystyka zaawansowana (studia, PWr).*

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?logo=r&logoColor=white)

## 📖 Opis

Cztery raporty (`Lista1.py`–`Lista4.py`), z których każdy jest samodzielnym generatorem PDF (biblioteka `weasyprint`): wczytuje wyniki z własnych modułów `report*_partN.py`, wstawia je do szablonu HTML i renderuje gotowy dokument. Listy 2–4 importują funkcje pomocnicze bezpośrednio z modułów Listy 1 (`wykres_do_base64`, `first_type_error`, przez `sys.path` wskazujący na `lista-01/`) — to realna zależność międzylistowa, nie generyczna biblioteka.

## 📂 Struktura

| Folder | Zawartość |
|---|---|
| `lista-01/` | `Lista1.py` (+ wersja robocza) wraz z modułami `report_part1.py`–`report_part4.py` (wykresy, testy statystyczne, przygotowanie danych — importowane też przez listy 2–4). Model: rozkład Weibulla z trzema parametrami |
| `lista-02/` | Test dwupróbkowy (błąd I rodzaju, dane o remisji), `Raport_Lista2.pdf`. Zawiera też `szablon2_wersja_robocza.html` — wcześniejszy wariant szablonu |
| `lista-03/` | Analiza danych o raku płuc ([NCCTG Lung Cancer](https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv)): modele Coxa PH i proportional odds, `Raport_Lista3.pdf`. Raport obejmuje też zagadnienia z „Listy 9–12". Podfolder `r-analiza/` zawiera równoległą eksplorację tych samych modeli w R — warianty dopasowania (`ph9`, `ph11`, `pomR` z wariantem `wersja-alt` na innym rozkładzie: Weibull vs log-logistic, `proportional_odds_wersja1.Rmd`, `proportional_odds_lista11.Rmd`) oraz wyniki pośrednie w `tymczasowe/` |
| `lista-04/` | Model przyspieszonego czasu awarii (Weibull AFT) na danych o marskości wątroby ([PBC](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv)), `Raport_Lista4.pdf` |
| `wspolne/` | `style.css` — jedyny plik faktycznie współdzielony przez szablony PDF wszystkich 4 list |
| `testy/` | Luźne skrypty R do testów statystycznych (rozkłady, estymacja gęstości), niepowiązane z konkretną listą |

Powiązane repo: [Uczenie_Maszynowe](https://github.com/MichalF-lab/Uczenie_Maszynowe) (eksperymenty ML/DL).

## 🛠️ Technologie

| Technologia | Szczegóły |
|---|---|
| Python | pandas, numpy, scipy, matplotlib, lifelines, weasyprint |
| R | survival, timereg, nltm, RMarkdown |

## ⚠️ Uwagi

Repo zawiera kilka wariantów tego samego modelu (`wersja_robocza`, `wersja-alt`, `tymczasowe`) obok wersji głównej — to celowe warianty analizy, nie przypadkowe duplikaty.

## 👤 Autor

Michał Frąckowiak, nr indeksu 275951
