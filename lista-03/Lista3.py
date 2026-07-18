"""
Generator PDF - Główny plik Lista 3 (Listy 9-12)
Generuje profesjonalne raporty PDF z wykresami i kodem
"""

from weasyprint import HTML, CSS
from datetime import datetime
import os
from report3_part1 import przeslij_dane1
from report3_part2 import przeslij_dane2
from report3_part3 import przeslij_dane3
from report3_part4 import przeslij_dane4


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


def format_value(val, decimals=4):
    """Formatuje wartość liczbową"""
    if isinstance(val, (int, float)):
        return f"{val:.{decimals}f}"
    return str(val)


def format_percent(val):
    """Formatuje wartość jako procent"""
    if isinstance(val, (int, float)):
        return f"{val*100:.2f}%"
    return str(val)


def format_dataframe_html(df):
    """Konwertuje DataFrame na HTML table"""
    html = '<table>\n<thead>\n<tr>\n<th>Zmienna</th>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '\n</tr>\n</thead>\n<tbody>\n'
    
    for idx, row in df.iterrows():
        html += '<tr>\n'
        # Obsługa multi-index
        if isinstance(idx, tuple):
            html += f'<td><strong>{idx[-1]}</strong></td>'
        else:
            html += f'<td><strong>{idx}</strong></td>'
        
        for val in row:
            if isinstance(val, (int, float)):
                html += f'<td>{val:.6f}</td>'
            else:
                html += f'<td>{val}</td>'
        html += '\n</tr>\n'
    
    html += '</tbody>\n</table>'
    return html


def format_series_html(series):
    """Konwertuje Series na HTML table"""
    html = '<table>\n<thead>\n<tr>\n<th>Zmienna</th><th>Wartość</th>\n</tr>\n</thead>\n<tbody>\n'
    
    for idx, val in series.items():
        html += '<tr>\n'
        html += f'<td><strong>{idx}</strong></td>'
        if isinstance(val, (int, float)):
            html += f'<td>{val:.6f}</td>'
        else:
            html += f'<td>{val}</td>'
        html += '\n</tr>\n'
    
    html += '</tbody>\n</table>'
    return html


def stworz_html(d1, d2, d3, d4):
    """Tworzy HTML podstawiając dane do szablonu"""
    template = wczytaj_plik("szablon3.html")
    if not template:
        return None

    html = template

    # DATA
    html = html.replace("{{DATA}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # ---------------------------
    # LISTA 9 - WeibullAFT (d1)
    # ---------------------------
    
    print("   Przetwarzanie danych Lista 9...")
    
    # Tabela podsumowania modelu AFT
    html = html.replace("{{TABELA_AFT_SUMMARY}}", format_dataframe_html(d1['fit_aft']))
    
    # Wykres funkcji przeżycia (zadanie 3-4) - POPRAWKA: dodaj "data:image/png;base64,"
    fig1_data = d1['fig1'] if d1['fig1'].startswith('data:') else f"data:image/png;base64,{d1['fig1']}"
    html = html.replace("{{WYKRES_AFT_SURV}}", fig1_data)
    html = html.replace("{{PROB_AFT_300}}", format_value(d1['prob_survival'], 4))
    html = html.replace("{{PROB_AFT_300_PCT}}", format_percent(d1['prob_survival']))
    
    # Wykresy hazardu (zadanie 7)
    fig2_data = d1['fig2'] if d1['fig2'].startswith('data:') else f"data:image/png;base64,{d1['fig2']}"
    fig3_data = d1['fig3'] if d1['fig3'].startswith('data:') else f"data:image/png;base64,{d1['fig3']}"
    html = html.replace("{{WYKRES_AFT_HAZARD}}", fig2_data)
    html = html.replace("{{WYKRES_AFT_LNHAZARD}}", fig3_data)
    
    # Wykresy przeżycia dla obu profili (zadanie 8-9)
    fig4_data = d1['fig4'] if d1['fig4'].startswith('data:') else f"data:image/png;base64,{d1['fig4']}"
    fig5_data = d1['fig5'] if d1['fig5'].startswith('data:') else f"data:image/png;base64,{d1['fig5']}"
    html = html.replace("{{WYKRES_AFT_SURV_POROWNANIE}}", fig4_data)
    html = html.replace("{{WYKRES_AFT_SURV_POROWNANIE5}}", fig5_data)
    html = html.replace("{{PROB_AFT_PH1_300}}", format_value(d1['prob_survival1'], 4))
    html = html.replace("{{PROB_AFT_PH1_300_PCT}}", format_percent(d1['prob_survival1']))
    html = html.replace("{{PROB_AFT_PH2_300}}", format_value(d1['prob_survival2'], 4))
    html = html.replace("{{PROB_AFT_PH2_300_PCT}}", format_percent(d1['prob_survival2']))

    # ---------------------------
    # LISTA 10 - CoxPH (d2)
    # ---------------------------
    
    print("   Przetwarzanie danych Lista 10...")
    
    # Tabela podsumowania modelu Cox
    html = html.replace("{{TABELA_COX_SUMMARY}}", format_dataframe_html(d2['cph_summary']))
    html = html.replace("{{TABELA_COX_PARAMS}}", format_series_html(d2['cph_params']))
    
    # Baseline funkcje
    html = html.replace("{{TABELA_BASELINE_CUMHAZ}}", d2['fig11'])
    html = html.replace("{{TABELA_BASELINE_SURV}}", d2['fig12'])
    
    # Wykresy skumulowanego hazardu (zadanie 4)
    fig1_cox = d2['fig1'] if d2['fig1'].startswith('data:') else f"data:image/png;base64,{d2['fig1']}"
    fig2_cox = d2['fig2'] if d2['fig2'].startswith('data:') else f"data:image/png;base64,{d2['fig2']}"
    html = html.replace("{{WYKRES_COX_CUMHAZARD}}", fig1_cox)
    html = html.replace("{{WYKRES_COX_LNCUMHAZARD}}", fig2_cox)
    
    # Wykresy przeżycia (zadanie 5-6)
    fig3_cox = d2['fig3'] if d2['fig3'].startswith('data:') else f"data:image/png;base64,{d2['fig3']}"
    fig5_cox = d2['fig5'] if d2['fig5'].startswith('data:') else f"data:image/png;base64,{d2['fig5']}"
    html = html.replace("{{WYKRES_COX_SURV}}", fig3_cox)
    html = html.replace("{{WYKRES_COX_SUR}}", fig5_cox)
    html = html.replace("{{PROB_COX_PH1_300}}", format_value(d2['prob_survival1'], 4))
    html = html.replace("{{PROB_COX_PH1_300_PCT}}", format_percent(d2['prob_survival1']))
    html = html.replace("{{PROB_COX_PH2_300}}", format_value(d2['prob_survival2'], 4))
    html = html.replace("{{PROB_COX_PH2_300_PCT}}", format_percent(d2['prob_survival2']))
    # ---------------------------
    # LISTA 11 - OrderedModel (d3)
    # ---------------------------

    print("   Przetwarzanie danych Lista 11...")

    # Tabela podsumowania modelu OM - jako string/HTML
    html = html.replace("{{TABELA_PO_SUMMARY}}", f"<pre>{d3['ordered_model_summary']}</pre>")
    html = html.replace("{{TABELA_PO_PARAMS}}", format_series_html(d3['ordered_model_params']))

    # Baseline funkcje
    html = html.replace("{{TABELA_PO_BASELINE_CUMHAZ}}", d3['fig11'])
    html = html.replace("{{TABELA_PO_BASELINE_SURV}}", d3['fig12'])

    # Wykresy skumulowanego hazardu (zadanie 4)
    fig1_po = d3['fig1'] if d3['fig1'].startswith('data:') else f"data:image/png;base64,{d3['fig1']}"
    fig2_po = d3['fig2'] if d3['fig2'].startswith('data:') else f"data:image/png;base64,{d3['fig2']}"
    html = html.replace("{{WYKRES_PO_CUMHAZARD}}", fig1_po)
    html = html.replace("{{WYKRES_PO_LNCUMHAZARD}}", fig2_po)

    # Wykresy przeżycia (zadanie 5-6)
    fig3_po = d3['fig3'] if d3['fig3'].startswith('data:') else f"data:image/png;base64,{d3['fig3']}"
    html = html.replace("{{WYKRES_PO_SURV}}", fig3_po)
    html = html.replace("{{PROB_PO_PH1_300}}", format_value(d3['prob_survival1'], 4))
    html = html.replace("{{PROB_PO_PH1_300_PCT}}", format_percent(d3['prob_survival1']))
    html = html.replace("{{PROB_PO_PH2_300}}", format_value(d3['prob_survival2'], 4))
    html = html.replace("{{PROB_PO_PH2_300_PCT}}", format_percent(d3['prob_survival2']))
        # ---------------------------
    # LISTA 12 - Testy (d4)
    # ---------------------------
    
    print("   Przetwarzanie danych Lista 12...")
    
    # Model AFT - testy
    html = html.replace("{{AFT_AGE_WALD}}", format_value(d4['1A'], 6))
    html = html.replace("{{AFT_AGE_LRT}}", format_value(d4['1A1'], 6))
    html = html.replace("{{AFT_AGE_WNIOSKI}}", 
                       "Zmienna age JEST istotna (p < 0.05)" if d4['1A'] < 0.05 else "Zmienna age NIE jest istotna (p ≥ 0.05)")
    
    html = html.replace("{{AFT_SEX_WALD}}", format_value(d4['1B'], 6))
    html = html.replace("{{AFT_SEX_LRT}}", format_value(d4['1B1'], 6))
    html = html.replace("{{AFT_SEX_WNIOSKI}}", 
                       "Zmienna sex JEST istotna (p < 0.05)" if d4['1B'] < 0.05 else "Zmienna sex NIE jest istotna (p ≥ 0.05)")
    
    html = html.replace("{{AFT_ECOG_LRT}}", format_value(d4['1C'], 6))
    html = html.replace("{{AFT_ECOG_WNIOSKI}}", 
                       "Zmienna ph.ecog JEST istotna (p < 0.05)" if d4['1C'] < 0.05 else "Zmienna ph.ecog NIE jest istotna (p ≥ 0.05)")
    
    # Model Cox - testy
    html = html.replace("{{COX_AGE_WALD}}", format_value(d4['2A'], 6))
    html = html.replace("{{COX_AGE_LRT}}", format_value(d4['2A1'], 6))
    html = html.replace("{{COX_AGE_WNIOSKI}}", 
                       "Zmienna age JEST istotna (p < 0.05)" if d4['2A'] < 0.05 else "Zmienna age NIE jest istotna (p ≥ 0.05)")
    
    html = html.replace("{{COX_SEX_WALD}}", format_value(d4['2B'], 6))
    html = html.replace("{{COX_SEX_LRT}}", format_value(d4['2B1'], 6))
    html = html.replace("{{COX_SEX_WNIOSKI}}", 
                       "Zmienna sex JEST istotna (p < 0.05)" if d4['2B'] < 0.05 else "Zmienna sex NIE jest istotna (p ≥ 0.05)")
    
    html = html.replace("{{COX_ECOG_LRT}}", format_value(d4['2C'], 6))
    html = html.replace("{{COX_ECOG_WNIOSKI}}", 
                       "Zmienna ph.ecog JEST istotna (p < 0.05)" if d4['2C'] < 0.05 else "Zmienna ph.ecog NIE jest istotna (p ≥ 0.05)")

    return html


def sprawdz_pliki():
    """Sprawdza czy wszystkie wymagane pliki istnieją"""
    wymagane_pliki = [
        'szablon3.html', '../wspolne/style.css',
        'report3_part1.py', 'report3_part2.py', 'report3_part3.py', 'report3_part4.py'
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


def generuj_pdf(nazwa_pliku="raport_lista3.pdf"):
    """Główna funkcja generująca PDF"""
    print("=" * 60)
    print("  GENERATOR PDF - Raport Lista 3 (Listy 9-12)")
    print("=" * 60)
    
    # Sprawdź pliki
    if not sprawdz_pliki():
        print("\n💡 Upewnij się, że wszystkie pliki są w tym samym katalogu!")
        return False
    
    print("\n🔧 Generowanie danych z wszystkich części...")
    try:
        print("   📊 Część 1: Model Weibull AFT (Lista 9)...")
        dane1 = przeslij_dane1()
        
        print("   📊 Część 2: Model Cox PH (Lista 10)...")
        dane2 = przeslij_dane2()
        
        print("   📊 Część 3: Model Proportional Odds (Lista 11)...")
        dane3 = przeslij_dane3()
        
        print("   📊 Część 4: Testy statystyczne (Lista 12)...")
        dane4 = przeslij_dane4()
        
    except Exception as e:
        print(f"❌ Błąd generowania danych: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("📄 Ładowanie szablonu HTML...")
    html_content = stworz_html(dane1, dane2, dane3, dane4)
    if not html_content:
        return False
    
    print("🎨 Ładowanie stylów CSS...")
    css_content = wczytaj_plik('../wspolne/style.css')
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
    sukces = generuj_pdf("Raport_Lista3.pdf")
    
    if sukces:
        print("\n" + "=" * 60)
        print("  ✅ Gotowe! Otwórz plik: Raport_Lista3.pdf")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ❌ Wystąpił błąd podczas generowania")
        print("=" * 60)


if __name__ == "__main__":
    main()