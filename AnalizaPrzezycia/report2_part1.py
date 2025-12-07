# mozna uzyc survfit

import numpy as np
import matplotlib.pyplot as plt
import math

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



def Kaplan_Meier(dane, t=0):
    n = len(dane)
    wynik = 1
    m = np.sum(dane < np.max(dane))
    dane = np.sort(dane)
    dane_uncenzored = dane[:m]
    for i in range(m):
        if dane_uncenzored[i] > t:
            break
        wynik *= (1 - (1 / (n - i)))
    return wynik

def Fleming_Harrington(dane, t=0):
    n = len(dane)
    wynik = 0
    m = np.sum(dane < np.max(dane))
    dane = np.sort(dane)
    dane_uncenzored = dane[:m]
    for i in range(m):
        if dane_uncenzored[i] > t:
            break
        wynik += 1 / (n - i)
    return np.exp(-wynik)

#print("Kaplan_Meier A:", Kaplan_Meier(A, t=0.5))
#print("Kaplan_Meier B:", Kaplan_Meier(B, t=0.5))

def generate_plot(func, dane):
    x = []
    y = []

    # generujemy punkty od 0 do 1
    N = 500
    for i in range(N):
        t = i / (N - 1)
        x.append(t)
        y.append(func(dane, t=t))

    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Wykres funkcji f(x)")
    plt.show()

#generate_plot(Kaplan_Meier, A)
#generate_plot(Kaplan_Meier, B)
#generate_plot(Fleming_Harrington, A)
#generate_plot(Fleming_Harrington, B)


def generate_plot2(func, dane1, dane2):
    x = []
    y = []

    # generujemy punkty od 0 do 1
    N = 500
    for i in range(N):
        t = i / (N - 1)
        x.append(t)
        y.append(func(dane1, t=t))
    plt.plot(x, y)

    x = []
    y = []
    for i in range(N):
        t = i / (N - 1)
        x.append(t)
        y.append(func(dane2, t=t))
    plt.plot(x, y)

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Wykres funkcji f(x)")
    plt.show()

#generate_plot2(Kaplan_Meier, A, B)
#generate_plot2(Fleming_Harrington, A, B)


def generate_plot3(func, dane):
    x = []
    y = []

    # generujemy punkty od 0 do 1
    N = 500
    for i in range(N):
        t = i / (N - 1)
        x.append(t)
        y.append(func(dane, t=t))
    
    temp = y[-1]
    theta = - 1 / math.log(temp)
    for i in range(N):
        t = (i / (N - 1)) + 1
        x.append(t)
        y.append(math.exp(-t / theta))
    for i in range(N):
        t = (i / (N - 1)) + 2
        x.append(t)
        y.append(math.exp(-t / theta))


    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Wykres funkcji f(x)")
    plt.show()

#generate_plot3(Kaplan_Meier, A)
#generate_plot3(Kaplan_Meier, B)


M = 10000
alpha = 0.667
lambdaa = 1.5
EXw = 0.505
n = [30, 50, 100]

def estimate_parameters_KM(dane, t0=EXw):
    n = len(dane)
    wynik = 1
    m = np.sum(dane < np.max(dane))
    dane = np.sort(dane)
    dane_uncenzored = dane[:m]
    for i in range(m):
        wynik *= (1 - (1 / (n - i)))
    temp = dane_uncenzored[-1]
    theta = - 1 / math.log(temp)
    wynik2 = math.exp(-2 / theta)
    return (wynik, wynik2)

dane = [[] for _ in n]
for i in range(M):
    for j in range(len(n)):
        dane[j].append(first_type_error(t0 =EXw, n=n[j], lambdaa=lambdaa, alpha=alpha))



from scipy.stats import norm

ext = []
for j in dane:
    for i in j:
        ext.append(estimate_parameters_KM(i, t0=EXw))
    temp = [x[0] for x in ext]
    plt.hist(temp, bins=18, alpha=0.5, density=True, label=f'n={n[dane.index(j)]} - KM Estimator')
    plt.plot((x := np.linspace(min(temp), max(temp), 300)),
         norm.pdf(x, np.mean(temp), np.std(temp)))

    plt.show()