# -*- coding: utf-8 -*-
from lifelines import LogLogisticAFTFitter
from report4_part1 import wczytaj_i_przygotuj_dane, survival_at_time_interp, wczytaj_dane_z_r
import matplotlib.pyplot as plt
from report_part1 import wykres_do_base64
import numpy as np
import pandas as pd
from report4_part2 import fig1, fig2, fig3

dane, _ = wczytaj_i_przygotuj_dane()


cph = LogLogisticAFTFitter()
cph.fit(
    dane,
    duration_col='time',
    event_col='event',
    formula="trt + age + bili + albumin + edema + stage"
)


print(cph.summary)
print(cph.params_)

def create_baseline_profile():
    _, baseline = wczytaj_i_przygotuj_dane(edema=0)
    baseline = pd.DataFrame({
        'trt': [2],
        'age': [0.0],
        'bili': [0.0],
        'albumin': [0.0],
        'edema': [0],
        'stage': [3]
        })
    return baseline

def fig11():
    baseline_profile = create_baseline_profile()
    baseline_hazard = cph.predict_cumulative_hazard(baseline_profile)
    plt.figure(figsize=(10, 6))
    plt.plot(baseline_hazard.index, baseline_hazard.iloc[:, 0], color='red', lw=2, label="Bazowy skumulowany hazard")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard H0(t)")
    plt.title("Bazowa skumulowana funkcja hazardu")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt

def fig12():
    baseline_profile = create_baseline_profile()
    baseline_survival = cph.predict_survival_function(baseline_profile)
    plt.figure(figsize=(10, 6))
    plt.plot(baseline_survival.index, baseline_survival.iloc[:, 0], color='blue', lw=2, label="Bazowe przezycie")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Prawdopodobienstwo przezycia S0(t)")
    plt.title("Bazowa funkcja przezycia")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt

# 4
_, patient_profile1 = wczytaj_i_przygotuj_dane(0.5)
_, patient_profile2 = wczytaj_i_przygotuj_dane(1)


hazard_function1 = cph.predict_cumulative_hazard(patient_profile1)
hazard_function2 = cph.predict_cumulative_hazard(patient_profile2)

t1 = hazard_function1.index.values
t2 = hazard_function2.index.values

def fig111():
    plt = fig1()
    plt.plot(t1, hazard_function1, label="edema=0.5")
    plt.plot(t2, hazard_function2, label="edema=1")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard H(t)")
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def fig22():
    lnhazard_function1 = np.log(hazard_function1)
    lnhazard_function2 = np.log(hazard_function2)

    plt = fig2()
    plt.plot(t1, lnhazard_function1, label="edema=0.5")
    plt.plot(t2, lnhazard_function2, label="edema=1")
    plt.xlabel("Czas (dni)")
    plt.ylabel("ln H(t)")
    plt.title('Logarytm funkcji przezycia pacjenta, bili=3, albumin=4', 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)  

# 5 6
survival_function1 = cph.predict_survival_function(patient_profile1)
survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival1 = survival_at_time_interp(survival_function1.iloc[:, 0], 2000)
prob_survival2 = survival_at_time_interp(survival_function2.iloc[:, 0], 2000)
prob_survival = survival_at_time_interp(survival_function1.iloc[:, 0], 2000)

def create_baseline_profile(dane = dane):
    # dla scentryzowanych zmiennych ciągłych baseline = 0
    baseline = pd.DataFrame({
        "trt":   [dane["trt"].cat.categories[0]],
        "age":   [0.0],
        "bili":  [0.0],
        "albumin":[0.0],
        "edema": [dane["edema"].cat.categories[0]],
        "stage": [dane["stage"].cat.categories[0]],
    })

    # narzuć dokładnie te same dtype Categorical co w danych uczących
    for col in ["trt", "edema", "stage"]:
        baseline[col] = pd.Categorical(baseline[col], categories=dane[col].cat.categories)

    return baseline

def fig33():
    plt.figure(figsize=(10, 6))
    S1 = survival_function1.iloc[:, 0]
    S2 = survival_function2.iloc[:, 0]

    plt.plot(S1.index, S1.values, label="edema=0.5")
    plt.plot(S2.index, S2.values, label="edema=1")

    t_star = 2000
    prob1 = np.interp(t_star, S1.index.values, S1.values)
    prob2 = np.interp(t_star, S2.index.values, S2.values)


    plt.axvline(x=t_star, linestyle="--", alpha=0.5)
    plt.axhline(y=prob1, linestyle="--", label=f"S1(2000)={prob1:.4f}")
    plt.axhline(y=prob2, linestyle="--", label=f"S2(2000)={prob2:.4f}")


    plt.xlabel("Czas (dni)")
    plt.ylabel("Prawdopodobienstwo przezycia S(t)")
    plt.title("Funkcja przezycia pacjenta")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)

t_star = 2000
prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

print(f"P(T > 2000) dla edema=0.5: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
print(f"P(T > 2000) dla edema=1: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")
dane_r = wczytaj_dane_z_r()

def fig5():
    S1 = survival_function1.iloc[:, 0]
    plt = fig3()
    plt.plot(S1.index, S1.values, label="edema=0.5")
    t_star = 2000
    prob1 = np.interp(t_star, S1.index.values, S1.values)
    plt.axhline(y=prob1, linestyle="--", label=f"S1(2000)={prob1:.4f}")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Prawdopodobienstwo przezycia S(t)")
    plt.title("Funkcja przezycia: PO vs COX")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def przeslij_dane3():
    return {
        "ordered_model_summary": cph.summary,
        "ordered_model_params": cph.params_,
        "fig1": fig111(),
        "fig2": fig22(),
        "fig3": fig33(),
        "fig5": fig5(),
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
        "fig11": wykres_do_base64(fig11()),
        "fig12": wykres_do_base64(fig12()),
    }