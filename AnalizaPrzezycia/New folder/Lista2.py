"""
Generator PDF - Główny plik Lista 2
Generuje profesjonalne raporty PDF z wykresami i kodem
"""

from weasyprint import HTML, CSS
from datetime import datetime
import os
from report2_part1 import przeslij_dane1 as przeslij_dane2_1
from report2_part2 import przeslij_dane2 as przeslij_dane2_2
from report2_part3 import przeslij_dane3 as przeslij_dane2_3
from report2_part4 import przeslij_dane4 as przeslij_dane2_4


def wczytaj_plik(nazwa_pliku, encoding='utf-8'):
    """Wczytuje zawartość pliku"""
    try:
        with open(nazwa_pliku, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠ Nie znaleziono pliku: {nazwa_pliku}")
        return None
    except Exception as e:
        print(f"❌ Błąd wczytywania {nazwa_pliku}: {e}")
        return None

def stworz_html(d5, d6, d7, d8):
    template = wczytaj_plik("szablon2.html")
    if not template:
        return None

    html = template

    # ---------------------------
    # LISTA 5
    # ---------------------------
    html = html.replace("{{DATA}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    html = html.replace("{{WYKRES_KM_AB}}", d5['wykres_km_ab'])
    html = html.replace("{{WYKRES_FH_AB}}", d5['wykres_fh_ab'])
    html = html.replace("{{WNIOSKI_LEKI_AB}}", d5['wnioski_leki_ab'])

    html = html.replace("{{WYKRES_KM_OGON_AB}}", d5['wykres_km_ogon_ab'])
    html = html.replace("{{S_MAX_A}}", d5['s_max_a'])
    html = html.replace("{{THETA_A}}", d5['theta_a'])
    html = html.replace("{{S_MAX_B}}", d5['s_max_b'])
    html = html.replace("{{THETA_B}}", d5['theta_b'])

    html = html.replace("{{WYKRES_HIST_T0}}", d5['wykres_hist_t0'])
    html = html.replace("{{WYKRES_HIST_2T0}}", d5['wykres_hist_2t0'])

    for key in [
        'mean_n30_t0','std_n30_t0','shapiro_n30_t0',
        'mean_n30_2t0','std_n30_2t0','shapiro_n30_2t0',
        'mean_n50_t0','std_n50_t0','shapiro_n50_t0',
        'mean_n50_2t0','std_n50_2t0','shapiro_n50_2t0',
        'mean_n100_t0','std_n100_t0','shapiro_n100_t0',
        'mean_n100_2t0','std_n100_2t0','shapiro_n100_2t0'
    ]:
        html = html.replace("{{" + key.upper() + "}}", d5[key])


    # ---------------------------
    # LISTA 6
    # ---------------------------
    html = html.replace("{{MEAN_A_KM}}", d6['mean_A_KM'])
    html = html.replace("{{MEAN_A_FH}}", d6['mean_A_FH'])
    html = html.replace("{{DIFF_A}}", d6['diff_A'])

    html = html.replace("{{MEAN_B_KM}}", d6['mean_B_KM'])
    html = html.replace("{{MEAN_B_FH}}", d6['mean_B_FH'])
    html = html.replace("{{DIFF_B}}", d6['diff_B'])

    html = html.replace("{{POROWNANIE_MEAN}}", d6['porownanie_mean'])

    # ---------------------------
    # LISTA 7
    # ---------------------------
    html = html.replace("{{TAU1}}", str(d7['tau1']))
    html = html.replace("{{TAU2}}", str(d7['tau2']))

    for key in [
        'ci_low_tau1_l','ci_low_tau1_u','ci_low_tau1_w',
        'ci_high_tau1_l','ci_high_tau1_u','ci_high_tau1_w',
        'ci_low_tau2_l','ci_low_tau2_u','ci_low_tau2_w',
        'ci_high_tau2_l','ci_high_tau2_u','ci_high_tau2_w'
    ]:
        html = html.replace("{{" + key.upper() + "}}", d7[key])

    html = html.replace("{{POROWNANIE_CI}}", d7['porownanie_ci'])

    # ---------------------------
    # LISTA 8
    # ---------------------------
    html = html.replace("{{LOGRANK_STAT}}", d8['logrank_stat'])
    html = html.replace("{{LOGRANK_PVAL}}", d8['logrank_pvalue'])
    html = html.replace("{{LOGRANK_DECISION}}", d8['logrank_decision'])

    html = html.replace("{{BRESLOW_STAT}}", d8['breslow_stat'])
    html = html.replace("{{BRESLOW_PVAL}}", d8['breslow_pvalue'])
    html = html.replace("{{BRESLOW_DECISION}}", d8['breslow_decision'])

    html = html.replace("{{TARONE_STAT}}", d8['tarone_stat'])
    html = html.replace("{{TARONE_PVAL}}", d8['tarone_pvalue'])
    html = html.replace("{{TARONE_DECISION}}", d8['tarone_decision'])

    html = html.replace("{{PETO_STAT}}", d8['peto_stat'])
    html = html.replace("{{PETO_PVAL}}", d8['peto_pvalue'])
    html = html.replace("{{PETO_DECISION}}", d8['peto_decision'])

    html = html.replace("{{WYKRES_KM_GRUPY}}", d8['wykres_km'])

    html = html.replace("{{WYKRES_FUNKCJE_WAG1}}", d8['wykres_funkcje_wag1'])
    html = html.replace("{{WYKRES_FUNKCJE_WAG2}}", d8['wykres_funkcje_wag2'])
    
    return html


def sprawdz_pliki():
    """Sprawdza czy wszystkie wymagane pliki istnieją"""
    wymagane_pliki = [
        'szablon2.html', 'style.css',
        'report2_part1.py', 'report2_part2.py', 'report2_part3.py', 'report2_part4.py'
    ]
    brakujace = []
    
    for plik in wymagane_pliki:
        if not os.path.exists(plik):
            brakujace.append(plik)
    
    if brakujace:
        print("\n❌ Brakujące pliki:")
        for plik in brakujace:
            print(f"   - {plik}")
        return False
    
    return True


def generuj_pdf(nazwa_pliku="raport.pdf"):
    """Główna funkcja generująca PDF"""
    print("=" * 60)
    print("  GENERATOR PDF - Raport Kompletny (Lista 1 + Lista 2)")
    print("=" * 60)
    
    # Sprawdź pliki
    if not sprawdz_pliki():
        print("\n💡 Upewnij się, że wszystkie pliki są w tym samym katalogu!")
        return False
    
    
    print("\n🔧 Generowanie danych Lista 2...")
    try:
        dane2_1 = przeslij_dane2_1()
        dane2_2 = przeslij_dane2_2()
        dane2_3 = przeslij_dane2_3()
        dane2_4 = przeslij_dane2_4()
    except Exception as e:
        print(f"❌ Błąd generowania danych Lista 2: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("📄 Ładowanie szablonu HTML...")
    html_content = stworz_html(dane2_1, dane2_2, dane2_3, dane2_4)
    if not html_content:
        return False
    
    print("🎨 Ładowanie stylów CSS...")
    css_content = wczytaj_plik('style.css')
    if not css_content:
        return False
    
    print("📊 Generowanie PDF...")
    try:
        HTML(string=html_content).write_pdf(
            nazwa_pliku,
            stylesheets=[CSS(string=css_content)]
        )
        print(f"\n✅ PDF wygenerowany pomyślnie!")
        print(f"📁 Lokalizacja: {os.path.abspath(nazwa_pliku)}")
        return True
    except Exception as e:
        print(f"\n❌ Błąd podczas generowania PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Funkcja główna"""
    sukces = generuj_pdf("Raport_Kompletny.pdf")
    
    if sukces:
        print("\n" + "=" * 60)
        print("  ✅ Gotowe! Otwórz plik: Raport_Kompletny.pdf")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ❌ Wystąpił błąd podczas generowania")
        print("=" * 60)


if __name__ == "__main__":
    main()