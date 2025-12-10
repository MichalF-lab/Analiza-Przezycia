import pandas as pd
import numpy as np

# 1. Wczytanie pliku
url = "https://www.key2stats.com/NCCTG_Lung_Cancer_Data_535_29.csv" 
lung = pd.read_csv(url)

# 2. Usunięcie zbędnych kolumn
lung = lung.drop(columns=["Unnamed: 0", "X"], errors="ignore")

# 3. Sekcje jako NumPy arrays

# --- Survival ---
survival_np = lung[["time", "status"]].to_numpy()

# --- Demografia ---
demographics_np = lung[["age", "sex"]].to_numpy()

# --- Kliniczne ---
clinical_np = lung[[
    "inst",
    "ph.ecog",
    "ph.karno",
    "pat.karno",
    "meal.cal",
    "wt.loss"
]].to_numpy()

from sklearn.impute import SimpleImputer

imp = SimpleImputer(strategy="median")
lung_imputed = pd.DataFrame(imp.fit_transform(lung), columns=lung.columns)