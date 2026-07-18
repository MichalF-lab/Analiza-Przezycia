import numpy as np
from report_part1 import wzor_do_base64

def dexp(lambdaa, alpha):
    t = np.random.rand()
    return -(1/lambdaa) * np.log(1 - t**(1/alpha))

def first_type_error(t0, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    delta = []
    for i in range(len(ext)):
        if ext[i] > t0:
            ext[i] = t0
            delta.append(0)   # obserwacja ocenzurowana
        else:
            delta.append(1)   # awaria zaobserwowana

    return ext, delta

#print(first_type_error(1))

def second_type_error(m, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    ext.sort()
    delta = [1] * m + [0] * (n - m)
    ext = ext[:m] + [ext[m-1]] * (n - m)
    return ext, delta

#print(second_type_error(5))

def random_type_error(eta, n = 10, lambdaa = 1, alpha = 1):
    ext = [dexp(lambdaa, alpha) for _ in range(n)]
    ext2 = [np.random.exponential(scale=eta) for _ in range(n)]
    ext3 = []
    delta = []
    for i in range(len(ext)):
        if ext[i] < ext2[i]:
            ext3.append(ext[i])
            delta.append(1)
        else:
            ext3.append(ext2[i])
            delta.append(0)
    return ext3, delta


#print(random_type_error(1))
def stats_type1(data, delta):
    def quantile(data, q):
        return np.percentile(data, q)

    complete = [data[i] for i in range(len(data)) if delta[i] == 1]
    return {
        'n': len(data),
        'n_complete': len(complete),
        'min_time': np.min(data),
        'median': np.median(complete) if len(complete) > 0 else None,
        'Q': quantile(complete, 25),
        'Q3': quantile(complete, 75),
        'IQR': quantile(complete, 75) - quantile(complete, 25)
    }

def stats_type2(data, delta, m):
    complete = [data[i] for i in range(len(data)) if delta[i] == 1]
    return {
        'n': len(data),
        'n_complete': m,
        'censoring_value': data[m-1],
        'max_time': np.max(data),
        'median': np.median(data) if len(complete) > 0 else None
    }

def stats_random(data, delta):
    times = np.array(data)
    complete = [data[i] for i in range(len(data)) if delta[i] == 1]
    censored = [data[i] for i in range(len(data)) if delta[i] == 0]
    
    stats = {
        'n': len(data),
        'n_complete': len(complete),
        'n_censored': len(censored),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'median': np.median(times)
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

t0 = 1.5
ext1, delta1 = first_type_error(t0, n=n, lambdaa=lambdaa, alpha=alpha)
stats1 = stats_type1(ext1, delta1)
# Typ II
m = 12
ext2, delta2 = second_type_error(m, n=n, lambdaa=lambdaa, alpha=alpha)
stats2 = stats_type2(ext2, delta2, m)
# Losowe
eta = 1.0
ext3, delta3 = random_type_error(eta, n=n, lambdaa=lambdaa, alpha=alpha)
stats3 = stats_random(ext3, delta3)


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

A = np.concatenate((remisja_A, bez_remisji_A))
B = np.concatenate((remisja_B, bez_remisji_B))

delta_A = np.array([1]*10 + [0]*10)
delta_B = np.array([1]*10 + [0]*10)

statsA = stats_type1(A, delta_A)
statsB = stats_type1(B, delta_B)


def przeslij_dane2():

    print(" Dane zad2:")
    dane1 = stats1
    dane2 = stats2
    dane3 = stats3
    
    print("Dane zad3:")
    daneA = statsA
    daneB = statsB

    print("\ Generowanie wzorów matematycznych:")
    # Funkcja gęstości (PDF)
    wzor_pdf_latex = r'f(x) = \alpha \lambda e^{-\lambda x} \left(1 - e^{-\lambda x}\right)^{\alpha - 1}, \quad x \geq 0'
    wzor_pdf = wzor_do_base64(wzor_pdf_latex, "Funkcja gęstości (PDF) \n")
    
    
    return {
        'WZOR_PDF': wzor_pdf,
        'dane1': dane1,
        'dane2': dane2,
        'dane3': dane3,
        'daneA': daneA,
        'daneB': daneB
    }
