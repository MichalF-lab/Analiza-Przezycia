import numpy as np
from numpy import random

def dexp(lambdaa, alpha):
    t = random.rand()
    return -(1/lambdaa) * np.log(1 - t**(1/alpha))

def first_type_error(t0, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    for i in range(len(ext)):
        if ext[i] > t0:
            ext[i] = t0
    return ext

#print(first_type_error(1))

def second_type_error(m, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    ext.sort()
    ext = ext[:m]
    ext += [max(ext) for _ in range(n - m)]
    return ext

#print(second_type_error(5))

def random_type_error(eta, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    ext2 = [np.random.exponential(scale=eta) for _ in range(n)]
    ext3 = []
    for i in range(len(ext)):
        if ext[i] > ext2[i]:
            ext3.append((ext[i], 1))
        else:
            ext3.append((ext2[i], 0))
    return ext3

#print(random_type_error(1))

def stats_type1(data, t0):
    complete = [x for x in data if x < t0]
    return {
        'n': len(data),
        'n_complete': len(complete),
        'mean': np.mean(complete),
        'median': np.median(complete),
        'std': np.std(complete, ddof=1)
    }

def stats_type2(data, m):
    complete = data[:m]
    return {
        'n': len(data),
        'n_complete': m,
        'censoring_value': data[m],
        'mean': np.mean(complete),
        'median': np.median(complete),
        'std': np.std(complete, ddof=1)
    }

def stats_random(data):
    times = np.array([x[0] for x in data])
    complete = [x[0] for x in data if x[1] == 0]
    censored = [x[0] for x in data if x[1] == 1]
    
    stats = {
        'n': len(data),
        'n_complete': len(complete),
        'n_censored': len(censored),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'median_time': np.median(times)
    }
    
    if len(complete) > 0:
        stats['min_complete'] = np.min(complete)
        stats['max_complete'] = np.max(complete)
    if len(censored) > 0:
        stats['min_censored'] = np.min(censored)
        stats['max_censored'] = np.max(censored)
    
    return stats

# Generowanie danych
np.random.seed(42)
n = 20
lambdaa = 1.5
alpha = 2.0

# Typ I
t0 = 1.5
data1 = first_type_error(t0, n=n, lambdaa=lambdaa, alpha=alpha)
stats1 = stats_type1(data1, t0)

# Typ II
m = 12
data2 = second_type_error(m, n=n, lambdaa=lambdaa, alpha=alpha)
stats2 = stats_type2(data2, m)

# Losowe
eta = 1.0
data3 = random_type_error(eta, n=n, lambdaa=lambdaa, alpha=alpha)
stats3 = stats_random(data3)

import numpy as np

# --- Dane dla leku A ---
# 10 pacjentów z remisją:
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
