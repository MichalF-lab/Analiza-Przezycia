# -*- coding: utf-8 -*-
from lifelines import CoxPHFitter
from report3_part1 import wczyuj_i_przygotuj_dane_lung, wczytaj_i_przygotuj_dane_pacjentki
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lista-01'))
from report_part1 import wykres_do_base64
import numpy as np
import pandas as pd

lung_encoded = wczyuj_i_przygotuj_dane_lung()

cph = CoxPHFitter()
cph.fit(lung_encoded, duration_col='time', event_col='status')

print(cph.summary)
print(cph.params_)

# 3
def fig11():
    bh = cph.baseline_cumulative_hazard_
    plt.figure(figsize=(10, 6))
    plt.plot(bh.index, bh.iloc[:, 0], color='red', lw=2, label="Bazowy skumulowany hazard")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard H0(t)")
    plt.title("Bazowa skumulowana funkcja hazardu")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt

def fig12():
    bs = cph.baseline_survival_
    plt.figure(figsize=(10, 6))
    plt.plot(bs.index, bs.iloc[:, 0], color='blue', lw=2, label="Bazowe przezycie")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Prawdopodobienstwo przezycia S0(t)")
    plt.title("Bazowa funkcja przezycia")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt
# 4
patient_profile1 = wczytaj_i_przygotuj_dane_pacjentki(ph=1)
patient_profile2 = wczytaj_i_przygotuj_dane_pacjentki(ph=2)

hazard_function1 = cph.predict_cumulative_hazard(patient_profile1)
hazard_function2 = cph.predict_cumulative_hazard(patient_profile2)

t1 = hazard_function1.index.values
t2 = hazard_function2.index.values

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard_function1, label="ph=1")
    plt.plot(t2, hazard_function2, label="ph=2")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard H(t)")
    plt.title("Funkcja hazardu kobieta, wiek=70, ph.karno=90")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def fig2():
    lnhazard_function1 = np.log(hazard_function1)
    lnhazard_function2 = np.log(hazard_function2)

    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard_function1, label="ph=1")
    plt.plot(t2, lnhazard_function2, label="ph=2")
    plt.xlabel("Czas (dni)")
    plt.ylabel("ln H(t)")
    plt.title("Logarytm funkcji hazardu kobieta, wiek=70, ph.karno=90")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)  

# 5 6
survival_function1 = cph.predict_survival_function(patient_profile1)
survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival1 = survival_function1.loc[300].values[0]
prob_survival2 = survival_function2.loc[300].values[0]
prob_survival = survival_function1.loc[300].values[0]

def fig3():
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function1.index, survival_function1.values)
    plt.plot(survival_function2.index, survival_function2.values)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.axhline(y=prob_survival1, color='r', linestyle='--', label=f'S(300) = {prob_survival1:.4f}')
    plt.axhline(y=prob_survival2, color='r', linestyle='--', label=f'S(300) = {prob_survival2:.4f}')
    bs = cph.baseline_survival_
    idx_closest = np.abs(bs.index.values - 300).argmin()
    prob_baseline_300 = bs.iloc[idx_closest, 0]
    plt.axhline(y=prob_baseline_300, color='black', linestyle=':', label=f'Bazowe S(300) = {prob_baseline_300:.4f}')
    plt.axvline(x=300, color='r', linestyle='--', alpha=0.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)

t_star = 300
prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

print(f"P(T > 300) dla ph=1: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
print(f"P(T > 300) dla ph=2: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")


def fig5():
    from lifelines import WeibullAFTFitter
    fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
    survival_function = fit_aft.predict_survival_function(wczytaj_i_przygotuj_dane_pacjentki())
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function.index, survival_function.values)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.axhline(y=prob_survival1, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival1:.4f}')
    plt.plot(survival_function1.index, survival_function1.values)
    plt.axhline(y=prob_survival1, color='r', linestyle='--', label=f'S(300) = {prob_survival1:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig6():
    plt = fig12()
    plt.plot(survival_function1.index, survival_function1.values)
    plt.plot(survival_function2.index, survival_function2.values)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.axhline(y=prob_survival, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)

    return wykres_do_base64(plt)





def przeslij_dane2():
    return {
        "cph_summary": cph.summary,
        "cph_params": cph.params_,
        "fig11": fig11(),
        "fig12": fig12(),
        "fig1": fig1(),
        "fig2": fig2(),
        "fig3": fig3(),
        "fig5": fig5(),
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
        "fig11": wykres_do_base64(fig11()),
        "fig12": wykres_do_base64(fig12()),
    }