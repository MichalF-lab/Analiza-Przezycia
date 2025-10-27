"""
Generator PDF - Główny plik
Generuje profesjonalne raporty PDF z wykresami i kodem
"""

from weasyprint import HTML, CSS
from datetime import datetime
import os
from wykresy import przeslij_dane1
from raporcik2 import przeslij_dane2
import matplotlib.pyplot as plt




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
    

def stworz_html(dane1, dane2):
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
    html = html.replace('{{D3MED}}', f'{dane2["dane3"]["median_time"]:.4f}')

    # Porównanie leków A i B
    html = html.replace('{{DAN}}', str(dane2["daneA"]['n']))
    html = html.replace('{{DANC}}', str(dane2["daneA"]['n_complete']))
    html = html.replace('{{DAM}}', f'{dane2["daneA"]["min_time"]:.4f}')
    html = html.replace('{{DAMED}}', f'{dane2["daneA"]["median"]:.4f}')

    html = html.replace('{{DBN}}', str(dane2["daneB"]['n']))
    html = html.replace('{{DBNC}}', str(dane2["daneB"]['n_complete']))
    html = html.replace('{{DBM}}', f'{dane2["daneB"]["min_time"]:.4f}')
    html = html.replace('{{DBMED}}', f'{dane2["daneB"]["median"]:.4f}')
    
    return html

def sprawdz_pliki():
    """"Sprawdza czy wszystkie wymagane pliki istnieją"""
    wymagane_pliki = ['szablon.html', 'style.css', 'wykresy.py', 'raporcik2.py']
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

    print("📄 Ładowanie szablonu HTML...")
    html_content = stworz_html(dane1, dane2)
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
    sukces = generuj_pdf("moj_raport.pdf")
    
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