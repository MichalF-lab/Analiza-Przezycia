from math import gamma
import numpy as np
from numpy.random import seed
from scipy.stats import beta, gamma
from report_part2 import first_type_error
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
def confidence_interval_type1(data, alpha):
    n = len(data)
    R = np.sum(data < np.max(data))
    temp_L = beta.ppf(alpha / 2, R, n - R + 1)
    temp_U = beta.ppf(1 - alpha / 2, R + 1, n - R)
    theta_L = -np.log(1 - temp_L)
    theta_U = -np.log(1 - temp_U)

    return theta_L, theta_U

print(confidence_interval_type1(A, 0.05)) #0.76 #3.15
print(confidence_interval_type1(B, 0.05))
print(confidence_interval_type1(A, 0.01))
print(confidence_interval_type1(B, 0.01))

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
def confidence_interval_type2(data, alpha):
    n = len(data)
    m = np.sum(data < np.max(data))
    data = np.sort(data)
    data_uncenzored = data[:m]

    sum_di = 0
    for i in range(len(data_uncenzored)):
        sum_di += (len(data) - i + 1) * (data_uncenzored[i] - data_uncenzored[i - 1]) if i > 0 else (len(data) - i + 1) * data_uncenzored[i]

    sum_Di = np.sum(data_uncenzored) + (n - m) * data[m - 1]
    temp_L = gamma.ppf(alpha / 2, a=m, scale=1/m)
    temp_U = gamma.ppf(1 - (alpha / 2), a=m, scale=1/m) 
    theta_L = (m / sum_Di) * temp_L
    theta_U = (m / sum_Di) * temp_U

    return theta_L, theta_U

print(confidence_interval_type2(A, 0.05))
print(confidence_interval_type2(B, 0.05))
print(confidence_interval_type2(A, 0.01))
print(confidence_interval_type2(B, 0.01))

np.random.seed(42)
temp1 = first_type_error(0.5, n=10)
temp2 = first_type_error(0.5, n=30)
temp3 = first_type_error(1.2, n=10)
temp4 = first_type_error(1.2, n=30)
