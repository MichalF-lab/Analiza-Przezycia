import numpy as np
import matplotlib.pyplot as plt
from lifelines.statistics import logrank_test, multivariate_logrank_test
from report_part1 import wykres_do_base64

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
def process_survival_data(dane):
    times = []
    events = []  # 1 = zdarzenie, 0 = cenzurowane
    
    for item in dane:
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
#print("PODSUMOWANIE WSZYSTKICH TESTÓW")
#print("=" * 70)
#print(f"{'Test':<30} {'Statystyka':>12} {'p-value':>10} {'Istotny':>10}")
#print("-" * 70)
#print(f"{'Log-rank (Mantel-Cox)':<30} {result_logrank.test_statistic:>12.4f} {result_logrank.p_value:>10.4f} {'TAK' if result_logrank.p_value < 0.05 else 'NIE':>10}")
#print(f"{'Gehan-Breslow (Wilcoxon)':<30} {result_breslow.test_statistic:>12.4f} {result_breslow.p_value:>10.4f} {'TAK' if result_breslow.p_value < 0.05 else 'NIE':>10}")
#print(f"{'Tarone-Ware':<30} {result_tarone.test_statistic:>12.4f} {result_tarone.p_value:>10.4f} {'TAK' if result_tarone.p_value < 0.05 else 'NIE':>10}")
#print(f"{'Peto-Peto':<30} {result_peto.test_statistic:>12.4f} {result_peto.p_value:>10.4f} {'TAK' if result_peto.p_value < 0.05 else 'NIE':>10}")


from report2_part3 import Kaplan_Meier as Kaplan_Meier2

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
    #plt.show()

#generate_plot(Kaplan_Meier2, low)
#generate_plot(Kaplan_Meier2, high)

from report2_part3 import ri, di
def wykres(dane):
    t = np.linspace(0, max(dane[0]), 600)

    n_t = np.array([np.sum(dane[0] >= ti) for ti in t])
    S_t = np.ones_like(t)
    m = np.unique(dane[0][(dane[1] == 1)])
    for i in range(len(t)):
        prod = 1.0
        for event_time in m:
            if event_time <= t[i]:
                r_j = ri(dane, event_time)
                d_j = di(dane, event_time)
                if r_j > 0:
                    prod *= (1 - d_j / (r_j + 1))
        S_t[i] = prod


    w_logrank = np.ones_like(t)
    w_breslow = n_t
    w_tarone = np.sqrt(n_t)
    w_peto = S_t

    fig_w, axw = plt.subplots(figsize=(10, 6))

    axw.plot(t, w_logrank, label="Log-rank: w(t)=1", linewidth=2)
    axw.plot(t, w_breslow, label="Breslow/Gehan: w(t)=n(t)", linewidth=2)
    axw.plot(t, w_tarone, label="Tarone-Ware: w(t)=√n(t)", linewidth=2)
    axw.plot(t, w_peto, label="Peto-Peto: w(t)=S(t)", linewidth=2)

    axw.set_xlabel("t (czas – skalowany)", fontsize=12)
    axw.set_ylabel("waga w(t)", fontsize=12)
    axw.set_title("Funkcje wagowe testów porównawczych", fontsize=14, fontweight="bold")
    axw.grid(True, alpha=0.3)
    axw.legend(fontsize=11)

    return wykres_do_base64(fig_w)
wykres_funkcje_wag1 = wykres(process_survival_data(low))
wykres_funkcje_wag2 = wykres(process_survival_data(high))

def przeslij_dane4():
    """Zwraca dane dla Listy 8 - testy porównawcze"""
    print("   📊 Lista 8: Wykonywanie testów porównawczych...")

    # Przetwarzanie danych
    times_low, events_low = process_survival_data(low)
    times_high, events_high = process_survival_data(high)

    all_times = np.concatenate([times_low, times_high])
    all_events = np.concatenate([events_low, events_high])
    all_groups = np.array([0] * len(times_low) + [1] * len(times_high))

    # Testy
    result_logrank = logrank_test(times_low, times_high, events_low, events_high)
    result_breslow = multivariate_logrank_test(all_times, all_groups, all_events, weightings='wilcoxon')
    result_tarone = multivariate_logrank_test(all_times, all_groups, all_events, weightings='tarone-ware')
    result_peto = multivariate_logrank_test(all_times, all_groups, all_events, weightings='peto')

    # Decyzje
    decision_logrank = "Odrzucamy H₀" if float(result_logrank.p_value) < 0.05 else "Nie odrzucamy H₀"
    decision_breslow = "Odrzucamy H₀" if float(result_breslow.p_value) < 0.05 else "Nie odrzucamy H₀"
    decision_tarone = "Odrzucamy H₀" if float(result_tarone.p_value) < 0.05 else "Nie odrzucamy H₀"
    decision_peto = "Odrzucamy H₀" if float(result_peto.p_value) < 0.05 else "Nie odrzucamy H₀"



    # Wykres KM obu grup
    fig1, ax = plt.subplots(figsize=(10, 6))

    x_low = np.linspace(0, max(times_low), 400)
    x_high = np.linspace(0, max(times_high), 400)

    y_low = [Kaplan_Meier2(process_survival_data(low), t=t) for t in x_low]
    y_high = [Kaplan_Meier2(process_survival_data(high), t=t) for t in x_high]

    ax.plot(x_low, y_low, 'b-', label="Niski stopień")
    ax.plot(x_high, y_high, 'r-', label="Wysoki stopień")

    ax.set_xlabel("Czas (dni)")
    ax.set_ylabel("S(t)")
    ax.set_title("Krzywe Kaplana-Meiera")
    ax.legend()
    ax.grid(True, alpha=0.3)

    wykres_km_grupy = wykres_do_base64(fig1)


    return {
        'logrank_stat': f"{result_logrank.test_statistic:.4f}",
        'logrank_pvalue': f"{result_logrank.p_value:.6f}",
        'logrank_decision': decision_logrank,

        'breslow_stat': f"{result_breslow.test_statistic:.4f}",
        'breslow_pvalue': f"{result_breslow.p_value:.6f}",
        'breslow_decision': decision_breslow,

        'tarone_stat': f"{result_tarone.test_statistic:.4f}",
        'tarone_pvalue': f"{result_tarone.p_value:.6f}",
        'tarone_decision': decision_tarone,

        'peto_stat': f"{result_peto.test_statistic:.4f}",
        'peto_pvalue': f"{result_peto.p_value:.6f}",
        'peto_decision': decision_peto,

        'wykres_km': wykres_km_grupy,

        'wykres_funkcje_wag1': wykres_funkcje_wag1,
        'wykres_funkcje_wag2': wykres_funkcje_wag2
    }
