import math
import pandas as pd
import numpy as np
import os
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lista-01'))
from report_part1 import wykres_do_base64 # 1 2

def wczyuj_i_przygotuj_dane_lung(): 
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

    # Odpowiednik: fit_aft = survreg(Surv(time, status) ~ as.factor(sex) + as.factor(censored) + data = dane,
    #                                  dist = "weibull")
    return lung_encoded

lung_encoded = wczyuj_i_przygotuj_dane_lung()
#print(len(lung_encoded))

from lifelines import WeibullAFTFitter

fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
#print(fit_aft.summary)

# 3
def wczytaj_i_przygotuj_dane_pacjentki(ph = 1):

    url = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"
    lung_original = pd.read_csv(url)
    lung_original = lung_original[["time","status","age", "sex", "ph.ecog", "ph.karno"]]
    lung_original = lung_original.dropna()
    age_mean = lung_original['age'].mean()
    ph_karno_mean = lung_original['ph.karno'].mean()

    # Definicja profilu pacjenta z CENTROWANYMI wartościami
    patient_profile = pd.DataFrame({
        'sex': [1],                      # 1 = kobieta (po mapowaniu 2->1)
        'ph.ecog_1.0': [1 if ph == 1 else 0],
        'ph.ecog_2.0': [1 if ph == 2 else 0],
        'ph.ecog_3.0': [1 if ph == 3 else 0],
        'age': [70 - age_mean],          # WYCENTROWANY wiek
        'ph.karno': [90 - ph_karno_mean] # WYCENTROWANE ph.karno
    })
    return patient_profile

survival_function = fit_aft.predict_survival_function(wczytaj_i_przygotuj_dane_pacjentki())

prob_survival = survival_function.loc[300].values[0]

#print(f"Prawdopodobieństwo, że czas życia > 300 dni: {prob_survival:.4f}")
#print(f"Czyli około: {prob_survival * 100:.2f}%")

# 4
import matplotlib.pyplot as plt

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function.index, survival_function.values)
    plt.axhline(y=prob_survival, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival:.4f}')
    plt.axvline(x=300, color='r', linestyle='--', alpha=0.5)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt


# ... (wcześniejszy kod z importami i fit_aft zostaje)

def wczytaj_dane_z_r():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    dane = {
        'baseline_survival': pd.read_csv(os.path.join(script_dir, 'baseline_survival.csv')),
        'baseline_cumhazard': pd.read_csv(os.path.join(script_dir, 'baseline_cumhazard.csv')),
        'baseline_hazard': pd.read_csv(os.path.join(script_dir, 'baseline_hazard.csv')),  
        'survival_ph1': pd.read_csv(os.path.join(script_dir, 'survival_ph1.csv')),
        'survival_ph2': pd.read_csv(os.path.join(script_dir, 'survival_ph2.csv')),
        'cumhazard_ph1': pd.read_csv(os.path.join(script_dir, 'cumhazard_ph1.csv')),
        'cumhazard_ph2': pd.read_csv(os.path.join(script_dir, 'cumhazard_ph2.csv')),
        'hazard_ph1': pd.read_csv(os.path.join(script_dir, 'hazard_ph1.csv')), 
        'hazard_ph2': pd.read_csv(os.path.join(script_dir, 'hazard_ph2.csv'))  
    }
    
    return dane

def fig2(dane):
    t1 = dane['hazard_ph1']['time'].values
    t2 = dane['hazard_ph2']['time'].values
    hazard1 = dane['hazard_ph1']['value'].values
    hazard2 = dane['hazard_ph2']['value'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard1, 'b-', linewidth=2, label="ph.ecog=1")
    plt.plot(t2, hazard2, 'r-', linewidth=2, label="ph.ecog=2")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("Hazard h(t)", fontsize=12)
    plt.title("Funkcja hazardu – kobieta, wiek=70, ph.karno=90", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig3(dane):
    hazard1 = dane['hazard_ph1']['value'].values
    hazard2 = dane['hazard_ph2']['value'].values
    
    epsilon = 1e-10
    lnhazard1 = np.log(hazard1 + epsilon)
    lnhazard2 = np.log(hazard2 + epsilon)
    
    t1 = dane['hazard_ph1']['time'].values
    t2 = dane['hazard_ph2']['time'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard1, 'b-', linewidth=2, label="ph.ecog=1")
    plt.plot(t2, lnhazard2, 'r-', linewidth=2, label="ph.ecog=2")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("ln h(t)", fontsize=12)
    plt.title("Logarytm funkcji hazardu – kobieta, wiek=70, ph.karno=90", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def survival_at_time(survival_df, t_star):
    times = survival_df['time'].values
    values = survival_df['value'].values
    return np.interp(t_star, times, values)


def fig4():
    dane = wczytaj_dane_z_r()
    
    t_star = 300
    prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
    prob_survival2 = survival_at_time(dane['survival_ph2'], t_star)
    
    plt.figure(figsize=(10, 6))
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='ph.ecog=1')
    plt.plot(dane['survival_ph2']['time'], 
             dane['survival_ph2']['value'], 
             'r-', linewidth=2.5, label='ph.ecog=2')
    plt.axhline(y=prob_survival1, color='b', linestyle='--', alpha=0.5,
                label=f'S₁(300) = {prob_survival1:.4f}')
    plt.axhline(y=prob_survival2, color='r', linestyle='--', alpha=0.5,
                label=f'S₂(300) = {prob_survival2:.4f}')
    plt.axvline(x=300, color='green', linestyle='--', alpha=0.5)
    plt.scatter([300, 300], [prob_survival1, prob_survival2], 
                color=['blue', 'red'], s=100, zorder=5)
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcje przeżycia – kobieta, wiek=70, ph.karno=90',
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    return plt

def fig5():
    plt = fig1()
    dane = wczytaj_dane_z_r()
    t_star = 300
    prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='ph.ecog=1')
    plt.axhline(y=prob_survival1, color='b', linestyle='--', alpha=0.5,
                label=f'S₁(300) = {prob_survival1:.4f}')
    plt.axvline(x=300, color='green', linestyle='--', alpha=0.5)
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcje przeżycia – kobieta, wiek=70, ph.karno=90',
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    return plt


def przeslij_dane1():
    dane_r = wczytaj_dane_z_r()
    
    return {
        "fit_aft": fit_aft.summary,
        "prob_survival": prob_survival,
        "fig1": wykres_do_base64(fig1()),
        "fig2": fig2(dane_r),
        "fig3": fig3(dane_r),
        "fig4": wykres_do_base64(fig4()),
        "fig5": wykres_do_base64(fig5()),
        "prob_survival1": survival_at_time(dane_r['survival_ph1'], 300),
        "prob_survival2": survival_at_time(dane_r['survival_ph2'], 300)
    }