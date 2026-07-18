import pandas as pd

# 1. Wczytanie pliku
url = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"
lung = pd.read_csv(url)

print(f"Krok 1 - Po wczytaniu: {len(lung)} wierszy")
print(f"Kolumny: {lung.columns.tolist()}")
print()

# 2. Wybór kolumn i konwersja do numpy
data = lung[["time","status","age", "sex", "ph.ecog", "ph.karno"]].to_numpy()
print(f"Krok 2 - Po wybraniu kolumn i to_numpy(): {len(data)} wierszy")
print()

# 3. Sprawdź braki w wybranych kolumnach
lung_selected = lung[["time","status","age", "sex", "ph.ecog", "ph.karno"]]
print("Braki w wybranych kolumnach:")
print(lung_selected.isnull().sum())
print()

# 4. Sprawdź czy numpy zawiera NaN
import numpy as np
print(f"Czy numpy array zawiera NaN? {np.isnan(data).any()}")
print(f"Liczba NaN w numpy array: {np.isnan(data).sum()}")
print()

# 5. Co się stało?
print("DIAGNOZA:")
print(f"DataFrame lung ma: {len(lung)} wierszy")
print(f"Numpy array data ma: {len(data)} wierszy")