import numpy as np
from scipy.stats import beta
# from report_part1 import wzor_do_base64

# --- Dane dla leku A ---
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

bez_remisji_A = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

# --- Dane dla leku B ---
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

# 10 pacjentow bez remisji (cenzurowanie w czasie 1.0)
bez_remisji_B = np.array([
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0
])

A = np.concatenate((remisja_A, bez_remisji_A))
B = np.concatenate((remisja_B, bez_remisji_B))




# zad pierwsze bledy pierwszego typu
# 1A
L_A = len(remisja_A) / (np.sum(remisja_A) + (len(A) - len(remisja_A))) #0.70 
L_B = len(remisja_B) / (np.sum(remisja_B) + (len(B) - len(remisja_B))) #0.74


print(f'L_A: {L_A}')
print(f'L_B: {L_B}')

# 1B
def binom_confint(x, alpha=0.05):
    n = len(A)
    lower = np.where(x>0, beta.ppf(alpha / 2, x, n - x + 1), 0.0)
    upper = np.where(x<n, beta.ppf(1 - alpha / 2, x + 1, n - x), 1.0)
    return (lower, upper)

def confidence_interval(data, alpha=0.05):
    ext = binom_confint(data, alpha)
    Tl, Tu = ext
    Tl = - np.log(1 - Tl)
    Tu = - np.log(1 - Tu)
    return (Tl, Tu)

print(confidence_interval(A, 0.05)) #0.76 #3.15
print(confidence_interval(B, 0.05))
print(confidence_interval(A, 0.01))
print(confidence_interval(B, 0.01))

# binom.confint(x,n,conflevel = 1-alpha, method = 'exact')
# do przedzialu ufności

# zad drugie bledy drugiego typu
# 2A
m = 10
n = 20

remisja_A_sorted = np.sort(remisja_A)
remisja_B_sorted = np.sort(remisja_B)

L_A = m / (np.sum(remisja_A) + ((n - m)*remisja_A_sorted[-1]))
L_B = m / (np.sum(remisja_B) + ((n - m)*remisja_B_sorted[-1]))

print(f'L_Acenzored: {L_A}') # 0.73
print(f'L_Bcenzored: {L_B}') # 0.96

# 2B
def confidence_interval_censored(alpha, data, n_censored):
    alpha = alpha / 2
    p = 1 - np.exp()
    Tl = 1
    Tu = 1
    return (Tl, Tu)
