import pandas as pd
import numpy as np

# 1. Wczytanie pliku
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
print(lung_encoded.head())
# Zakładając, że masz DataFrame 'data' z kolumnami: time, status, sex

# Odpowiednik: fit_aft = survreg(Surv(time, status) ~ as.factor(sex) + as.factor(censored) + data = dane,
#                                  dist = "weibull")

from lifelines import WeibullAFTFitter

fit_aft = WeibullAFTFitter().fit(lung_encoded, duration_col='time', event_col='status', formula='sex + ph.ecog_1.0 + ph.ecog_2.0 + ph.ecog_3.0 + age + ph.karno')
print(fit_aft.summary)