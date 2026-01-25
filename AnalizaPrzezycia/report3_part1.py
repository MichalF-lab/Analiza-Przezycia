import pandas as pd
import numpy as np

# 1. Wczytanie pliku
url = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"
lung = pd.read_csv(url)

lung = lung[["time","status","age", "sex", "ph.ecog", "ph.karno"]]
lung = lung.dropna()

lung['age'] = lung['age'].astype(int) - lung['age'].mean()
lung['ph.karno'] = lung['ph.karno'].astype(int) - lung['ph.karno'].mean()
lung['sex'] = lung['sex'].map({1: 0, 2: 1})
lung['status'] = lung['status'].map({1: 0, 2: 1})
lung_encoded = pd.get_dummies(lung, columns=['ph.ecog'], drop_first=True)
lung_encoded['ph.ecog_1.0'] = lung_encoded['ph.ecog_1.0'].astype(int)
lung_encoded['ph.ecog_2.0'] = lung_encoded['ph.ecog_2.0'].astype(int)
lung_encoded['ph.ecog_3.0'] = lung_encoded['ph.ecog_3.0'].astype(int)
print(lung_encoded.head())
# Zakładając, że masz DataFrame 'data' z kolumnami: time, status, sex

# Odpowiednik: fit_aft = survreg(Surv(time, status) ~ as.factor(sex) + as.factor(censored) + data = dane,
#                                  dist = "weibull")

from lifelines import WeibullAFTFitter

fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
print(fit_aft.summary)


def wczytaj_i_przygotuj_dane():
    
    # zad 3
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"
    lung_original = pd.read_csv(url)
    lung_original = lung_original[["time","status","age", "sex", "ph.ecog", "ph.karno"]]
    lung_original = lung_original.dropna()
    age_mean = lung_original['age'].mean()
    ph_karno_mean = lung_original['ph.karno'].mean()

    # Definicja profilu pacjenta z CENTROWANYMI wartościami
    patient_profile = pd.DataFrame({
        'sex': [1],                      # 1 = kobieta (po mapowaniu 2->1)
        'ph.ecog_1.0': [1],
        'ph.ecog_2.0': [0],
        'ph.ecog_3.0': [0],
        'age': [70 - age_mean],          # WYCENTROWANY wiek
        'ph.karno': [90 - ph_karno_mean] # WYCENTROWANE ph.karno
    })
    return patient_profile

patient_profile = wczytaj_i_przygotuj_dane()

survival_function = fit_aft.predict_survival_function(patient_profile)

prob_survival = survival_function.loc[300].values[0]

print(f"Prawdopodobieństwo, że czas życia > 300 dni: {prob_survival:.4f}")
print(f"Czyli około: {prob_survival * 100:.2f}%")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(survival_function.index, survival_function.values)
plt.axhline(y=prob_survival, color='r', linestyle='--', 
            label=f'S(300) = {prob_survival:.4f}')
plt.axvline(x=300, color='r', linestyle='--', alpha=0.5)
plt.xlabel('Czas (dni)')
plt.ylabel('Prawdopodobieństwo przeżycia S(t)')
plt.title('Funkcja przeżycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
# Pobranie parametrów z modelu AFT
params = fit_aft.params_

# Parametr kształtu (rho) i sigma
rho = np.exp(params['rho_'])
sigma = 1 / rho

print("="*60)
print("Parametry rozkładu Weibulla:")
print("="*60)
print(f"rho = {rho.values[0]:.4f}")
print(f"sigma = {sigma.values[0]:.4f}")

# Współczynniki gamma z modelu AFT (bez rho_ i lambda_)
gamma = params.drop(['rho_', 'lambda_'])
print("\n" + "="*60)
print("Współczynniki gamma z modelu AFT:")
print("="*60)
print(gamma)

# Przekształcenie na współczynniki beta modelu PH: beta = -gamma/sigma
print(beta)
# najpierw dajemy parametry dopiero pozniej zmieniamy bete
beta = -gamma / sigma.values[0]
print("\n" + "="*60)
print("Współczynniki beta modelu PH (beta = -gamma/sigma):")
print("="*60)





# Zad 1 10
from lifelines import CoxPHFitter


cph = CoxPHFitter()
cph.fit(lung_encoded, duration_col='time', event_col='status')

# Wyświetlenie wyników
print(cph.summary)
print("\n" + "="*60)
print("Parametry modelu (współczynniki):")
print("="*60)
print(cph.params_)