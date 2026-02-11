# mozna uzyc survfit

import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats

from report_part2 import first_type_error

from report_part1 import wykres_do_base64

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



def Kaplan_Meier2(dane, t=0):
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

#print("Kaplan_Meier A:", Kaplan_Meier(A, t=2))
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

    t_plus = np.max(dane_uncenzored)
    if t > t_plus:
        wynik = np.exp((np.log(wynik) / t_plus) * t)

    return wynik

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


ext = []
for j in dane:
    for i in j:
        ext.append(estimate_parameters_KM(i, t0=EXw))
    temp = [x[0] for x in ext]
    plt.hist(temp, bins=18, alpha=0.5, density=True, label=f'n={n[dane.index(j)]} - KM Estimator')
    plt.plot((x := np.linspace(min(temp), max(temp), 300)),
         stats.norm.pdf(x, np.mean(temp), np.std(temp)))

    #plt.show()

M = 1000
lambda_param = 1.5
alpha_param = 2.0
t0 = 0.723

wyniki_n30_t0 = []
wyniki_n30_2t0 = []
wyniki_n50_t0 = []
wyniki_n50_2t0 = []
wyniki_n100_t0 = []
wyniki_n100_2t0 = []
    
    
for i in range(M):

    dane30 = first_type_error(t0=t0, n=30, lambdaa=lambda_param, alpha=alpha_param)
    S_30_t0 = Kaplan_Meier(np.array(dane30), t=t0)
    wyniki_n30_t0.append(S_30_t0)
    max_dane30 = max(dane30)
    if 2*t0 > max_dane30:
        S_30_max = Kaplan_Meier(np.array(dane30), t=max_dane30)
        if S_30_max > 0 and S_30_max < 1:
            theta30 = -max_dane30 / np.log(S_30_max)
            S_30_2t0 = S_30_max * np.exp(-(2*t0 - max_dane30) / theta30)
        else:
            S_30_2t0 = 0 if S_30_max == 0 else S_30_max
    else:
        S_30_2t0 = Kaplan_Meier(np.array(dane30), t=2*t0)
    
    wyniki_n30_2t0.append(S_30_2t0)
        

    dane50 = first_type_error(t0=t0, n=50, lambdaa=lambda_param, alpha=alpha_param)
    S_50_t0 = Kaplan_Meier(np.array(dane50), t=t0)
    wyniki_n50_t0.append(S_50_t0)
    max_dane50 = max(dane50)
    if 2*t0 > max_dane50:
        S_50_max = Kaplan_Meier(np.array(dane50), t=max_dane50)
        if S_50_max > 0 and S_50_max < 1:
            theta50 = -max_dane50 / np.log(S_50_max)
            S_50_2t0 = S_50_max * np.exp(-(2*t0 - max_dane50) / theta50)
        else:
            S_50_2t0 = 0 if S_50_max == 0 else S_50_max
    else:
        S_50_2t0 = Kaplan_Meier(np.array(dane50), t=2*t0)
    
    wyniki_n50_2t0.append(S_50_2t0)
        

    dane100 = first_type_error(t0=t0, n=1000, lambdaa=lambda_param, alpha=alpha_param)
    S_100_t0 = Kaplan_Meier(np.array(dane100), t=t0)
    wyniki_n100_t0.append(S_100_t0)
    max_dane100 = max(dane100)
    if 2*t0 > max_dane100:
        S_100_max = Kaplan_Meier(np.array(dane100), t=max_dane100)
        if S_100_max > 0 and S_100_max < 1:
            theta100 = -max_dane100 / np.log(S_100_max)
            S_100_2t0 = S_100_max * np.exp(-(2*t0 - max_dane100) / theta100)
        else:
            S_100_2t0 = 0 if S_100_max == 0 else S_100_max
    else:
        S_100_2t0 = Kaplan_Meier(np.array(dane100), t=2*t0)
    
    wyniki_n100_2t0.append(S_100_2t0)


def przeslij_dane1():
    print("   📊 Lista 5: Generowanie estymatorów KM i FH...")
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 2, 500)
    y_A_KM = [Kaplan_Meier2(A, t=t) for t in x]
    y_B_KM = [Kaplan_Meier2(B, t=t) for t in x]
    
    ax1.plot(x, y_A_KM, 'b-', linewidth=2.5, label='Lek A')
    ax1.plot(x, y_B_KM, 'r-', linewidth=2.5, label='Lek B')
    ax1.set_xlabel('Czas (lata)', fontsize=12)
    ax1.set_ylabel('S(t) - Prawdopodobieństwo przeżycia', fontsize=12)
    ax1.set_title('Estymator Kaplana-Meiera', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1.05])
    wykres_km_ab = wykres_do_base64(fig1)
    

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    y_A_FH = [Fleming_Harrington(A, t=t) for t in x]
    y_B_FH = [Fleming_Harrington(B, t=t) for t in x]
    
    ax2.plot(x, y_A_FH, 'b-', linewidth=2.5, label='Lek A')
    ax2.plot(x, y_B_FH, 'r-', linewidth=2.5, label='Lek B')
    ax2.set_xlabel('Czas (lata)', fontsize=12)
    ax2.set_ylabel('S(t) - Prawdopodobieństwo przeżycia', fontsize=12)
    ax2.set_title('Estymator Fleminga-Harringtona', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1.05])
    wykres_fh_ab = wykres_do_base64(fig2)
    

    diff_km = np.mean(np.abs(np.array(y_A_KM) - np.array(y_B_KM)))
    diff_fh = np.mean(np.abs(np.array(y_A_FH) - np.array(y_B_FH)))
    
    if diff_km < 0.1 and diff_fh < 0.1:
        wnioski_ab = "krzywe przeżycia dla obu leków są bardzo zbliżone, co sugeruje podobne działanie leków A i B."
    else:
        wnioski_ab = "istnieją widoczne różnice między krzywymi przeżycia, szczególnie w późniejszych okresach obserwacji. Lek B wydaje się wykazywać nieco lepsze wyniki."
    

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    x_obs = np.linspace(0, 1, 300)
    y_A_obs = [Kaplan_Meier(A, t=t) for t in x_obs]
    ax3.plot(x_obs, y_A_obs, 'b-', linewidth=2.5, label='Lek A (obserwacje)')
    S_max_A = Kaplan_Meier(A, 1.0)
    theta_A = -1 / np.log(S_max_A) if S_max_A > 1e-10 else 1.0
    x_tail = np.linspace(1.0, 3.0, 200)
    y_A_tail = [S_max_A * np.exp(-(t - 1.0) / theta_A) for t in x_tail]
    ax3.plot(x_tail, y_A_tail, 'b--', linewidth=2, label='Lek A (ogon wykładniczy)')
    
    y_B_obs = [Kaplan_Meier(B, t=t) for t in x_obs]
    ax3.plot(x_obs, y_B_obs, 'r-', linewidth=2.5, label='Lek B (obserwacje)')
    S_max_B = Kaplan_Meier(B, 1.0)
    theta_B = -1 / np.log(S_max_B) if S_max_B > 1e-10 else 1.0
    y_B_tail = [S_max_B * np.exp(-(t - 1.0) / theta_B) for t in x_tail]
    ax3.plot(x_tail, y_B_tail, 'r--', linewidth=2, label='Lek B (ogon wykładniczy)')
    
    ax3.axvline(x=1.0, color='gray', linestyle=':', alpha=0.5, label='t_max')
    ax3.set_xlabel('Czas (lata)', fontsize=12)
    ax3.set_ylabel('S(t)', fontsize=12)
    ax3.set_title('Estymator KM z ogonem wykładniczym (Brown, Hollander, Kowar)', 
                  fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0, 1.05])
    wykres_km_ogon_ab = wykres_do_base64(fig3)
    
   
    fig4, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (wyniki, n_val) in enumerate([(wyniki_n30_t0, 30), (wyniki_n50_t0, 50), (wyniki_n100_t0, 100)]):
        mean_val = np.mean(wyniki)
        std_val = np.std(wyniki)
        axes[idx].hist(wyniki, bins=12, density=True, alpha=0.7, color='steelblue', edgecolor='black')
        x_norm = np.linspace(min(wyniki), max(wyniki), 100)
        axes[idx].plot(x_norm, stats.norm.pdf(x_norm, mean_val, std_val), 
                       'r-', linewidth=2, label='Rozkład normalny')
        axes[idx].set_title(f'n={n_val}, t=t₀', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Ŝ(t₀)')
        axes[idx].set_ylabel('Gęstość')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    wykres_hist_t0 = wykres_do_base64(fig4)
    
    # Histogramy dla 2t0
    fig5, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (wyniki, n_val) in enumerate([(wyniki_n30_2t0, 30), (wyniki_n50_2t0, 50), (wyniki_n100_2t0, 100)]):
        mean_val = np.mean(wyniki)
        std_val = np.std(wyniki)
        axes[idx].hist(wyniki, bins=12, density=True, alpha=0.7, color='coral', edgecolor='black')
        x_norm = np.linspace(min(wyniki), max(wyniki), 100)
        axes[idx].plot(x_norm, stats.norm.pdf(x_norm, mean_val, std_val), 
                       'b-', linewidth=2, label='Rozkład normalny')
        axes[idx].set_title(f'n={n_val}, t=2t₀', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Ŝ(2t₀)')
        axes[idx].set_ylabel('Gęstość')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    wykres_hist_2t0 = wykres_do_base64(fig5)
    
    stats_dict = {}
    for label, wyniki in [
        ('n30_t0', wyniki_n30_t0), ('n30_2t0', wyniki_n30_2t0),
        ('n50_t0', wyniki_n50_t0), ('n50_2t0', wyniki_n50_2t0),
        ('n100_t0', wyniki_n100_t0), ('n100_2t0', wyniki_n100_2t0)
    ]:
        _, p_val = stats.shapiro(wyniki)
        stats_dict[label] = {
            'mean': np.mean(wyniki),
            'std': np.std(wyniki),
            'shapiro_p': p_val
        }
    

    
    return {
        'wykres_km_ab': wykres_km_ab,
        'wykres_fh_ab': wykres_fh_ab,
        'wnioski_leki_ab': wnioski_ab,
        'wykres_km_ogon_ab': wykres_km_ogon_ab,
        's_max_a': f'{S_max_A:.4f}',
        'theta_a': f'{theta_A:.4f}',
        's_max_b': f'{S_max_B:.4f}',
        'theta_b': f'{theta_B:.4f}',
        'wykres_hist_t0': wykres_hist_t0,
        'wykres_hist_2t0': wykres_hist_2t0,
        'm_symulacji': M,
        'lambda': lambda_param,
        'alpha': alpha_param,
        't0_wartosc': f'{t0:.3f}',
        'mean_n30_t0': f'{stats_dict["n30_t0"]["mean"]:.4f}',
        'std_n30_t0': f'{stats_dict["n30_t0"]["std"]:.4f}',
        'shapiro_n30_t0': f'{stats_dict["n30_t0"]["shapiro_p"]:.4f}',
        'mean_n30_2t0': f'{stats_dict["n30_2t0"]["mean"]:.4f}',
        'std_n30_2t0': f'{stats_dict["n30_2t0"]["std"]:.4f}',
        'shapiro_n30_2t0': f'{stats_dict["n30_2t0"]["shapiro_p"]:.4f}',
        'mean_n50_t0': f'{stats_dict["n50_t0"]["mean"]:.4f}',
        'std_n50_t0': f'{stats_dict["n50_t0"]["std"]:.4f}',
        'shapiro_n50_t0': f'{stats_dict["n50_t0"]["shapiro_p"]:.4f}',
        'mean_n50_2t0': f'{stats_dict["n50_2t0"]["mean"]:.4f}',
        'std_n50_2t0': f'{stats_dict["n50_2t0"]["std"]:.4f}',
        'shapiro_n50_2t0': f'{stats_dict["n50_2t0"]["shapiro_p"]:.4f}',
        'mean_n100_t0': f'{stats_dict["n100_t0"]["mean"]:.4f}',
        'std_n100_t0': f'{stats_dict["n100_t0"]["std"]:.4f}',
        'shapiro_n100_t0': f'{stats_dict["n100_t0"]["shapiro_p"]:.4f}',
        'mean_n100_2t0': f'{stats_dict["n100_2t0"]["mean"]:.4f}',
        'std_n100_2t0': f'{stats_dict["n100_2t0"]["std"]:.4f}',
        'shapiro_n100_2t0': f'{stats_dict["n100_2t0"]["shapiro_p"]:.4f}'
    }
