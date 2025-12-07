import numpy as np
from scipy import stats
from scipy.integrate import quad

alpha = 0.05

def Kaplan_Meier(dane, t=0):
    dane = np.sort(dane)
    n = len(dane)
    m = np.sum(dane < np.max(dane))
    wynik = 1.0
    dane_uncenzored = dane[:m]

    for i in range(m):
        if dane_uncenzored[i] > t:
            break
        wynik *= (1 - 1 / (n - i))

    return wynik


def mean_survival_KM(si, dane, tau):
    dane = np.sort(dane)
    area, _ = quad(lambda k: Kaplan_Meier(dane,k), si, tau, limit=100)
    s_max = Kaplan_Meier(dane, tau)
    tail = s_max * -1 / np.log(s_max)

    return area + tail


def ri(dane, si):
    t = dane[0]
    return np.sum(t >= si)


def di(dane, si):
    t = dane[0]
    delta = dane[1]
    return np.sum((t == si) & (delta == 1))

def przedzial_ufnosci_KM(dane, alpha=0.05, tau=0.5):
    t = dane[0]
    delta = dane[1]
    czasy = np.argsort(t)
    t = t[czasy]
    delta = delta[czasy]
    dane = np.array([t, delta])
    
    zdarzenia = t[delta == 1]
    zdarzenia = zdarzenia[zdarzenia <= tau]
    
    suma = 0.0
    for si in zdarzenia:
        if ri(dane, si) - di(dane, si) == 0:
            continue
        integral = mean_survival_KM(si, t, tau)
        suma += (integral**2) * di(dane, si) / (ri(dane, si) * (ri(dane, si) - di(dane, si)))
    
    se = np.sqrt(suma)
    z = stats.norm.ppf(1 - alpha / 2)
    mu_hat = mean_survival_KM(0, t, tau)
    
    lower = mu_hat - z * se
    upper = mu_hat + z * se
    
    return lower, upper

# def przedzial_ufnosci_KM(dane, alpha=0.05, tau=0.5):
#     t = dane[0]
#     delta = dane[1]
#     idx = np.argsort(t)
#     t = t[idx]
#     delta = delta[idx]
#     dane = np.array([t, delta])
#     zdarzenia = t[delta == 1]
#     D = len(zdarzenia)
#     sum_var = 0.0
#     n = len(t)
#     for si in zdarzenia:
#         if ri(dane, si) - di(dane, si) == 0:
#             continue
#         integral = mean_survival_KM(si, t, tau)
#         sum_var += (integral**2) * di(dane, si) / (ri(dane, si) * (ri(dane, si) - di(dane, si)))
#     var_hat = sum_var
#     se = np.sqrt(var_hat)
#     z = stats.norm.ppf(1 - alpha / 2)
#     lower = -z * se + mean_survival_KM(0, t, tau)
#     upper =  z * se + mean_survival_KM(0, t, tau)
#     return lower, upper



low = [
    28,89,175,195,309, "377+","393+","421+","447+",
    462,"709+","744+","770+","1106+","1206+"
]

high = [
    34,88,137,199,280,291,"299+","300+",
    309,351,358,369,369,370,375,382,392,
    "429+",451,"1119+"
]

def convert(dane):
    t = []
    d = []
    for x in dane:
        if isinstance(x, str) and x.endswith('+'):
            t.append(int(x[:-1]))
            d.append(0)
        else:
            t.append(int(x))
            d.append(1)
    return np.array(t), np.array(d)

t_low, d_low = convert(low)
t_high, d_high = convert(high)

dane_low = np.array([t_low, d_low])
dane_high = np.array([t_high, d_high])

tau = 500
ci_low = przedzial_ufnosci_KM(dane_low, 0.05, tau)
ci_high = przedzial_ufnosci_KM(dane_high, 0.05, tau)

print("PRZEDZIAŁY UFNOŚCI 95% DLA ŚREDNIEGO CZASU DO PROGRESJI:\n")

print("Niski stopień zaawansowania:")
print("  (", ci_low[0], ",", ci_low[1], ")\n")

print("Wysoki stopień zaawansowania:")
print("  (", ci_high[0], ",", ci_high[1], ")\n")