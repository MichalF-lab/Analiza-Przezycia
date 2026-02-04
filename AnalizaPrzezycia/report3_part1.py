import math
import pandas as pd
import numpy as np
from report_part1 import wzor_do_base64 # 1 2
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
        'ph.ecog_1.0': [ph],
        'ph.ecog_2.0': [ph - 1],
        'ph.ecog_3.0': [0],
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
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)')
    plt.title('Funkcja przeżycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)

# 5 6 
fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
params = fit_aft.params_
rho = np.exp(params['rho_'])
sigma = 1 / rho

#print(f"rho = {rho.values[0]:.4f}")
#print(f"sigma = {sigma.values[0]:.4f}")

# Współczynniki gamma z modelu AFT (bez rho_ i lambda_)
gamma = params.drop(['rho_', 'lambda_'])
#print(gamma)

# Przekształcenie na współczynniki beta modelu PH: beta = -gamma/sigma
beta = -gamma / sigma.values[0]
#print(beta)
# najpierw dajemy parametry dopiero pozniej zmieniamy bete

# 7
patient1 , patient2 = wczytaj_i_przygotuj_dane_pacjentki(ph=1), wczytaj_i_przygotuj_dane_pacjentki(ph=2)


survival_function1 = fit_aft.predict_survival_function(patient1)
survival_function2 = fit_aft.predict_survival_function(patient2)

#cumulative_hazard1 = fit_aft.predict_cumulative_hazard(patient1)
#cumulative_hazard2 = fit_aft.predict_cumulative_hazard(patient2)
#
#hazard_function1 = cumulative_hazard1.diff().fillna(0)
#hazard_function2 = cumulative_hazard2.diff().fillna(0)

def hazard_from_survival(S_df, epsilon=1e-8):
    S = S_df.iloc[:, 0].values
    t = S_df.index.values
    return -np.gradient(np.log(S + epsilon), t)

hazard_function1 = hazard_from_survival(survival_function1)
hazard_function2 = hazard_from_survival(survival_function2)

lnhazard_function1 = np.log(hazard_function1)
lnhazard_function2 = np.log(hazard_function2)

t1 = survival_function1.index.values
t2 = survival_function2.index.values

def fig2():
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard_function1, label="ph=1")
    plt.plot(t2, hazard_function2, label="ph=2")
    plt.xlabel("Czas (dni)")
    plt.ylabel("Hazard h(t)")
    plt.title("Funkcja hazardu – kobieta, wiek=70, ph.karno=90")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)

def fig3():
    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard_function1, label="ph=1")
    plt.plot(t2, lnhazard_function2, label="ph=2")
    plt.xlabel("Czas (dni)")
    plt.ylabel("ln h(t)")
    plt.title("Logarytm funkcji hazardu – kobieta, wiek=70, ph.karno=90")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)


# 8 9 
def fig4():
    prob_survival = survival_function1.loc[300].values[0]
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function1.index, survival_function1.values)
    plt.plot(survival_function2.index, survival_function2.values)
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)')
    plt.title('Funkcja przeżycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.axhline(y=prob_survival, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)


# zad 9
def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)
t_star = 300

prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

#print(f"P(T > 300) dla ph=1: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
#print(f"P(T > 300) dla ph=2: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")

def przeslij_dane1():
    fit_aft = fit_aft.summary
    prob_survival = prob_survival
    fig1 = fig1()
    rho = rho.values[0]
    sigma = sigma.values[0]
    gamma = gamma
    beta = beta
    fig2 = fig2()
    fig3 = fig3()
    fig4 = fig4()
    prob_survival1 = prob_survival1
    prob_survival2 = prob_survival2
    return {
        "fit_aft": fit_aft,
        "prob_survival": prob_survival,
        "fig1": fig1,
        "rho": rho,
        "sigma": sigma,
        "gamma": gamma,
        "beta": beta,
        "fig2": fig2,
        "fig3": fig3,
        "fig4": fig4,
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2
    }