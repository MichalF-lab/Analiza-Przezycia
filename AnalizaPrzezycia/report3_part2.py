# -*- coding: utf-8 -*-
from lifelines import CoxPHFitter
from report3_part1 import wczyuj_i_przygotuj_dane_lung, wczytaj_i_przygotuj_dane_pacjentki
import matplotlib.pyplot as plt

lung_encoded = wczyuj_i_przygotuj_dane_lung()

# 1 2
cph = CoxPHFitter()
cph.fit(lung_encoded, duration_col='time', event_col='status')

print(cph.summary)
print(cph.params_)

# 3
baseline_cumulative_hazard = cph.baseline_cumulative_hazard_
print(baseline_cumulative_hazard.head())

baseline_survival = cph.baseline_survival_
print(baseline_survival.head())

# 4
patient_profile1 = wczytaj_i_przygotuj_dane_pacjentki(ph=1)
patient_profile2 = wczytaj_i_przygotuj_dane_pacjentki(ph=2)

hazard_function1 = cph.predict_cumulative_hazard(patient_profile1)
hazard_function2 = cph.predict_cumulative_hazard(patient_profile2)

t1 = hazard_function1.index.values
t2 = hazard_function2.index.values

plt.figure(figsize=(10, 6))
plt.plot(t1, hazard_function1, label="ph=1")
plt.plot(t2, hazard_function2, label="ph=2")
plt.xlabel("Czas (dni)")
plt.ylabel("Hazard h(t)")
plt.title("Funkcja hazardu kobieta, wiek=70, ph.karno=90")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

import numpy as np
lnhazard_function1 = np.log(hazard_function1)
lnhazard_function2 = np.log(hazard_function2)

plt.figure(figsize=(10, 6))
plt.plot(t1, lnhazard_function1, label="ph=1")
plt.plot(t2, lnhazard_function2, label="ph=2")
plt.xlabel("Czas (dni)")
plt.ylabel("ln h(t)")
plt.title("Logarytm funkcji hazardu kobieta, wiek=70, ph.karno=90")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 5 6
survival_function1 = cph.predict_survival_function(patient_profile1)
survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival = survival_function1.loc[300].values[0]

plt.figure(figsize=(10, 6))
plt.plot(survival_function1.index, survival_function1.values)
plt.plot(survival_function2.index, survival_function2.values)
plt.xlabel('Czas (dni)')
plt.ylabel('Prawdopodobienstwo przezycia S(t)')
plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
plt.axhline(y=prob_survival, color='r', linestyle='--', 
            label=f'S(300) = {prob_survival:.4f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)
t_star = 300

prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

print(f"P(T > 300) dla ph=1: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
print(f"P(T > 300) dla ph=2: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")
