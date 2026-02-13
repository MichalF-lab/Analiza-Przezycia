import math
import pandas as pd
import numpy as np
import os
from report_part1 import wykres_do_base64
import pandas as pd
import numpy as np
from lifelines import WeibullAFTFitter
import matplotlib.pyplot as plt

def wczytaj_i_przygotuj_dane(edema=0.5):
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv"
    df = pd.read_csv(url, index_col=0)
    df = df[['time', 'status', 'trt', 'age', 'bili', 'albumin', 'edema', 'stage']]

    df = df[df['status'] != 1]
    df['event'] = (df['status'] == 2).astype(int)
    df = df.dropna(subset=['trt'])

    mean_age = df['age'].mean()
    mean_bili = df['bili'].mean()
    mean_albumin = df['albumin'].mean()

    df['age'] = df['age'] - mean_age
    df['bili'] = df['bili'] - mean_bili
    df['albumin'] = df['albumin'] - mean_albumin

    categorical_vars = ['trt', 'edema', 'stage']
    for col in categorical_vars:
        df[col] = df[col].astype('category')

    patient_data = pd.DataFrame({
        'trt': [2],
        'age': [40 - mean_age],
        'bili': [3 - mean_bili],
        'albumin': [4 - mean_albumin],
        'edema': [edema],
        'stage': [3]
    })

    
    for col in categorical_vars:
        df[col] = df[col].astype('category')
        patient_data[col] = pd.Categorical(patient_data[col], categories=df[col].cat.categories)

    return df, patient_data

df, patient_data = wczytaj_i_przygotuj_dane()
aft = WeibullAFTFitter()
fit_aft = aft.fit(df, duration_col='time', event_col='event', formula='trt + age + bili + albumin + edema + stage')


times = np.linspace(0, 4000, 400)
survival_function = fit_aft.predict_survival_function(patient_data, times=times)


def survival_at_time_interp(survival_series, t_star):
    times = survival_series.index.values
    values = survival_series.values.flatten()
    return np.interp(t_star, times, values)

prob_survival = survival_at_time_interp(survival_function.iloc[:, 0], 2000)

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function.index, survival_function.values)
    plt.axhline(y=prob_survival, color='r', linestyle='--', label=f'S(2000) = {prob_survival:.4f}')
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4, edema=0.5')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt


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

def fig2():
    dane = wczytaj_dane_z_r()
    t1 = dane['hazard_ph1']['time'].values
    t2 = dane['hazard_ph2']['time'].values
    hazard1 = dane['hazard_ph1']['value'].values
    hazard2 = dane['hazard_ph2']['value'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard1, 'b-', linewidth=2, label="edema=0.5")
    plt.plot(t2, hazard2, 'r-', linewidth=2, label="edema=1")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("Hazard h(t)", fontsize=12)
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig3():
    dane = wczytaj_dane_z_r()
    hazard1 = dane['hazard_ph1']['value'].values
    hazard2 = dane['hazard_ph2']['value'].values
    
    epsilon = 1e-10
    lnhazard1 = np.log(hazard1 + epsilon)
    lnhazard2 = np.log(hazard2 + epsilon)
    
    t1 = dane['hazard_ph1']['time'].values
    t2 = dane['hazard_ph2']['time'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard1, 'b-', linewidth=2, label="edema=0.5")
    plt.plot(t2, lnhazard2, 'r-', linewidth=2, label="edema=1")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("ln h(t)", fontsize=12)
    plt.title('Logarytm funkcji przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)


def survival_at_time(survival_df, t_star):
    times = survival_df['time'].values
    values = survival_df['value'].values
    return np.interp(t_star, times, values)
dane = wczytaj_dane_z_r()
    
t_star = 2000
prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
prob_survival2 = survival_at_time(dane['survival_ph2'], t_star)

def fig4():
    plt.figure(figsize=(10, 6))
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='edema=0.5')
    plt.plot(dane['survival_ph2']['time'], 
             dane['survival_ph2']['value'], 
             'r-', linewidth=2.5, label='edema=1')
    plt.axhline(y=prob_survival1, color='b', linestyle='--', alpha=0.5,
                label=f'S₁(2000) = {prob_survival1:.4f}')
    plt.axhline(y=prob_survival2, color='r', linestyle='--', alpha=0.5,
                label=f'S₂(2000) = {prob_survival2:.4f}')
    plt.scatter([2000, 2000], [prob_survival1, prob_survival2], 
                color=['blue', 'red'], s=100, zorder=5)
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    return plt

def fig5():
    plt_obj = fig1()
    dane = wczytaj_dane_z_r()
    t_star = 2000
    prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='edema=0.5')
    plt.axhline(y=prob_survival1, color='black', linestyle='--', label=f'S(2000) = {prob_survival1:.4f}')
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcja przezycia pacjenta, bili=3, albumin=4, edema=0.5', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    return plt

def przeslij_dane1():
    
    return {
        "fit_aft": fit_aft.summary,
        "prob_survival": prob_survival,
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
        "fig1": wykres_do_base64(fig1()),
        "fig2": fig2(),
        "fig3": fig3(),
        "fig4": wykres_do_base64(fig4()),
        "fig5": wykres_do_base64(fig5()),
    }