import random
import numpy as np
from scipy import stats
from report_part2 import first_type_error


def exp_likelihood_ratio_test(data, theta0):
    #n = len(data)
    r = np.sum(data < np.max(data))
    data = np.sort(data)
    data_uncenzored = data[:r]
    s = np.sum(data_uncenzored)  
    #t0 = data_uncenzored[-1]
    theta_hat = r / s

    def log_likelihood(theta, r, s):
        if theta <= 0:
            return -np.inf
        return r * np.log(theta) - theta * s


    log_L_mle = log_likelihood(theta_hat, r, s)
    log_L_h0 = log_likelihood(theta0, r, s)

    statistic = -2 * (log_L_h0 - log_L_mle)
    p_value = 1 - stats.chi2.cdf(statistic, df=1)

    return p_value


theta0 = 2.0
t0 = 1.5
n1 = 20
n2 = 50
N = 10000


def exp_likelihood_ratio_power_test(data, theta0, test_type, alpha = 0.05):
    #n = len(data)
    r = np.sum(data < np.max(data))
    data = np.sort(data)
    data_uncenzored = data[:r]
    s = np.sum(data_uncenzored)  
    #t0 = data_uncenzored[-1]
    theta_hat = r / s

    def log_likelihood(theta, r, s):
        if theta <= 0:
            return -np.inf
        return r * np.log(theta) - theta * s


    log_L_mle = log_likelihood(theta_hat, r, s)
    log_L_h0 = log_likelihood(theta0, r, s)

    statistic = -2 * (log_L_h0 - log_L_mle)
    p_value = 1 - stats.chi2.cdf(statistic, df=1)

    if test_type == "a":
        return p_value < alpha
    elif test_type == "b":
        return (theta_hat > theta0) and (p_value < alpha)
    elif test_type == "c":
        return (theta_hat < theta0) and (p_value < alpha)

temp = [(0.8,"a"), (1.2,"a"), (1.8,"a"), (2.1,"a"), (1.5,"b"), (2.0,"b"), (2.2,"b"), (3.0,"c"), (2.2,"c"), (2.1, "c")]

ext = []
for  (theta, test_type) in temp:
    reject_count = 0
    for _ in range(N):
        data1 = first_type_error(t0, n=n1, lambdaa=theta0, alpha=1)
        if exp_likelihood_ratio_power_test(data1, theta, test_type, alpha=0.05):
            reject_count += 1
    power = reject_count / N
    #print(f'Moc testu dla θ={theta}, typ={test_type}: n = 20 {power:.4f}')
    ext.append((theta, test_type, power))

print("\n")
for  (theta, test_type) in temp:
    reject_count = 0
    for _ in range(N):
        data1 = first_type_error(t0, n=n2, lambdaa=theta0, alpha=1)
        if exp_likelihood_ratio_power_test(data1, theta, test_type, alpha=0.05):
            reject_count += 1
    power = reject_count / N
    #print(f'Moc testu dla θ={theta}, typ={test_type}: n = 50 {power:.4f}')
    ext.append((theta, test_type, power))

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


# print(exp_likelihood_ratio_test(A, 1))
# p-value 0.0043 
# print(exp_likelihood_ratio_test(B, 1))

def przeslij_dane4():
    """
    Główna funkcja zwracająca dane z raport_part4
    """
    
    print("   📈 Dane zad4 - testy mocy:\n")
    
    # Przygotuj dane mocy testów w uporządkowanej strukturze
    moce_n20 = {}
    moce_n50 = {}
    
    # ext zawiera krotki (theta, test_type, power)
    # Pierwsze 10 elementów to n=20, kolejne 10 to n=50
    for i in range(10):
        theta, test_type, power = ext[i]
        key = f"{theta}_{test_type}"
        moce_n20[key] = power
    
    for i in range(10, 20):
        theta, test_type, power = ext[i]
        key = f"{theta}_{test_type}"
        moce_n50[key] = power
    
    # p-values dla leków
    p_value_A = exp_likelihood_ratio_test(A, 1)
    p_value_B = exp_likelihood_ratio_test(B, 1)
    
    return {
        'moce_n20': moce_n20,
        'moce_n50': moce_n50,
        'p_value_A': p_value_A,
        'p_value_B': p_value_B,
        'theta0': theta0,
        'n1': n1,
        'n2': n2,
        'N': N
    }