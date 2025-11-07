"""
Generator PDF - Główny plik
Generuje profesjonalne raporty PDF z wykresami i kodem
"""

from weasyprint import HTML, CSS
from datetime import datetime
import os
from report_part1 import przeslij_dane1
from report_part2 import przeslij_dane2
from report_part3 import przeslij_dane3
from report_part4 import przeslij_dane4




def wczytaj_plik(nazwa_pliku, encoding='utf-8'):
    """Wczytuje zawartość pliku1"""
    try:
        with open(nazwa_pliku, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠ Nie znaleziono pliku: {nazwa_pliku}")
        return None
    except Exception as e:
        print(f"❌ Błąd wczytywania {nazwa_pliku}: {e}")
        return None
    

def stworz_html(dane1, dane2, dane3, dane4):
    """Tworzy kompletny HTML z danymi"""
    template = wczytaj_plik('szablon.html')
    if not template:
        return None


    # Zastąp placeholdery danymi
    html = template.replace('{{DATA}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    html = html.replace('{{WYKRES1}}', dane1['wykres1'])
    html = html.replace('{{WYKRES2}}', dane1['wykres2'])
 
    # Podmień wzory LaTeX jako obrazy base64
    html = html.replace('{{WZOR_PDF}}', dane1['WZOR_PDF'])
    html = html.replace('{{WZOR_CDF}}', dane1['WZOR_CDF'])
    html = html.replace('{{WZOR_KWANTYL}}', dane1['WZOR_KWANTYL'])
    html = html.replace('{{WZOR_HAZARD}}', dane1['WZOR_HAZARD'])

    html = html.replace('{{MEDIAN_THEO_243}}', f'{dane1["dane"]["theoretical_EW_243"]["median"]:.4f}')
    html = html.replace('{{MEDIAN_THEO_221}}', f'{dane1["dane"]["theoretical_EW_221"]["median"]:.4f}')
    html = html.replace('{{Q1_THEO_243}}', f'{dane1["dane"]["theoretical_EW_243"]["q1"]:.4f}')
    html = html.replace('{{Q1_THEO_221}}', f'{dane1["dane"]["theoretical_EW_221"]["q1"]:.4f}')
    html = html.replace('{{Q3_THEO_243}}', f'{dane1["dane"]["theoretical_EW_243"]["q3"]:.4f}')
    html = html.replace('{{Q3_THEO_221}}', f'{dane1["dane"]["theoretical_EW_221"]["q3"]:.4f}')
    html = html.replace('{{IQR_THEO_243}}', f'{dane1["dane"]["theoretical_EW_243"]["iqr"]:.4f}')
    html = html.replace('{{IQR_THEO_221}}', f'{dane1["dane"]["theoretical_EW_221"]["iqr"]:.4f}')

    for i in range(1, 5):
        sample = dane1["dane"][f"sample{i}"]
        html = html.replace(f'{{{{MEAN{i}}}}}', f'{sample["mean"]:.4f}')
        html = html.replace(f'{{{{MEDIAN{i}}}}}', f'{sample["median"]:.4f}')
        html = html.replace(f'{{{{STD{i}}}}}', f'{sample["std"]:.4f}')
        html = html.replace(f'{{{{Q1_{i}}}}}', f'{sample["q1"]:.4f}')
        html = html.replace(f'{{{{Q3_{i}}}}}', f'{sample["q3"]:.4f}')
        html = html.replace(f'{{{{IQR{i}}}}}', f'{sample["iqr"]:.4f}')
        html = html.replace(f'{{{{MIN{i}}}}}', f'{sample["min"]:.4f}')
        html = html.replace(f'{{{{MAX{i}}}}}', f'{sample["max"]:.4f}')
        html = html.replace(f'{{{{RANGE{i}}}}}', f'{sample["range"]:.4f}')

    # Cenzurowanie typu I
    html = html.replace('{{D1N}}', str(dane2["dane1"]["n"]))
    html = html.replace('{{D1NC}}', str(dane2["dane1"]['n_complete']))
    html = html.replace('{{D1M}}', f'{dane2["dane1"]["min_time"]:.4f}')
    html = html.replace('{{D1MED}}', f'{dane2["dane1"]["median"]:.4f}')
    html = html.replace('{{DAQ}}', f'{dane2["dane1"]["Q"]:.4f}')

    # Cenzurowanie typu II
    html = html.replace('{{D2N}}', str(dane2["dane2"]['n']))
    html = html.replace('{{D2NC}}', str(dane2["dane2"]['n_complete']))
    html = html.replace('{{D2CV}}', f'{dane2["dane2"]["censoring_value"]:.4f}')
    html = html.replace('{{D2MED}}', f'{dane2["dane2"]["median"]:.4f}')

    # Cenzurowanie losowe
    html = html.replace('{{D3N}}', str(dane2["dane3"]['n']))
    html = html.replace('{{D3NC}}', str(dane2["dane3"]['n_complete']))
    html = html.replace('{{D3NCEN}}', str(dane2["dane3"]['n_censored']))
    html = html.replace('{{D3MIN}}', f'{dane2["dane3"]["min_time"]:.4f}')
    html = html.replace('{{D3MAX}}', f'{dane2["dane3"]["max_time"]:.4f}')

    # Porównanie leków A i B
    html = html.replace('{{DAN}}', str(dane2["daneA"]['n']))
    html = html.replace('{{DANC}}', str(dane2["daneA"]['n_complete']))
    html = html.replace('{{DAM}}', f'{dane2["daneA"]["min_time"]:.4f}')
    html = html.replace('{{DAMED}}', f'{dane2["daneA"]["median"]:.4f}')
    html = html.replace('{{DAMED}}', f'{dane2["daneA"]["median"]:.4f}')

    html = html.replace('{{DBN}}', str(dane2["daneB"]['n']))
    html = html.replace('{{DBNC}}', str(dane2["daneB"]['n_complete']))
    html = html.replace('{{DBM}}', f'{dane2["daneB"]["min_time"]:.4f}')
    html = html.replace('{{DBMED}}', f'{dane2["daneB"]["median"]:.4f}')
    html = html.replace('{{DBQ}}', f'{dane2["daneB"]["Q"]:.4f}')

    # Lista3
    html = html.replace('{{EST_A_TYPE1}}', f'{dane3["est_A_type1"]:.4f}')
    html = html.replace('{{EST_B_TYPE1}}', f'{dane3["est_B_type1"]:.4f}')
    
    # Przedziały ufności typ I (α=0.05)
    html = html.replace('{{CI_A_005_L}}', f'{dane3["ci_A_005"][0]:.4f}')
    html = html.replace('{{CI_A_005_U}}', f'{dane3["ci_A_005"][1]:.4f}')
    html = html.replace('{{CI_B_005_L}}', f'{dane3["ci_B_005"][0]:.4f}')
    html = html.replace('{{CI_B_005_U}}', f'{dane3["ci_B_005"][1]:.4f}')
    
    # Przedziały ufności typ I (α=0.01)
    html = html.replace('{{CI_A_001_L}}', f'{dane3["ci_A_001"][0]:.4f}')
    html = html.replace('{{CI_A_001_U}}', f'{dane3["ci_A_001"][1]:.4f}')
    html = html.replace('{{CI_B_001_L}}', f'{dane3["ci_B_001"][0]:.4f}')
    html = html.replace('{{CI_B_001_U}}', f'{dane3["ci_B_001"][1]:.4f}')
    
    # Estymatory typ II
    html = html.replace('{{EST_A_TYPE2}}', f'{dane3["est_A_type2"]:.4f}')
    html = html.replace('{{EST_B_TYPE2}}', f'{dane3["est_B_type2"]:.4f}')
    
    # Przedziały ufności typ II (α=0.05)
    html = html.replace('{{CI2_A_005_L}}', f'{dane3["ci2_A_005"][0]:.4f}')
    html = html.replace('{{CI2_A_005_U}}', f'{dane3["ci2_A_005"][1]:.4f}')
    html = html.replace('{{CI2_B_005_L}}', f'{dane3["ci2_B_005"][0]:.4f}')
    html = html.replace('{{CI2_B_005_U}}', f'{dane3["ci2_B_005"][1]:.4f}')
    
    # Przedziały ufności typ II (α=0.01)
    html = html.replace('{{CI2_A_001_L}}', f'{dane3["ci2_A_001"][0]:.4f}')
    html = html.replace('{{CI2_A_001_U}}', f'{dane3["ci2_A_001"][1]:.4f}')
    html = html.replace('{{CI2_B_001_L}}', f'{dane3["ci2_B_001"][0]:.4f}')
    html = html.replace('{{CI2_B_001_U}}', f'{dane3["ci2_B_001"][1]:.4f}')
    
    # Bias
    for i in range(1, 9):
        html = html.replace(f'{{{{BIAS{i}}}}}', f'{dane3[f"bias{i}"]:.6f}')
    
    # MSE
    for i in range(1, 9):
        html = html.replace(f'{{{{MSE{i}}}}}', f'{dane3[f"mse{i}"]:.6f}')
    

    # Parametry testu
    html = html.replace('{{THETA0}}', f'{dane4["theta0"]:.1f}')
    html = html.replace('{{N1}}', str(dane4["n1"]))
    html = html.replace('{{N2}}', str(dane4["n2"]))
    html = html.replace('{{N_SIMULATIONS}}', str(dane4["N"]))
    
    # Moce testów dla n=20
    html = html.replace('{{MOC_N20_0_8_A}}', f'{dane4["moce_n20"]["0.8_a"]:.4f}')
    html = html.replace('{{MOC_N20_1_2_A}}', f'{dane4["moce_n20"]["1.2_a"]:.4f}')
    html = html.replace('{{MOC_N20_1_8_A}}', f'{dane4["moce_n20"]["1.8_a"]:.4f}')
    html = html.replace('{{MOC_N20_2_1_A}}', f'{dane4["moce_n20"]["2.1_a"]:.4f}')
    
    html = html.replace('{{MOC_N20_1_5_B}}', f'{dane4["moce_n20"]["1.5_b"]:.4f}')
    html = html.replace('{{MOC_N20_2_0_B}}', f'{dane4["moce_n20"]["2.0_b"]:.4f}')
    html = html.replace('{{MOC_N20_2_2_B}}', f'{dane4["moce_n20"]["2.2_b"]:.4f}')
    
    html = html.replace('{{MOC_N20_3_0_C}}', f'{dane4["moce_n20"]["3.0_c"]:.4f}')
    html = html.replace('{{MOC_N20_2_2_C}}', f'{dane4["moce_n20"]["2.2_c"]:.4f}')
    html = html.replace('{{MOC_N20_2_1_C}}', f'{dane4["moce_n20"]["2.1_c"]:.4f}')
    
    # Moce testów dla n=50
    html = html.replace('{{MOC_N50_0_8_A}}', f'{dane4["moce_n50"]["0.8_a"]:.4f}')
    html = html.replace('{{MOC_N50_1_2_A}}', f'{dane4["moce_n50"]["1.2_a"]:.4f}')
    html = html.replace('{{MOC_N50_1_8_A}}', f'{dane4["moce_n50"]["1.8_a"]:.4f}')
    html = html.replace('{{MOC_N50_2_1_A}}', f'{dane4["moce_n50"]["2.1_a"]:.4f}')
    
    html = html.replace('{{MOC_N50_1_5_B}}', f'{dane4["moce_n50"]["1.5_b"]:.4f}')
    html = html.replace('{{MOC_N50_2_0_B}}', f'{dane4["moce_n50"]["2.0_b"]:.4f}')
    html = html.replace('{{MOC_N50_2_2_B}}', f'{dane4["moce_n50"]["2.2_b"]:.4f}')
    
    html = html.replace('{{MOC_N50_3_0_C}}', f'{dane4["moce_n50"]["3.0_c"]:.4f}')
    html = html.replace('{{MOC_N50_2_2_C}}', f'{dane4["moce_n50"]["2.2_c"]:.4f}')
    html = html.replace('{{MOC_N50_2_1_C}}', f'{dane4["moce_n50"]["2.1_c"]:.4f}')
    
    # p-values i decyzje dla leków
    html = html.replace('{{P_VALUE_A}}', f'{dane4["p_value_A"]:.6f}')
    html = html.replace('{{P_VALUE_B}}', f'{dane4["p_value_B"]:.6f}')
    
    decision_A = "Odrzucamy H₀" if dane4["p_value_A"] < 0.05 else "Nie odrzucamy H₀"
    decision_B = "Odrzucamy H₀" if dane4["p_value_B"] < 0.05 else "Nie odrzucamy H₀"
    html = html.replace('{{DECISION_A}}', decision_A)
    html = html.replace('{{DECISION_B}}', decision_B)
    
    return html


    return html


def sprawdz_pliki():
    """"Sprawdza czy wszystkie wymagane pliki istnieją"""
    wymagane_pliki = ['szablon.html', 'style.css', 'report_part1.py', 'report_part2.py', 'report_part3.py', 'report_part4.py']
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
    print("  GENERATOR PDF - Raport z wykresami")
    print("=" * 60)
    
    # Sprawdź pliki
    if not sprawdz_pliki():
        print("\n💡 Upewnij się, że wszystkie pliki są w tym samym katalogu!")
        return False
    
    print("\n🔧 Generowanie danych lista1...")
    try:
        dane1 = przeslij_dane1()
    except Exception as e:
        print(f"❌ Błąd generowania danych: {e}")
        return False
    
    print("\n🔧 Generowanie danych lista2...")
    try:
        dane2 = przeslij_dane2()
    except Exception as e:
        print(f"❌ Błąd generowania danych: {e}")
        return False

        print("\n🔧 Generowanie danych lista3...")
    try:
        dane3 = przeslij_dane3()
    except Exception as e:
        print(f"❌ Błąd generowania danych: {e}")
        return False

    print("\n🔧 Generowanie danych lista4...")
    try:
        dane4 = przeslij_dane4()
    except Exception as e:
        print(f"❌ Błąd generowania danych: {e}")
        return False

    print("📄 Ładowanie szablonu HTML...")
    html_content = stworz_html(dane1, dane2, dane3, dane4)
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
        return False

def main():
    """Funkcja główna"""
    sukces = generuj_pdf("Lista1.pdf")
    
    if sukces:
        print("\n" + "=" * 60)
        print("  ✅ Gotowe! Otwórz plik: moj_raport.pdf")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ❌ Wystąpił błąd podczas generowania")
        print("=" * 60)

if __name__ == "__main__":
    main()