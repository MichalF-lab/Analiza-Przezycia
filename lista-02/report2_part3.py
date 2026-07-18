import numpy as np
from scipy import stats
from scipy.integrate import quad

alpha = 0.05

def ri(dane, si):
    t = dane[0]
    return np.sum(t >= si)


def di(dane, si):
    t = dane[0]
    delta = dane[1]
    return np.sum((t == si) & (delta == 1))

def Kaplan_Meier(dane, t=0):
    wynik = 1
    m = np.unique(dane[0][(dane[1] == 1) & (dane[0] <= t)])
    for i in m:
        n = ri(dane, i)
        d = di(dane, i)
        wynik *= (1 - d / n)
    return wynik

def mean_survival_KM(si, dane, tau):
    area, _ = quad(lambda k: Kaplan_Meier(dane,k), si, tau, limit=100)
    s_max = Kaplan_Meier(dane, tau)
    tail = - s_max * tau / np.log(s_max)

    return area + tail


def przedzial_ufnosci_KM(dane, alpha=0.05, tau=0.5):
    t = dane[0]
    delta = dane[1]
    czasy = np.argsort(t)
    t = t[czasy]
    delta = delta[czasy]
    dane = np.array([t, delta])
    
    zdarzenia = t[delta == 1]
    zdarzenia = zdarzenia[zdarzenia <= tau]
    s_max = Kaplan_Meier(dane, tau)
    suma = 0.0

    for si in zdarzenia:
        if ri(dane, si) - di(dane, si) == 0:
            continue
        integral = mean_survival_KM(si, dane, tau)
        tail = - s_max * tau / np.log(s_max)
        suma += (integral + tail)**2 * di(dane, si) / (ri(dane, si) * (ri(dane, si) - di(dane, si)))
    
    se = np.sqrt(suma)
    z = stats.norm.ppf(1 - alpha / 2)
    mu_hat = mean_survival_KM(0, dane, tau)
    
    lower = mu_hat - z * se
    upper = mu_hat + z * se
    
    return lower, upper



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




def przeslij_dane3():
    """Zwraca dane dla Listy 7 - przedziały ufności"""
    print("   📊 Lista 7: Obliczanie przedziałów ufności...")
    
    # Dane (z treści zadania)
    tau1 = 500
    tau2 = 800
    
    t_low, d_low = convert(low)
    t_high, d_high = convert(high)
    
    dane_low = np.array([t_low, d_low])
    dane_high = np.array([t_high, d_high])
    
    # Przedziały dla tau1
    ci_low_tau1 = przedzial_ufnosci_KM(dane_low, 0.05, tau1)
    ci_high_tau1 = przedzial_ufnosci_KM(dane_high, 0.05, tau1)
    width_low_tau1 = ci_low_tau1[1] - ci_low_tau1[0]
    width_high_tau1 = ci_high_tau1[1] - ci_high_tau1[0]
    
    # Przedziały dla tau2
    ci_low_tau2 = przedzial_ufnosci_KM(dane_low, 0.05, tau2)
    ci_high_tau2 = przedzial_ufnosci_KM(dane_high, 0.05, tau2)
    width_low_tau2 = ci_low_tau2[1] - ci_low_tau2[0]
    width_high_tau2 = ci_high_tau2[1] - ci_high_tau2[0]
    
    
    if ci_low_tau1[0] > ci_high_tau1[1]:
        porownanie = f"Przedziały ufności dla obu grup nie nakładają się, co wskazuje na istotną statystycznie " \
                    f"różnicę w średnim czasie do progresji. Pacjentki z niskim stopniem zaawansowania mają " \
                    f"znacząco dłuższy średni czas do progresji. Zwiększenie τ z {tau1} do {tau2} dni " \
                    f"prowadzi do szerszych przedziałów (większa niepewność przy dłuższej ekstrapolacji)."
    else:
        porownanie = f"Przedziały ufności częściowo się nakładają, jednak grupa z niskim stopniem zaawansowania " \
                    f"wykazuje lepsze rokowania. Dla τ={tau2} przedziały są szersze " 
 
    
    
    return {
        'tau1': tau1,
        'tau2': tau2,
        'ci_low_tau1_l': f'{ci_low_tau1[0]:.2f}',
        'ci_low_tau1_u': f'{ci_low_tau1[1]:.2f}',
        'ci_low_tau1_w': f'{width_low_tau1:.2f}',
        'ci_high_tau1_l': f'{ci_high_tau1[0]:.2f}',
        'ci_high_tau1_u': f'{ci_high_tau1[1]:.2f}',
        'ci_high_tau1_w': f'{width_high_tau1:.2f}',
        'ci_low_tau2_l': f'{ci_low_tau2[0]:.2f}',
        'ci_low_tau2_u': f'{ci_low_tau2[1]:.2f}',
        'ci_low_tau2_w': f'{width_low_tau2:.2f}',
        'ci_high_tau2_l': f'{ci_high_tau2[0]:.2f}',
        'ci_high_tau2_u': f'{ci_high_tau2[1]:.2f}',
        'ci_high_tau2_w': f'{width_high_tau2:.2f}',
        'porownanie_ci': porownanie
    }