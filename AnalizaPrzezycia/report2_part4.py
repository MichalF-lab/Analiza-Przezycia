import numpy as np
from lifelines.statistics import logrank_test, multivariate_logrank_test

# Dane
low = [
    28, 89, 175, 195, 309, "377+", "393+", "421+", "447+",
    462, "709+", "744+", "770+", "1106+", "1206+"
]

high = [
    34, 88, 137, 199, 280, 291, "299+", "300+",
    309, 351, 358, 369, 369, 370, 375, 382, 392,
    "429+", 451, "1119+"
]

# Funkcja do przetworzenia danych z cenzurowaniem
def process_survival_data(data):
    times = []
    events = []  # 1 = zdarzenie, 0 = cenzurowane
    
    for item in data:
        if isinstance(item, str) and '+' in item:
            times.append(float(item.replace('+', '')))
            events.append(0)  # cenzurowane
        else:
            times.append(float(item))
            events.append(1)  # zdarzenie
    
    return np.array(times), np.array(events)

# Przetworzenie danych
times_low, events_low = process_survival_data(low)
times_high, events_high = process_survival_data(high)

# Przygotowanie danych dla testów multivariate
all_times = np.concatenate([times_low, times_high])
all_events = np.concatenate([events_low, events_high])
all_groups = np.array([0] * len(times_low) + [1] * len(times_high))

result_logrank = logrank_test(
    times_low, times_high,
    events_low, events_high
)

result_breslow = multivariate_logrank_test(
    all_times, all_groups, all_events,
    weightings='wilcoxon'
)

result_tarone = multivariate_logrank_test(
    all_times, all_groups, all_events,
    weightings='tarone-ware'
)

result_peto = multivariate_logrank_test(
    all_times, all_groups, all_events,
    weightings='peto'
)
print("PODSUMOWANIE WSZYSTKICH TESTÓW")
print("=" * 70)
print(f"{'Test':<30} {'Statystyka':>12} {'p-value':>10} {'Istotny':>10}")
print("-" * 70)
print(f"{'Log-rank (Mantel-Cox)':<30} {result_logrank.test_statistic:>12.4f} {result_logrank.p_value:>10.4f} {'TAK' if result_logrank.p_value < 0.05 else 'NIE':>10}")
print(f"{'Gehan-Breslow (Wilcoxon)':<30} {result_breslow.test_statistic:>12.4f} {result_breslow.p_value:>10.4f} {'TAK' if result_breslow.p_value < 0.05 else 'NIE':>10}")
print(f"{'Tarone-Ware':<30} {result_tarone.test_statistic:>12.4f} {result_tarone.p_value:>10.4f} {'TAK' if result_tarone.p_value < 0.05 else 'NIE':>10}")
print(f"{'Peto-Peto':<30} {result_peto.test_statistic:>12.4f} {result_peto.p_value:>10.4f} {'TAK' if result_peto.p_value < 0.05 else 'NIE':>10}")

import matplotlib.pyplot as plt

def Kaplan_Meier2(dane, t=0):
    times , events = process_survival_data(dane)
    
    temp = sorted(range(len(times)), key=lambda i: times[i])
    times_sorted = [times[i] for i in temp]
    events_sorted = [events[i] for i in temp]
    n = len(times_sorted)
    wynik = 1

    for i in range(n):
        if times_sorted[i] > t:
            continue
        if events_sorted[i] == 1:
            wynik *= (1 - 1 / (n - i)) #indekowane od 0
    return wynik

def generate_plot(func, dane):
    x = []
    y = []

    # znajdz maksymalny czas w danych
    max_time = max(float(item.replace('+', '')) if isinstance(item, str) else item
                   for item in dane)

    N = 500
    for i in range(N):
        t = (i / (N - 1)) * max_time
        x.append(t)
        y.append(func(dane, t=t))

    plt.plot(x, y)
    plt.xlabel("t")
    plt.ylabel("S(t)")
    plt.title("Kaplan-Meier")
    plt.grid(True)
    plt.show()

generate_plot(Kaplan_Meier2, low)
generate_plot(Kaplan_Meier2, high)
