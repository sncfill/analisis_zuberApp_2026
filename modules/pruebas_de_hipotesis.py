import pandas as pd
from scipy import stats
import decpandas as dp

def prueba_estadistica(normal: bool, x: pd.Series, y: pd.Series, h0: str, h1: str):
    """
        Realiza una prueba estadística de hipótesis
        Args:
            normal (bool): Indica si los datos siguen una distribución normal
            x (pd.Series): Serie con los datos de la primera muestra
            y (pd.Series): Serie con los datos de la segunda muestra
            h0 (str): hipótesis nula
            h1 (str): hipótesis alternativa
    """
    if(normal):
        stat, p = stats.ttest_ind(x, y)
        print(f"\nUtilizando prueba paramétrica t-test:\n")
        prueba_de_hipotesis(p, 0.05, h0, h1)
    else:
        stat, p = stats.mannwhitneyu(x, y)
        print(f"\nUtilizando prueba no paramétrica Mann-Whitney U:\n")
        prueba_de_hipotesis(p, 0.05, h0, h1)

def prueba_de_hipotesis(pv: float, alpha: float, h0: str, h1: str):
    """
        Prueba de hipótesis basada en el valor p
        Args:
            pv (float): valor p obtenido de la prueba estadística
            alpha (float): nivel de significancia
            h0 (str): hipótesis nula
            h1 (str): hipótesis alternativa
        Returns:
            bool: True Si pv es mayor a alpha (no se rechaza la hipótesis nula), False si pv es menor a alpha (se rechaza la hipótesis nula)
    """
    
    print(f"El valor p es de: {pv}:")
    if(pv > alpha):
        print(f"  * El valor p es mayor al de valor alfa ({alpha}). No se rechaza la hipótesis nula (H₀).", "\n  *", h0)
        return True
    else:
        print(f"  * El valor p es menor al de valor alfa ({alpha}). Rechazamos la hipótesis nula (H₀).", "\n  *", h1)
        return False

def correlacion_entre(x: pd.Series, y: pd.Series) -> float:
    """Calcula el coeficiente de correlación de Pearson entre dos series"""
    r = x.corr(y)
    if r < 0.1:
        fuerza = "Muy débil o inexistente"
    elif r <= 0.3:
        fuerza = "Baja o débil"
    elif r <= 0.5:
        fuerza = "Moderada o mediana"
    elif r <= 1.0:
        fuerza = "Fuerte o alta"
    else:
        fuerza = "Perfecta"
    print(f"El coeficiente de correlación de Pearson (r) entre '{dp.astitlestr(x.name)}' y '{dp.astitlestr(y.name)}' es de {r}, lo que indica una correlación de fuerza: {fuerza}.")
    return r

def prueba_de_normalidad(data: pd.Series, alpha: float = 0.05, label: str = ""):
    if(label == ""):
        label = data.name
    h0 = "Los datos siguen una distribución normal."
    h1 = "Los datos NO siguen una distribución normal."
    tm = len(data)
    l = 5000
    if(tm > l):
        """Realiza la prueba de normalidad de D'Agostino-Pearson"""
        stat, p = stats.normaltest(data)
        print(f"\nEl tamaño de la muestra [{label}] es de {tm} (mayor a {l}), por lo que se utiliza la prueba de D'Agostino-Pearson.")
        return prueba_de_hipotesis(p, alpha, h0, h1)
    else:
        """Realiza la prueba de normalidad de Shapiro-Wilk"""
        stat, p = stats.shapiro(data)        
        print(f"\nEl tamaño de la muestra es de {tm} (menor a {l}), por lo que se utiliza la prueba de Shapiro-Wilk.")
        return prueba_de_hipotesis(p, alpha, h0, h1)