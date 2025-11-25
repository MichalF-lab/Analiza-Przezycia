# mozna uzyc survfit

import numpy as np

from report_part2 import first_type_error


remisja_A = np.array([
    0.03345514,
    0.08656403,
    0.08799947,
    0.24385821,
    0.27755032,
    0.40787247,
    0.58825664,
    0.64125620,
    0.90679161,
    0.94222208
])

# 10 pacjentów bez remisji (cenzurowanie w czasie 1.0)
bez_remisji_A = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

# --- Dane dla leku B ---
# 10 pacjentów z remisją:
remisja_B = np.array([
    0.03788958,
    0.12207257,
    0.20319983,
    0.24474299,
    0.30492413,
    0.34224462,
    0.42950144,
    0.44484582,
    0.63805066,
    0.69119721
])

# 10 pacjentów bez remisji (cenzurowanie w czasie 1.0)
bez_remisji_B = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

A = np.concatenate((remisja_A, bez_remisji_A))
B = np.concatenate((remisja_B, bez_remisji_B))

def Kaplan_Meier(dane, t0=1.0):
    n = len(dane)
    wynik = 1
    m = np.sum(dane < np.max(dane))
    dane = np.sort(dane)
    dane_uncenzored = dane[:m]
    for i in range(m):
        wynik *= (1 - (1 / (n - i + 1)))
        if dane_uncenzored[i] >= t0:
            break
    return wynik

def Fleming_Harrington(dane, t0=1.0):
    n = len(dane)
    wynik = 0
    m = np.sum(dane < np.max(dane))
    dane = np.sort(dane)
    dane_uncenzored = dane[:m]
    for i in range(m):
        if dane_uncenzored[i] >= t0:
            break
        wynik += 1 / (n - i + 1)
    return np.exp(-wynik)