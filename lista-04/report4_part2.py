
# -*- coding: utf-8 -*-
from lifelines import CoxPHFitter
from report4_part1 import wczytaj_i_przygotuj_dane, survival_at_time_interp, wczytaj_dane_z_r
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lista-01'))
from report_part1 import wykres_do_base64
import numpy as np
import pandas as pd

dane, _ = wczytaj_i_przygotuj_dane()

cph = CoxPHFitter()
cph.fit(
    dane,
    duration_col='time',
    event_col='event',
    formula="C(trt) + age + bili + albumin + C(edema) + C(stage)"
)


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
_, patient_profile1 = wczytaj_i_przygotuj_dane(0.5)
_, patient_profile2 = wczytaj_i_przygotuj_dane(1)
print(patient_profile1)
print(patient_profile2)


hazard_function1 = cph.predict_cumulative_hazard(patient_profile1)
hazard_function2 = cph.predict_cumulative_hazard(patient_profile2)

t1 = hazard_function1.index.values
t2 = hazard_function2.index.values

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard_function1, label="edema=0.5")
    plt.plot(t2, hazard_function2, label="edema=1")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard H(t)")
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt


def fig2():
    lnhazard_function1 = np.log(hazard_function1)
    lnhazard_function2 = np.log(hazard_function2)

    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard_function1, label="edema=0.5")
    plt.plot(t2, lnhazard_function2, label="edema=1")
    plt.xlabel("Czas (dni)")
    plt.ylabel("ln H(t)")
    plt.title('Logarytm funkcji przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt

# 5 6
survival_function1 = cph.predict_survival_function(patient_profile1)
survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival1 = survival_at_time_interp(survival_function1.iloc[:, 0], 2000)
prob_survival2 = survival_at_time_interp(survival_function2.iloc[:, 0], 2000)
prob_survival = survival_at_time_interp(survival_function1.iloc[:, 0], 2000)


def fig3():
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function1.index, survival_function1.values)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.axhline(y=prob_survival1, color='r', linestyle='--', label=f'S(2000) = {prob_survival1:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt

def fig3old():
    plt = fig3()
    plt.plot(survival_function2.index, survival_function2.values)
    plt.axhline(y=prob_survival2, color='r', linestyle='--', label=f'S(2000) = {prob_survival2:.4f}')
    return plt



def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)

t_star = 2000
prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

print(f"P(T > 2000) dla edema=0.5: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
print(f"P(T > 2000) dla edema=1: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")
dane = wczytaj_dane_z_r()

def fig5():
    plt.figure(figsize=(10, 6))
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='Model PH (edema=0.5)')

    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia pacjenta (PO vs Cox)', fontsize=14, fontweight='bold')
    plt.plot(survival_function1.index, survival_function1.values, label="Model Coxa", linestyle='--')
    plt.legend()
    plt.xlim(0, 4000)
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def przeslij_dane2():
    return {
        "cph_summary": cph.summary,
        "cph_params": cph.params_,
        "fig11": fig11(),
        "fig12": fig12(),
        "fig1": wykres_do_base64(fig1()),
        "fig2": wykres_do_base64(fig2()),
        "fig3": wykres_do_base64(fig3old()),
        "fig5": fig5(),
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
        "fig11": wykres_do_base64(fig11()),
        "fig12": wykres_do_base64(fig12()),
    }