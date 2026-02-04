# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri, Formula
from rpy2.robjects.conversion import localconverter
from report3_part1 import wczyuj_i_przygotuj_dane_lung, wczytaj_i_przygotuj_dane_pacjentki
from report_part1 import wzor_do_base64

os.environ['LANGUAGE'] = 'en'
os.environ['LC_ALL'] = 'C'

def load_r_environment():
    r_script = """
    options(repos = c(CRAN = "https://cloud.r-project.org"), warn = -1)
    suppressMessages({
        if(!require("survival")) install.packages("survival", quiet=TRUE)
        if(!require("timereg")) install.packages("timereg", quiet=TRUE)
        library(survival)
        library(timereg)
    })
    """
    try:
        ro.r(r_script)
        return True
    except Exception as e:
        print(f"Błąd R: {e}")
        return False

load_r_environment()

class ProportionalOddsFitter:
    def __init__(self):
        self.params_ = None
        self.summary = None
        self._coef_values = None
        self._coef_names = None
        self._baseline_times = None
        self._baseline_cum_odds = None
        self.baseline_survival_ = None
        self.baseline_cumulative_hazard_ = None

    def fit(self, df, duration_col='time', event_col='status'):
        df_r = df.copy().select_dtypes(include=[np.number])
        covariates = [col for col in df_r.columns if col not in [duration_col, event_col]]
        formula_str = f"Surv({duration_col}, {event_col}) ~ {' + '.join(covariates)}"
        
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_data = ro.conversion.py2rpy(df_r)
            ro.globalenv['temp_data'] = r_data
            ro.r(f"model_r <- timereg::prop.odds({formula_str}, data=temp_data, Nit=40, detail=0)")
            model = ro.r('model_r')

        gamma = np.array(model.rx2('gamma'))
        self._coef_names = list(model.rx2('var.name'))
        self._coef_values = gamma[:, 0]
        
        cum_matrix = np.array(model.rx2('cum'))
        self._baseline_times = cum_matrix[:, 0]
        self._baseline_cum_odds = cum_matrix[:, 1]

        self.params_ = pd.Series(self._coef_values, index=self._coef_names)
        self.summary = pd.DataFrame({
            'coef': gamma[:, 0],
            'se': gamma[:, 1],
            'p-val': gamma[:, 2]
        }, index=self._coef_names)

        self.baseline_survival_ = pd.DataFrame(
            1 / (1 + np.exp(self._baseline_cum_odds)), 
            index=self._baseline_times, columns=['baseline_survival']
        )
        self.baseline_cumulative_hazard_ = -np.log(self.baseline_survival_)
        
        return self

    def predict_survival_function(self, X):
        X_vals = X[self._coef_names].values
        linear_predictor = np.dot(X_vals, self._coef_values).reshape(-1, 1)
        base_odds = self._baseline_cum_odds.reshape(1, -1)
        surv_matrix = 1 / (1 + np.exp(base_odds + linear_predictor))
        return pd.DataFrame(surv_matrix.T, index=self._baseline_times)

    def predict_cumulative_hazard(self, X):
        return -np.log(self.predict_survival_function(X))

lung_encoded = wczyuj_i_przygotuj_dane_lung()
cph = ProportionalOddsFitter()
cph.fit(lung_encoded, duration_col='time', event_col='status')

baseline_cumulative_hazard = cph.baseline_cumulative_hazard_
baseline_survival = cph.baseline_survival_

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
    plt.ylabel("Hazard h(t)")
    plt.title("Funkcja hazardu kobieta, wiek=70, ph.karno=90")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)

def fig2():
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
    return wzor_do_base64(plt)  

survival_function1 = cph.predict_survival_function(patient_profile1)
survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival = survival_function1.loc[300].values[0]

def fig3():
    plt.figure(figsize=(10, 6))
    plt.plot(survival_function1.index, survival_function1.values, label="ph=1")
    plt.plot(survival_function2.index, survival_function2.values, label="ph=2")
    plt.xlabel('Czas (dni)')
    plt.ylabel('Prawdopodobienstwo przezycia S(t)')
    plt.title('Funkcja przezycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90')
    plt.axhline(y=prob_survival, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival:.4f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)

def survival_at_time(S_df, t):
    times = S_df.index.values
    values = S_df.iloc[:, 0].values
    return np.interp(t, times, values)

t_star = 300
prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

def przeslij_dane3():
    res_fig1 = fig1()
    res_fig2 = fig2()
    res_fig3 = fig3()
    return {
        "cph_summary": cph.summary,
        "cph_params": cph.params_,
        "baseline_cumulative_hazard_head": baseline_cumulative_hazard.head(),
        "baseline_survival_head": baseline_survival.head(),
        "fig1": res_fig1,
        "fig2": res_fig2,
        "fig3": res_fig3,
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2
    }

print("Model dopasowany pomyślnie!")
print(cph.summary)