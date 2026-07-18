


from weasyprint import HTML, CSS
from datetime import datetime
import os
from report4_part1 import przeslij_dane1
from report4_part2 import przeslij_dane2
from report4_part3 import przeslij_dane3
from report4_part4 import przeslij_dane4


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
    """Konwertuje DataFrame na HTML table z poprawnym wyrównaniem kolumn"""
    # Zwiększamy zakres do :4, aby złapać COEF, EXP(COEF) i SE(COEF)
    # Oryginalny df zazwyczaj ma 'Zmienna' jako indeks, a nie kolumnę
    subset = df.iloc[:, :3] 
    
    html = '<table>\n<thead>\n<tr>\n'
    html += '  <th>ZMIENNA</th>'  # Nagłówek dla indeksu
    for col in subset.columns:
        html += f'<th>{col}</th>'
    html += '\n</tr>\n</thead>\n<tbody>\n'
    
    for idx, row in subset.iterrows():
        html += '<tr>\n'
        
        # Wyciąganie nazwy zmiennej z indeksu (obsługa krotek i zwykłych stringów)
        var_name = idx[-1] if isinstance(idx, tuple) else idx
        html += f'  <td><strong>{var_name}</strong></td>'
        
        # Wypisywanie wartości z rzędu
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
    template = wczytaj_plik("szablon4.html")
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
    fig5_po = d3['fig5'] if d3['fig5'].startswith('data:') else f"data:image/png;base64,{d3['fig5']}"
    html = html.replace("{{WYKRES_PO_SURV}}", fig3_po)
    html = html.replace("{{WYKRE5_PO_SURV}}", fig5_po)
    html = html.replace("{{PROB_PO_PH1_300}}", format_value(d3['prob_survival1'], 4))
    html = html.replace("{{PROB_PO_PH1_300_PCT}}", format_percent(d3['prob_survival1']))
    html = html.replace("{{PROB_PO_PH2_300}}", format_value(d3['prob_survival2'], 4))
    html = html.replace("{{PROB_PO_PH2_300_PCT}}", format_percent(d3['prob_survival2']))
        # ---------------------------
    # LISTA 12 - Testy (d4)
    # ---------------------------
    
    print("   Przetwarzanie danych Lista 12...")
    
    # Model AFT - testy age
    html = html.replace("{{AFT_AGE_WALD}}", format_value(d4['zadanie_1']['1a']['wald_pvalue'], 6))
    html = html.replace("{{AFT_AGE_LRT}}", format_value(d4['zadanie_1']['1a']['lrt_pvalue'], 6))
    html = html.replace("{{AFT_AGE_WALD_STAT}}", format_value(d4['zadanie_1']['1a']['wald_statistic'], 6))
    html = html.replace("{{AFT_AGE_LRT_STAT}}", format_value(d4['zadanie_1']['1a']['lrt_statistic'], 6))
    html = html.replace("{{AFT_AGE_WNIOSKI}}", 
                       "Zmienna age JEST istotna (p < 0.05)" if d4['zadanie_1']['1a']['wald_pvalue'] < 0.05 else "Zmienna age NIE jest istotna (p >= 0.05)")
    
    # Model AFT - testy trt
    html = html.replace("{{AFT_TRT_WALD}}", format_value(d4['zadanie_1']['1b']['wald_pvalue'], 6))
    html = html.replace("{{AFT_TRT_LRT}}", format_value(d4['zadanie_1']['1b']['lrt_pvalue'], 6))
    html = html.replace("{{AFT_TRT_WALD_STAT}}", format_value(d4['zadanie_1']['1b']['wald_statistic'], 6))
    html = html.replace("{{AFT_TRT_LRT_STAT}}", format_value(d4['zadanie_1']['1b']['lrt_statistic'], 6))
    html = html.replace("{{AFT_TRT_WNIOSKI}}", 
                       "Zmienna trt JEST istotna (p < 0.05)" if d4['zadanie_1']['1b']['wald_pvalue'] < 0.05 else "Zmienna trt NIE jest istotna (p >= 0.05)")
    
    # Model AFT - testy stage
    html = html.replace("{{AFT_STAGE_LRT}}", format_value(d4['zadanie_1']['1c']['lrt_pvalue'], 6))
    html = html.replace("{{AFT_STAGE_LRT_STAT}}", format_value(d4['zadanie_1']['1c']['lrt_statistic'], 6))
    html = html.replace("{{AFT_STAGE_DF}}", format_value(d4['zadanie_1']['1c']['df'], 0))
    html = html.replace("{{AFT_STAGE_WNIOSKI}}", 
                       "Zmienna stage JEST istotna (p < 0.05)" if d4['zadanie_1']['1c']['lrt_pvalue'] < 0.05 else "Zmienna stage NIE jest istotna (p >= 0.05)")
    
    # Model Cox - testy age
    html = html.replace("{{COX_AGE_WALD}}", format_value(d4['zadanie_2']['2a']['wald_pvalue'], 6))
    html = html.replace("{{COX_AGE_LRT}}", format_value(d4['zadanie_2']['2a']['lrt_pvalue'], 6))
    html = html.replace("{{COX_AGE_WALD_STAT}}", format_value(d4['zadanie_2']['2a']['wald_statistic'], 6))
    html = html.replace("{{COX_AGE_LRT_STAT}}", format_value(d4['zadanie_2']['2a']['lrt_statistic'], 6))
    html = html.replace("{{COX_AGE_WNIOSKI}}", 
                       "Zmienna age JEST istotna (p < 0.05)" if d4['zadanie_2']['2a']['wald_pvalue'] < 0.05 else "Zmienna age NIE jest istotna (p >= 0.05)")
    
    # Model Cox - testy trt
    html = html.replace("{{COX_TRT_WALD}}", format_value(d4['zadanie_2']['2b']['wald_pvalue'], 6))
    html = html.replace("{{COX_TRT_LRT}}", format_value(d4['zadanie_2']['2b']['lrt_pvalue'], 6))
    html = html.replace("{{COX_TRT_WALD_STAT}}", format_value(d4['zadanie_2']['2b']['wald_statistic'], 6))
    html = html.replace("{{COX_TRT_LRT_STAT}}", format_value(d4['zadanie_2']['2b']['lrt_statistic'], 6))
    html = html.replace("{{COX_TRT_WNIOSKI}}", 
                       "Zmienna trt JEST istotna (p < 0.05)" if d4['zadanie_2']['2b']['wald_pvalue'] < 0.05 else "Zmienna trt NIE jest istotna (p >= 0.05)")
    
    # Model Cox - testy stage
    html = html.replace("{{COX_STAGE_LRT}}", format_value(d4['zadanie_2']['2c']['lrt_pvalue'], 6))
    html = html.replace("{{COX_STAGE_LRT_STAT}}", format_value(d4['zadanie_2']['2c']['lrt_statistic'], 6))
    html = html.replace("{{COX_STAGE_DF}}", format_value(d4['zadanie_2']['2c']['df'], 0))
    html = html.replace("{{COX_STAGE_WNIOSKI}}", 
                       "Zmienna stage JEST istotna (p < 0.05)" if d4['zadanie_2']['2c']['lrt_pvalue'] < 0.05 else "Zmienna stage NIE jest istotna (p >= 0.05)")
    
    # Zadanie 3a - Backward elimination AFT
    html = html.replace("{{AFT_BACKWARD_VARS}}", ", ".join(d4['zadanie_3']['3a']['final_variables']))
    html = html.replace("{{AFT_BACKWARD_LOGLIK}}", format_value(d4['zadanie_3']['3a']['log_likelihood'], 6))
    
    # Zadanie 3b - AIC AFT
    html = html.replace("{{AFT_AIC_VARS}}", ", ".join(d4['zadanie_3']['3b']['best_variables']))
    html = html.replace("{{AFT_AIC_VALUE}}", format_value(d4['zadanie_3']['3b']['best_aic'], 6))
    html = html.replace("{{AFT_AIC_LOGLIK}}", format_value(d4['zadanie_3']['3b']['log_likelihood'], 6))
    
    # Zadanie 3c - BIC AFT
    html = html.replace("{{AFT_BIC_VARS}}", ", ".join(d4['zadanie_3']['3c']['best_variables']))
    html = html.replace("{{AFT_BIC_VALUE}}", format_value(d4['zadanie_3']['3c']['best_bic'], 6))
    html = html.replace("{{AFT_BIC_LOGLIK}}", format_value(d4['zadanie_3']['3c']['log_likelihood'], 6))
    
    # Zadanie 4a - Backward elimination Cox
    html = html.replace("{{COX_BACKWARD_VARS}}", ", ".join(d4['zadanie_4']['4a']['final_variables']))
    html = html.replace("{{COX_BACKWARD_LOGLIK}}", format_value(d4['zadanie_4']['4a']['log_likelihood'], 6))
    
    # Zadanie 4b - AIC Cox
    html = html.replace("{{COX_AIC_VARS}}", ", ".join(d4['zadanie_4']['4b']['best_variables']))
    html = html.replace("{{COX_AIC_VALUE}}", format_value(d4['zadanie_4']['4b']['best_aic'], 6))
    html = html.replace("{{COX_AIC_LOGLIK}}", format_value(d4['zadanie_4']['4b']['log_likelihood'], 6))
    
    # Zadanie 4c - BIC Cox
    html = html.replace("{{COX_BIC_VARS}}", ", ".join(d4['zadanie_4']['4c']['best_variables']))
    html = html.replace("{{COX_BIC_VALUE}}", format_value(d4['zadanie_4']['4c']['best_bic'], 6))
    html = html.replace("{{COX_BIC_LOGLIK}}", format_value(d4['zadanie_4']['4c']['log_likelihood'], 6))
    
    return html
  


def sprawdz_pliki():
    """Sprawdza czy wszystkie wymagane pliki istnieją"""
    wymagane_pliki = [
        'szablon4.html', '../wspolne/style.css',
        'report4_part1.py', 'report4_part2.py', 'report4_part3.py', 'report4_part4.py'
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


def generuj_pdf(nazwa_pliku="raport_lista4.pdf"):
    nazwa_pliku="raport_lista4.pdf"
    """Główna funkcja generująca PDF"""
    print("=" * 60)
    print("  GENERATOR PDF - Raport Lista 4 (Listy 9-12)")
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
    sukces = generuj_pdf("Raport_Lista4.pdf")
    
    if sukces:
        print("\n" + "=" * 60)
        print("  ✅ Gotowe! Otwórz plik: Raport_Lista4.pdf")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  ❌ Wystąpił błąd podczas generowania")
        print("=" * 60)


if __name__ == "__main__":
    main()