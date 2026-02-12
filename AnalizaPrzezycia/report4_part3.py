# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from report_part1 import wykres_do_base64

def wczytaj_i_przygotuj_dane(edema_val=0.5):
    url = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv"
    df = pd.read_csv(url, index_col=0)
    df = df[['time', 'status', 'trt', 'age', 'bili', 'albumin', 'edema', 'stage']]
    df = df[df['status'] != 1]
    df['status'] = (df['status'] == 2).astype(int)
    df = df.dropna(subset=['trt', 'stage'])
    
    for col in ['trt', 'stage', 'edema']:
        df[col] = df[col].astype(str)
    
    mean_age = df['age'].mean()
    mean_bili = df['bili'].mean()
    mean_albumin = df['albumin'].mean()
    df['age'] = df['age'] - mean_age
    df['bili'] = df['bili'] - mean_bili
    df['albumin'] = df['albumin'] - mean_albumin
    
    patient_data = pd.DataFrame({
        'trt': [str(df['trt'].mode()[0])],
        'age': [0.0],
        'bili': [0.0],
        'albumin': [0.0],
        'edema': [str(edema_val)],
        'stage': [str(df['stage'].mode()[0])]
    })
    
    return df, patient_data

lung_encoded, _ = wczytaj_i_przygotuj_dane()
max_time = int(lung_encoded['time'].max())

def make_person_period(df):
    df_long = df.loc[df.index.repeat(df['time'])].copy()
    df_long['interval'] = df_long.groupby(level=0).cumcount() + 1
    df_long['y'] = 0
    df_long.loc[(df_long['interval'] == df_long['time']) & (df_long['status'] == 1), 'y'] = 1
    return df_long.reset_index(drop=True)

long_df = make_person_period(lung_encoded)
long_df['log_t'] = np.log(long_df['interval'])

formula = "y ~ age + bili + albumin + C(trt) + C(edema) + C(stage) + log_t"
model = smf.logit(formula, data=long_df)
result = model.fit(method='bfgs', maxiter=500)

summary_frame = result.summary2().tables[1]
summary_frame['Exp(coef)'] = np.exp(summary_frame['Coef.'])
ordered_summary = summary_frame[['Coef.', 'Exp(coef)', 'Std.Err.']]

def predict_survival_curve(res, p_profile, max_t=max_time):
    surv = 1.0
    s_vals = [1.0]
    
    prob_matrix = res.predict(pd.concat([p_profile]*max_t, ignore_index=True).assign(log_t=np.log(np.arange(1, max_t+1))))
    
    for h_t in prob_matrix:
        surv *= (1 - h_t)
        s_vals.append(surv)
        
    s_vals = np.array(s_vals)
    h_vals = -np.log(np.clip(s_vals, 1e-10, 1.0))
    return s_vals, h_vals

_, p1_df = wczytaj_i_przygotuj_dane(0.5)
_, p2_df = wczytaj_i_przygotuj_dane(1.0)

S1, H1 = predict_survival_curve(result, p1_df.iloc[0:1])
S2, H2 = predict_survival_curve(result, p2_df.iloc[0:1])
time_axis = np.arange(0, max_time + 1)

def fig11():
    plt.figure(figsize=(10, 6))
    base_prof = pd.DataFrame({'age':[0.0], 'bili':[0.0], 'albumin':[0.0], 'trt':['1.0'], 'edema':['0.0'], 'stage':['1.0']})
    _, H_0 = predict_survival_curve(result, base_prof)
    plt.plot(time_axis, H_0, color='red', label="H0(t)")
    plt.title("Bazowa skumulowana funkcja hazardu (Profile=0)")
    plt.xlabel("Dni")
    plt.ylabel("H0(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig12():
    plt.figure(figsize=(10, 6))
    base_prof = pd.DataFrame({'age':[0.0], 'bili':[0.0], 'albumin':[0.0], 'trt':['1.0'], 'edema':['0.0'], 'stage':['1.0']})
    S_0, _ = predict_survival_curve(result, base_prof)
    plt.plot(time_axis, S_0, color='blue', label="S0(t)")
    plt.title("Bazowa funkcja przezycia (Profile=0)")
    plt.xlabel("Dni")
    plt.ylabel("S0(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig1():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, H1, '--', label="PS: edema=0.5")
    plt.plot(time_axis, H2, '--', label="PS: edema=1.0")
    plt.title("Skumulowany hazard: Porownanie edema=0.5 vs 1.0")
    plt.xlabel("Dni")
    plt.ylabel("H(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig2():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis[1:], np.log(np.clip(H1[1:], 1e-10, None)), label="PS: edema=0.5")
    plt.plot(time_axis[1:], np.log(np.clip(H2[1:], 1e-10, None)), label="PS: edema=1.0")
    plt.title("Wykres ln(H(t)): Sprawdzenie zalozenia proporcjonalnosci")
    plt.xlabel("Dni")
    plt.ylabel("ln(H(t))")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig3():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, S1, '--', label="PS: edema=0.5")
    plt.plot(time_axis, S2, '--', label="PS: edema=1.0")
    plt.title("Funkcje przezycia modelu PS")
    plt.xlabel("Dni")
    plt.ylabel("S(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

def fig5():
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, S1, label="edema=0.5")
    plt.plot(time_axis, S2, label="edema=1.0")
    plt.title("Krzywe przezycia modelu Proporcjonalnych Szans")
    plt.xlabel("Dni")
    plt.ylabel("S(t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return wykres_do_base64(plt)

prob_survival1 = S1[2000] if 2000 < len(S1) else S1[-1]
prob_survival2 = S2[2000] if 2000 < len(S2) else S2[-1]

def przeslij_dane3():
    return {
        "ordered_model_summary": ordered_summary.to_html(),
        "ordered_model_params": result.params,
        "fig11": fig11(),
        "fig12": fig12(),
        "fig1": fig1(),
        "fig2": fig2(),
        "fig3": fig3(),
        "fig5": fig5(),
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2
    }