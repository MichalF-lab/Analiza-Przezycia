# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

from report3_part1 import wczyuj_i_przygotuj_dane_lung, wczytaj_i_przygotuj_dane_pacjentki
from report_part1 import wykres_do_base64

os.environ['LANGUAGE'] = 'en'
os.environ['LC_ALL'] = 'C'

lung_encoded = wczyuj_i_przygotuj_dane_lung()

load_r_environment()

def make_person_period(df, time_col="time", status_col="status", max_t=None):
    if max_t is None:
        max_t = int(df[time_col].max())
    
    rows = []
    for _, row in df.iterrows():
        t_event = int(row[time_col])
        event = int(row[status_col])

        for t in range(1, min(t_event, max_t) + 1):
            new_row = row.copy()
            new_row["interval"] = t
            new_row["y"] = 1 if (t == t_event and event == 1) else 0
            rows.append(new_row)

    return pd.DataFrame(rows)

        cum_matrix = np.array(model.rx2('cum'))
        self._baseline_times = cum_matrix[:, 0]
        self._baseline_cum_odds = cum_matrix[:, 1]

max_time = int(lung_encoded['time'].max())
long_df = make_person_period(lung_encoded, max_t=max_time)

covariates = ["age","sex","ph.karno","ph.ecog_1.0","ph.ecog_2.0","ph.ecog_3.0"]
y = long_df["y"]
X_main = long_df[covariates]

time_vals = long_df["interval"]
X_time = pd.DataFrame({
    't': time_vals,
    't2': time_vals**2,
    't3': time_vals**3,
})
X = pd.concat([X_main, X_time], axis=1)
X = sm.add_constant(X)
X = X.astype(float)
y = y.astype(float)

model = sm.Logit(y, X)
result = model.fit()

params_df = pd.DataFrame({
    "Zmienna": result.params.index,
    "Wspolczynnik": result.params.values,
    "Exp(coef)": np.exp(result.params.values)
})

        self.baseline_survival_ = pd.DataFrame(
            1 / (1 + np.exp(self._baseline_cum_odds)), 
            index=self._baseline_times, columns=['baseline_survival']
        )
        self.baseline_cumulative_hazard_ = -np.log(self.baseline_survival_)

def predict_survival_curve(result, patient_profile, max_t=None):
    if max_t is None:
        max_t = max_time
    
    surv = 1.0
    survival_values = [1.0]
    cumhaz_values = [0.0]
    
    for t in range(1, max_t + 1):
        full_row = patient_profile.copy()
        full_row["const"] = 1.0
        full_row["t"] = float(t)
        full_row["t2"] = float(t**2)
        full_row["t3"] = float(t**3)

        Xp = pd.DataFrame([full_row])[result.params.index]
        h_t = result.predict(Xp).iloc[0]
        surv *= (1 - h_t)
        survival_values.append(surv)
        cumhaz_values.append(-np.log(max(surv, 1e-10)))

    return np.array(survival_values), np.array(cumhaz_values)

patient_profile1 = wczytaj_i_przygotuj_dane_pacjentki(ph=1)
patient_profile2 = wczytaj_i_przygotuj_dane_pacjentki(ph=2)

S1, H1 = predict_survival_curve(result, patient_profile1.iloc[0], max_t=max_time)
S2, H2 = predict_survival_curve(result, patient_profile2.iloc[0], max_t=max_time)

time_axis = np.arange(0, max_time + 1)


def fig11():
    baseline_profile = pd.Series({
        'age': lung_encoded['age'].mean(),
        'sex': 0,
        'ph.karno': lung_encoded['ph.karno'].mean(),
        'ph.ecog_1.0': 0,
        'ph.ecog_2.0': 0,
        'ph.ecog_3.0': 0
    })
    
    S_baseline, H_baseline = predict_survival_curve(result, baseline_profile, max_t=max_time)
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, H_baseline, label="Bazowa skumulowana funkcja hazardu", color='red', lw=2)
    plt.xlabel("Dni")
    plt.ylabel("H0(t)")
    plt.title("Bazowa skumulowana funkcja hazardu")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)


def fig12():
    """Baseline survival"""
    baseline_profile = pd.Series({
        'age': lung_encoded['age'].mean(),
        'sex': 0,
        'ph.karno': lung_encoded['ph.karno'].mean(),
        'ph.ecog_1.0': 0,
        'ph.ecog_2.0': 0,
        'ph.ecog_3.0': 0
    })
    
    S_baseline, H_baseline = predict_survival_curve(result, baseline_profile, max_t=max_time)
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, S_baseline, label="Bazowa funkcja przeaycia", color='blue', lw=2)
    plt.xlabel("Dni")
    plt.ylabel("S0(t)")
    plt.title("Bazowa funkcja przeaycia")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)

lung_encoded = wczyuj_i_przygotuj_dane_lung()
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cph.fit(lung_encoded, duration_col='time', event_col='status')
patient_profile1 = wczytaj_i_przygotuj_dane_pacjentki(ph=1)
patient_profile2 = wczytaj_i_przygotuj_dane_pacjentki(ph=2)
hazard_function1 = cph.predict_cumulative_hazard(patient_profile1)
hazard_function2 = cph.predict_cumulative_hazard(patient_profile2)

t1 = hazard_function1.index.values
t2 = hazard_function2.index.values

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, H1, label="PS: ph.ecog=1", linestyle='--')
    plt.plot(time_axis, H2, label="PS", linestyle='--')
    plt.plot(hazard_function1.index, hazard_function1.values, label="Cox: ph.ecog=1")
    plt.plot(hazard_function2.index, hazard_function2.values, label="Cox: ph.ecog=2")
    plt.xlabel("Dni")
    plt.ylabel("Skumulowany hazard H(t)")
    plt.title("Porównanie: PS vs Cox PH")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)

def fig2():
    lnhazard_function1 = np.log(hazard_function1.replace(0, 1e-10))
    lnhazard_function2 = np.log(hazard_function2.replace(0, 1e-10)) 
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis[1:], np.log(H1[1:]), label="PS: ph.ecog=1", linestyle='--')
    plt.plot(time_axis[1:], np.log(H2[1:]), label="PS: ph.ecog=2", linestyle='--')
    plt.plot(hazard_function1.index, lnhazard_function1.values, label="Cox: ph.ecog=1")
    plt.plot(hazard_function2.index, lnhazard_function2.values, label="Cox: ph.ecog=2")
    plt.xlabel("Dni")
    plt.ylabel("ln(H(t))")
    plt.title("Porównanie: PS vs Cox PH")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)

def fig3():
    survival_function1 = cph.predict_survival_function(patient_profile1)
    survival_function2 = cph.predict_survival_function(patient_profile2)
prob_survival = survival_function1.loc[300].values[0]
    
def fig3():
    plt.figure(figsize=(10, 6))
    # Discrete time model
    plt.plot(time_axis, S1, label="PS: ph.ecog=1", linestyle='--')
    plt.plot(time_axis, S2, label="PS: ph.ecog=2", linestyle='--')
    # Cox model
    plt.plot(survival_function1.index, survival_function1.values, label="Cox: ph.ecog=1")
    plt.plot(survival_function2.index, survival_function2.values, label="Cox: ph.ecog=2")
    plt.xlabel("Dni")
    plt.ylabel("S(t)")
    plt.title("Porównanie: PS vs Cox PH")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)

def fig5():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, S1, linestyle="--", label="PS: ph.ecog=1")
    plt.plot(time_axis, S2, linestyle="-", label="PS: ph.ecog=2")
    plt.xlabel("Dni")
    plt.ylabel("S(t)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    return wykres_do_base64(plt)


prob_survival1 = S1[300] if 300 < len(S1) else 0.0
prob_survival2 = S2[300] if 300 < len(S2) else 0.0

print(f"\nP(T > 300) dla ph.ecog=1: {prob_survival1:.4f} ({prob_survival1*100:.2f}%)")
print(f"P(T > 300) dla ph.ecog=2: {prob_survival2:.4f} ({prob_survival2*100:.2f}%)")

t_star = 300
prob_survival1 = survival_at_time(survival_function1, t_star)
prob_survival2 = survival_at_time(survival_function2, t_star)

def przeslij_dane3():
    summary_html = str(result.summary())

    return {
        "ordered_model_summary": summary_html,
        "ordered_model_params": params_df.set_index("Zmienna")["Wspolczynnik"],
        "fig11": fig11(),
        "fig12": fig12(),
        "fig1": fig1(),
        "fig2": fig2(),
        "fig3": fig3(),
        "fig5": fig5(),
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
    }

print("Model dopasowany pomyślnie!")
print(cph.summary)