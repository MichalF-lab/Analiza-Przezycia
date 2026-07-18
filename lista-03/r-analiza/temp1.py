import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Wczytanie danych z plików CSV wygenerowanych przez R
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def wczytaj_dane_z_r():
    """Wczytuje pliki CSV wygenerowane przez kod R (z tego samego folderu co skrypt)"""
    # Pobierz ścieżkę do folderu, gdzie jest ten skrypt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    dane = {
        'baseline_survival': pd.read_csv(os.path.join(script_dir, 'baseline_survival.csv')),
        'baseline_cumhazard': pd.read_csv(os.path.join(script_dir, 'baseline_cumhazard.csv')),
        'survival_ph1': pd.read_csv(os.path.join(script_dir, 'survival_ph1.csv')),
        'survival_ph2': pd.read_csv(os.path.join(script_dir, 'survival_ph2.csv')),
        'cumhazard_ph1': pd.read_csv(os.path.join(script_dir, 'cumhazard_ph1.csv')),
        'cumhazard_ph2': pd.read_csv(os.path.join(script_dir, 'cumhazard_ph2.csv'))
    }
    
    print(f" Lokalizacja: {script_dir}")
    print(f" Liczba punktów czasowych: {len(dane['survival_ph1'])}")
    
    return dane

def hazard_from_cumhazard(cumhazard_df):
    t = cumhazard_df['time'].values
    H = cumhazard_df['value'].values
    h = np.gradient(H, t)
    return h

def survival_at_time(survival_df, t_star):
    times = survival_df['time'].values
    values = survival_df['value'].values
    return np.interp(t_star, times, values)

# ============================================================
# ZADANIE 7: Wykresy funkcji hazardu
# ============================================================

def fig2(dane):
    hazard1 = hazard_from_cumhazard(dane['cumhazard_ph1'])
    hazard2 = hazard_from_cumhazard(dane['cumhazard_ph2'])
    t1 = dane['cumhazard_ph1']['time'].values
    t2 = dane['cumhazard_ph2']['time'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, hazard1, 'b-', linewidth=2, label="ph.ecog=1")
    plt.plot(t2, hazard2, 'r-', linewidth=2, label="ph.ecog=2")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("Hazard h(t)", fontsize=12)
    plt.title("Funkcja hazardu – kobieta, wiek=70, ph.karno=90", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    return wzor_do_base64(plt)

def fig3(dane):
    """Wykres logarytmu funkcji hazardu (analogia do Twojego fig3)"""
    # Oblicz hazardy
    hazard1 = hazard_from_cumhazard(dane['cumhazard_ph1'])
    hazard2 = hazard_from_cumhazard(dane['cumhazard_ph2'])
    
    epsilon = 1e-10
    lnhazard1 = np.log(hazard1 + epsilon)
    lnhazard2 = np.log(hazard2 + epsilon)
    
    t1 = dane['cumhazard_ph1']['time'].values
    t2 = dane['cumhazard_ph2']['time'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, lnhazard1, 'b-', linewidth=2, label="ph.ecog=1")
    plt.plot(t2, lnhazard2, 'r-', linewidth=2, label="ph.ecog=2")
    plt.xlabel("Czas (dni)", fontsize=12)
    plt.ylabel("ln h(t)", fontsize=12)
    plt.title("Logarytm funkcji hazardu – kobieta, wiek=70, ph.karno=90", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    return wzor_do_base64(plt)

def fig_proporcjonalnosc(dane):
    """Wykres weryfikacji proporcjonalnych hazardów"""
    hazard1 = hazard_from_cumhazard(dane['cumhazard_ph1'])
    hazard2 = hazard_from_cumhazard(dane['cumhazard_ph2'])
    
    epsilon = 1e-10
    log_diff = np.log(hazard2 + epsilon) - np.log(hazard1 + epsilon)
    t1 = dane['cumhazard_ph1']['time'].values
    
    plt.figure(figsize=(10, 6))
    plt.plot(t1, log_diff, 'g-', linewidth=2)
    plt.axhline(y=np.mean(log_diff), color='r', linestyle='--', 
                linewidth=2, label=f'Średnia = {np.mean(log_diff):.3f}')
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('log h₂(t) - log h₁(t)', fontsize=12)
    plt.title('Różnica logarytmów hazardów (weryfikacja proporcjonalności)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    return wzor_do_base64(plt)

# ============================================================
# ZADANIE 8 & 9: Funkcje przeżycia
# ============================================================

def fig1(dane):
    """Wykres funkcji przeżycia dla ph.ecog=1 (analogia do Twojego fig1)"""
    t_star = 300
    prob_survival = survival_at_time(dane['survival_ph1'], t_star)
    
    plt.figure(figsize=(10, 6))
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5)
    plt.axhline(y=prob_survival, color='r', linestyle='--', 
                label=f'S(300) = {prob_survival:.4f}')
    plt.axvline(x=300, color='r', linestyle='--', alpha=0.5)
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcja przeżycia dla kobiety, wiek=70, ph.ecog=1, ph.karno=90',
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    
    return wzor_do_base64(plt)

def fig4(dane):
    """Wykres obu funkcji przeżycia (analogia do Twojego fig4)"""
    t_star = 300
    prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
    prob_survival2 = survival_at_time(dane['survival_ph2'], t_star)
    
    plt.figure(figsize=(10, 6))
    plt.plot(dane['survival_ph1']['time'], 
             dane['survival_ph1']['value'], 
             'b-', linewidth=2.5, label='ph.ecog=1')
    plt.plot(dane['survival_ph2']['time'], 
             dane['survival_ph2']['value'], 
             'r-', linewidth=2.5, label='ph.ecog=2')
    plt.axhline(y=prob_survival1, color='b', linestyle='--', alpha=0.5,
                label=f'S₁(300) = {prob_survival1:.4f}')
    plt.axhline(y=prob_survival2, color='r', linestyle='--', alpha=0.5,
                label=f'S₂(300) = {prob_survival2:.4f}')
    plt.axvline(x=300, color='green', linestyle='--', alpha=0.5)
    plt.scatter([300, 300], [prob_survival1, prob_survival2], 
                color=['blue', 'red'], s=100, zorder=5)
    plt.xlabel('Czas (dni)', fontsize=12)
    plt.ylabel('Prawdopodobieństwo przeżycia S(t)', fontsize=12)
    plt.title('Funkcje przeżycia – kobieta, wiek=70, ph.karno=90',
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    
    return wzor_do_base64(plt)

# ============================================================
# Funkcja główna (analogia do Twojego przeslij_dane1)
# ============================================================

def przeslij_dane_proportional_odds():
    """
    Główna funkcja zbierająca wszystkie wyniki
    (analogia do Twojego przeslij_dane1)
    """
    # Wczytaj dane
    dane = wczytaj_dane_z_r()
    
    # Oblicz prawdopodobieństwa w t=300
    t_star = 300
    prob_survival1 = survival_at_time(dane['survival_ph1'], t_star)
    prob_survival2 = survival_at_time(dane['survival_ph2'], t_star)
    
    # Oblicz mediany
    def find_median(survival_df):
        times = survival_df['time'].values
        values = survival_df['value'].values
        idx = np.argmin(np.abs(values - 0.5))
        return times[idx]
    
    median1 = find_median(dane['survival_ph1'])
    median2 = find_median(dane['survival_ph2'])
    
    # Weryfikacja proporcjonalnych hazardów
    hazard1 = hazard_from_cumhazard(dane['cumhazard_ph1'])
    hazard2 = hazard_from_cumhazard(dane['cumhazard_ph2'])
    epsilon = 1e-10
    log_diff = np.log(hazard2 + epsilon) - np.log(hazard1 + epsilon)
    
    # Generuj wszystkie wykresy
    wyniki = {
        # Prawdopodobieństwa
        "prob_survival": prob_survival1,
        "prob_survival1": prob_survival1,
        "prob_survival2": prob_survival2,
        
        # Mediany
        "median_survival1": median1,
        "median_survival2": median2,
        
        # Statystyki proporcjonalności
        "log_hazard_diff_mean": np.mean(log_diff),
        "log_hazard_diff_std": np.std(log_diff),
        "proporcjonalnosc_ok": np.std(log_diff) < 0.5,  # heurystyczny próg
        
        # Wykresy (w formacie base64)
        "fig1": fig1(dane),
        "fig2": fig2(dane),
        "fig3": fig3(dane),
        "fig4": fig4(dane),
        "fig_proporcjonalnosc": fig_proporcjonalnosc(dane),
        
        # Surowe dane (opcjonalnie, jeśli potrzebujesz)
        "dane": dane
    }
    
    return wyniki

# ============================================================
# UŻYCIE
# ============================================================

if __name__ == "__main__":
    # Uruchom analizę
    wyniki = przeslij_dane_proportional_odds()
    
    # Możesz teraz używać wyników, np.:
    # print(wyniki["prob_survival1"])
    # wyświetl wykres w Jupyter: display(HTML(f'<img src="{wyniki["fig1"]}"/>'))