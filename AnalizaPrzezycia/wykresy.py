"""
Moduł do tworzenia wykresów i obsługi LaTeX
Zawiera funkcje generujące różne typy wizualizacji
"""

import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

np.random.seed(422)

def wykres_do_base64(fig):
    """
    Konwertuje wykres matplotlib do formatu base64
    
    Parametry:
    ----------
    fig : matplotlib.figure.Figure
        Obiekt figury matplotlib
        
    Zwraca:
    -------
    str : String z obrazem zakodowanym w base64
    """
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"

def wzor_do_base64(wzor_latex, tytul_wzoru):
    """
    Konwertuje wzór LaTeX do obrazu PNG zakodowanego w base64.
    
    Parametry:
    ----------
    wzor_latex : str
        String z wzorem w formacie LaTeX (np. r'$y = \alpha x + \beta$')
    tytul_wzoru : str
        Krótki opis do wydruku w konsoli
        
    Zwraca:
    -------
    str : String z obrazem zakodowanym w base64 (data:image/png;...)
    """
    print(f"   📐 Wzór: {tytul_wzoru}...")
    fig, ax = plt.subplots(figsize=(8, 1)) # Mały rozmiar, tylko na wzór
    
    # Renderowanie tekstu LaTeX
    # fontsize=18 dla lepszej czytelności w raporcie
    wzor_do_renderowania = r'$' + wzor_latex + r'$'
    
    fig, ax = plt.subplots(figsize=(8, 1)) # Mały rozmiar
    
    # Renderowanie tekstu LaTeX
    # fontsize=18 dla lepszej czytelności w raporcie
    ax.text(0.5, 0.5, wzor_do_renderowania, 
            horizontalalignment='center', 
            verticalalignment='center', 
            fontsize=18, 
            color='black',
            transform=ax.transAxes)
            
    ax.axis('off') # Ukryj osie i ramki
    ax.set_title('')
    plt.tight_layout(pad=0.1) # Minimalne marginesy

    return wykres_do_base64(fig)

def wykres_liniowy():
    
    def dEW(x, alpha, beta, gamma):
        weibull_cdf = 1 - np.exp(-(x / beta)**alpha)
        weibull_pdf = (alpha / beta) * (x / beta)**(alpha - 1) * np.exp(-(x / beta)**alpha)
    
        return gamma * weibull_pdf * weibull_cdf**(gamma - 1)


    def pEW(x, alpha, beta, gamma): 
        return (1 - np.exp(-(x / beta)**alpha))**gamma


    def qEW(p, alpha, beta, gamma):
        return beta * (-np.log(1 - p**(1/gamma)))**(1/alpha)


    def hazard_EW(x, alpha, beta, gamma):
        f = dEW(x, alpha, beta, gamma)
        F = pEW(x, alpha, beta, gamma)
    
        # Unikanie dzielenia przez zero
        survival = 1 - F
        return np.where(survival > 1e-10, f / survival, np.inf)

    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(0, 20, 100)
    y1 = hazard_EW(x, 1.4, 2, 2)
    y2 = hazard_EW(x, 1, 2, 2)
    y3 = hazard_EW(x, 0.8, 1, 2)
    
    ax.plot(x, y1, label='(1.4,2,2)', linewidth=2, color='red')
    ax.plot(x, y2, label='(1,2,2)', linewidth=2, color='blue')
    ax.plot(x, y3, label='(1,1,2)', linewidth=2, color='green')
    
    ax.set_xlabel('X', fontsize=11)
    ax.set_ylabel('Y', fontsize=11)
    ax.set_title('Exponentiated Weibull', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    return wykres_do_base64(fig)


np.random.seed(42)

def qEW(p, alpha, beta, gamma):
    return beta * (-np.log(1 - p**(1/gamma)))**(1/alpha)

def rEW(count, alpha, beta, gamma):
    uniform_samples = np.random.uniform(0, 1, size=count)
    return qEW(uniform_samples, alpha, beta, gamma)

data1 = rEW(50, 2, 4, 3)
data2 = rEW(100, 2, 4, 3)
data3 = rEW(50, 2, 2, 1)
data4 = rEW(100, 2, 2, 1)

def wykres_slupkowy():

    def dEW(x, alpha, beta, gamma):
        weibull_cdf = 1 - np.exp(-(x / beta)**alpha)
        weibull_pdf = (alpha / beta) * (x / beta)**(alpha - 1) * np.exp(-(x / beta)**alpha)
    
        return gamma * weibull_pdf * weibull_cdf**(gamma - 1)


    def pEW(x, alpha, beta, gamma): 
        return (1 - np.exp(-(x / beta)**alpha))**gamma



    # Tworzenie siatki 2x2 wykresów
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Porównanie histogramów i teoretycznej gęstości EW', fontsize=16, fontweight='bold')

    # Funkcja pomocnicza do przeskalowanego histogramu
    def plot_scaled_hist(ax, data, bins, color, label):
        counts, bin_edges = np.histogram(data, bins=bins)
        counts = counts / counts.max()  # normalizacja do [0, 1]
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        width = bin_edges[1] - bin_edges[0]
        ax.bar(bin_centers, counts, width=width, alpha=0.6, color=color, edgecolor='black', label=label)

    ax1 = axes[0, 0]
    plot_scaled_hist(ax1, data1, bins=20, color='skyblue', label='Histogram')
    x1 = np.linspace(0.01, data1.max()*1.1, 200)
    y1 = dEW(x1, 2, 4, 3)
    y1 = y1 / y1.max()  * 0.8
    ax1.plot(x1, y1, 'r-', linewidth=2, label='Gęstość teoretyczna')
    ax1.set_title('Rozkład EW(α=2, β=4, γ=3) — n=50', fontweight='bold')
    ax1.set_xlabel('x')
    ax1.set_ylabel('Przeskalowana gęstość')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = axes[0, 1]
    plot_scaled_hist(ax2, data2, bins=25, color='lightgreen', label='Histogram')
    x2 = np.linspace(0.01, data2.max()*1.1, 200)
    y2 = dEW(x2, 2, 4, 3)
    y2 = y2 / y2.max() * 0.8
    ax2.plot(x2, y2, 'b-', linewidth=2, label='Gęstość teoretyczna')
    ax2.set_title('Rozkład EW(α=2, β=4, γ=3) — n=100', fontweight='bold')
    ax2.set_xlabel('x')
    ax2.set_ylabel('Przeskalowana gęstość')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = axes[1, 0]
    plot_scaled_hist(ax3, data3, bins=20, color='salmon', label='Histogram')
    x3 = np.linspace(0.01, data3.max()*1.1, 200)
    y3 = dEW(x3, 2, 2, 1)
    y3 = y3 / y3.max() * 0.8
    ax3.plot(x3, y3, 'purple', linewidth=2, label='Gęstość teoretyczna')
    ax3.set_title('Rozkład EW(α=2, β=2, γ=1) — n=50', fontweight='bold')
    ax3.set_xlabel('x')
    ax3.set_ylabel('Przeskalowana gęstość')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    ax4 = axes[1, 1]
    plot_scaled_hist(ax4, data4, bins=25, color='gold', label='Histogram')
    x4 = np.linspace(0.01, data4.max()*1.1, 200)
    y4 = dEW(x4, 2, 2, 1)
    y4 = y4 / y4.max() * 0.8
    ax4.plot(x4, y4, 'darkgreen', linewidth=2, label='Gęstość teoretyczna')
    ax4.set_title('Rozkład EW(α=2, β=2, γ=1) — n=100', fontweight='bold')
    ax4.set_xlabel('x')
    ax4.set_ylabel('Przeskalowana gęstość')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    
    return wykres_do_base64(fig)

def wykres_kolowy():
    def qEW(p, alpha, beta, gamma):
        return beta * (-np.log(1 - p**(1/gamma)))**(1/alpha)

    # Statystyki dla próby 1
    mean1 = np.mean(data1)
    median1 = np.median(data1)
    std1 = np.std(data1, ddof=1)
    q1_1 = np.percentile(data1, 25)
    q3_1 = np.percentile(data1, 75)
    iqr1 = q3_1 - q1_1
    min1 = np.min(data1)
    max1 = np.max(data1)
    range1 = max1 - min1
    
    # Statystyki dla próby 2
    mean2 = np.mean(data2)
    median2 = np.median(data2)
    std2 = np.std(data2, ddof=1)
    q1_2 = np.percentile(data2, 25)
    q3_2 = np.percentile(data2, 75)
    iqr2 = q3_2 - q1_2
    min2 = np.min(data2)
    max2 = np.max(data2)
    range2 = max2 - min2
    
    # Statystyki dla próby 3
    mean3 = np.mean(data3)
    median3 = np.median(data3)
    std3 = np.std(data3, ddof=1)
    q1_3 = np.percentile(data3, 25)
    q3_3 = np.percentile(data3, 75)
    iqr3 = q3_3 - q1_3
    min3 = np.min(data3)
    max3 = np.max(data3)
    range3 = max3 - min3
    
    # Statystyki dla próby 4
    mean4 = np.mean(data4)
    median4 = np.median(data4)
    std4 = np.std(data4, ddof=1)
    q1_4 = np.percentile(data4, 25)
    q3_4 = np.percentile(data4, 75)
    iqr4 = q3_4 - q1_4
    min4 = np.min(data4)
    max4 = np.max(data4)
    range4 = max4 - min4
    
    # Wartości teoretyczne dla EW(2,4,3)
    median_theo_243 = qEW(0.5, 2, 4, 3)
    q1_theo_243 = qEW(0.25, 2, 4, 3)
    q3_theo_243 = qEW(0.75, 2, 4, 3)
    iqr_theo_243 = q3_theo_243 - q1_theo_243
    
    # Wartości teoretyczne dla EW(2,2,1)
    median_theo_221 = qEW(0.5, 2, 2, 1)
    q1_theo_221 = qEW(0.25, 2, 2, 1)
    q3_theo_221 = qEW(0.75, 2, 2, 1)
    iqr_theo_221 = q3_theo_221 - q1_theo_221

    return {
        'sample1': {
            'mean': mean1, 'median': median1, 'std': std1,
            'q1': q1_1, 'q3': q3_1, 'iqr': iqr1,
            'min': min1, 'max': max1, 'range': range1
        },
        'sample2': {
            'mean': mean2, 'median': median2, 'std': std2,
            'q1': q1_2, 'q3': q3_2, 'iqr': iqr2,
            'min': min2, 'max': max2, 'range': range2
        },
        'sample3': {
            'mean': mean3, 'median': median3, 'std': std3,
            'q1': q1_3, 'q3': q3_3, 'iqr': iqr3,
            'min': min3, 'max': max3, 'range': range3
        },
        'sample4': {
            'mean': mean4, 'median': median4, 'std': std4,
            'q1': q1_4, 'q3': q3_4, 'iqr': iqr4,
            'min': min4, 'max': max4, 'range': range4
        },
        'theoretical_EW_243': {
            'median': median_theo_243,
            'q1': q1_theo_243,
            'q3': q3_theo_243,
            'iqr': iqr_theo_243
        },
        'theoretical_EW_221': {
            'median': median_theo_221,
            'q1': q1_theo_221,
            'q3': q3_theo_221,
            'iqr': iqr_theo_221
        }
    }




def stworz_wykresy():
    """
    Główna funkcja tworząca wszystkie wykresy
    
    Zwraca:
    -------
    dict : Słownik z wykresami zakodowanymi w base64
    """
    print("   📈 Wykres 1: Funkcje trygonometryczne...")
    wykres1 = wykres_liniowy()
    
    print("   📊 Wykres 2: Sprzedaż miesięczna...")
    wykres2 = wykres_slupkowy()

    dane = wykres_kolowy()
    print(dane.keys())
    


    print("\n✍️ Generowanie wzorów matematycznych:")
    
    # Funkcja gęstości (PDF)
    wzor_pdf_latex = r'f(x) = \gamma \frac{\alpha}{\beta} \left(\frac{x}{\beta}\right)^{\alpha-1} (1-e^{-\left(\frac{x}{\beta}\right)^\alpha})^{\gamma -1}, \quad x \geq \gamma'
    wzor_pdf = wzor_do_base64(wzor_pdf_latex, "Funkcja gęstości (PDF)")
    
    # Dystrybuanta (CDF)
    wzor_cdf_latex = r'F(x) = (1 - e^{-\left(\frac{x}{\beta}\right)^\alpha})^\gamma, \quad x \geq \gamma'
    wzor_cdf = wzor_do_base64(wzor_cdf_latex, "Dystrybuanta (CDF)")
    
    # Funkcja kwantylowa
     
    wzor_kwantyl_latex = r'Q(p) = \beta \left( - \ln(1 - p^{\frac{1}{\gamma}}) \right)^{\frac{1}{\alpha}}, \quad 0 \leq p < 1'
    wzor_kwantyl = wzor_do_base64(wzor_kwantyl_latex, "Funkcja kwantylowa")
    
    # Funkcja hazardu
    wzor_hazard_latex = r'h(x) = \frac{\alpha \cdot \frac{k}{\lambda} \left(\frac{x}{\lambda}\right)^{k - 1} e^{-\left(\frac{x}{\lambda}\right)^k} \left[1 - e^{-\left(\frac{x}{\lambda}\right)^k}\right]^{\alpha - 1}}{1 - \left[1 - e^{-\left(\frac{x}{\lambda}\right)^k}\right]^\alpha}, \quad x \geq 0'
    wzor_hazard = wzor_do_base64(wzor_hazard_latex, "Funkcja hazardu")
    
    
    return {
        'wykres1': wykres1,
        'wykres2': wykres2,
        'WZOR_PDF': wzor_pdf,
        'WZOR_CDF': wzor_cdf,
        'WZOR_KWANTYL': wzor_kwantyl,
        'WZOR_HAZARD': wzor_hazard,
        'dane': dane,
    }


