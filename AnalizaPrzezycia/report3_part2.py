# -*- coding: utf-8 -*-
from lifelines import CoxPHFitter
from report3_part1 import wczyuj_i_przygotuj_dane_lung, wczytaj_i_przygotuj_dane_pacjentki
import matplotlib.pyplot as plt

lung_encoded = wczyuj_i_przygotuj_dane_lung()

class ProportionalOddsFitter:
    
    def __init__(self):
        self.po_model = None
        self._coef_names = None
        self._coef_values = None
        self._baseline_times = None
        self._baseline_cum_odds = None
        self.params_ = None
        self.baseline_cumulative_hazard_ = None
        self.baseline_survival_ = None
        self.summary = None
    
    def fit(self, df, duration_col='time', event_col='status', formula=None):
        r_data = pandas2ri.py2rpy(df)
        
        if formula is None:
            covariates = [col for col in df.columns if col not in [duration_col, event_col]]
            formula_str = f"Surv({duration_col}, {event_col}) ~ {' + '.join(covariates)}"
        else:
            formula_str = formula
        
        formula_r = ro.r(formula_str)
        self.po_model = timereg.prop_odds(formula_r, data=r_data, Nit=40, detail=0)
        
        coef_matrix = np.array(self.po_model.rx2('gamma'))
        self._coef_names = list(self.po_model.rx2('var.name'))
        self._coef_values = coef_matrix[:, 0]
        
        self.params_ = pd.Series(self._coef_values, index=self._coef_names)
        
        cum_odds_matrix = np.array(self.po_model.rx2('cum'))
        self._baseline_times = cum_odds_matrix[:, 0]
        self._baseline_cum_odds = cum_odds_matrix[:, 1]
        
        self.baseline_cumulative_hazard_ = pd.DataFrame(
            {'baseline cumulative hazard': self._baseline_cum_odds},
            index=self._baseline_times
        )
        
        baseline_survival_vals = 1 / (1 + np.exp(self._baseline_cum_odds))
        self.baseline_survival_ = pd.DataFrame(
            {'baseline survival': baseline_survival_vals},
            index=self._baseline_times
        )
        
        self.summary = pd.DataFrame({
            'coef': coef_matrix[:, 0],
            'se(coef)': coef_matrix[:, 1],
            'z': coef_matrix[:, 0] / coef_matrix[:, 1],
            'p': coef_matrix[:, 3]
        }, index=self._coef_names)
        
        return self
    
    def _calculate_linear_predictor(self, X):
        linear_pred = 0
        for col in X.columns:
            if col in self._coef_names:
                idx = self._coef_names.index(col)
                linear_pred += X[col].values[0] * self._coef_values[idx]
        return linear_pred
    
    def predict_survival_function(self, X):
        linear_pred = self._calculate_linear_predictor(X)
        survival_vals = 1 / (1 + np.exp(self._baseline_cum_odds + linear_pred))
        return pd.DataFrame(survival_vals, index=self._baseline_times, columns=[0])
    
    def predict_cumulative_hazard(self, X):
        survival_func = self.predict_survival_function(X)
        return -np.log(survival_func)
    
cph = ProportionalOddsFitter()
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
