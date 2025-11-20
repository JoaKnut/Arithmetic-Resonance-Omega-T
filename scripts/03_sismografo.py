import numpy as np
import matplotlib.pyplot as plt
import math
import argparse

def explicar_contexto():
    print("""
    ===========================================================================
    SCRIPT 3: DINÁMICA DEL SISMÓGRAFO (Psi_E)
    Referencia: Sección 10 del paper.
    ===========================================================================
    
    Simula el proceso de 'Carga' (Compuestos) y 'Descarga' (Primos).
    
    Reglas:
      - Psi(2) = 0
      - Si n es compuesto: Psi(n) = Psi(n-1) + T(n)   [Acumulación de Tensión]
      - Si n es primo:     Psi(n) = Psi(n-1) / Tp     [Relajación / Descarga]
      
    Hipótesis de Knuttzen: Psi(n) ~ (K_MF) * log(n)
    Donde K_MF approx 1.72864 (Dimensión de Equilibrio).
    """)

# Constantes del modelo
TP_CONST = 2.410142264
K_MF = 1.72864
PENDIENTE_TEORICA = K_MF

def omega_fast(n):
    """Requerido para calcular T(n) aproximado."""
    m = 2 * n
    divisors = 0
    limit = int(math.isqrt(m))
    for i in range(1, limit + 1):
        if m % i == 0:
            divisors += 1
            if i*i != m: divisors += 1
    return divisors - 4

def estimar_T(n, max_k=10):
    """
    Estimación rápida de T(n) para la simulación dinámica.
    Usamos pocos términos (k=10) porque el decaimiento es rápido 
    para n grandes (compuestos saturados).
    """
    suma = 0.0
    prod = 1.0
    suma += prod # k=0
    
    for k in range(1, max_k):
        arg = n * (2**(k-1))
        om = omega_fast(arg)
        prod *= (1.0 / (1.0 + om))
        suma += prod
        if prod < 1e-6: break
    return suma

def simular_sismografo(N):
    psi = np.zeros(N + 1)
    # Estado inicial n=2. (Primo, pero definimos inicio en 0)
    psi[2] = 0 
    
    # Criba básica para saber quién es primo rápido
    es_primo = np.ones(N + 1, dtype=bool)
    es_primo[0:2] = False
    for i in range(2, int(math.sqrt(N)) + 1):
        if es_primo[i]:
            es_primo[i*i::i] = False
            
    log_trend = np.zeros(N + 1)
    
    print(f"[INFO] Simulando dinámica hasta n={N}...")
    
    for n in range(3, N + 1):
        prev = psi[n-1]
        
        if es_primo[n]:
            # Regla de Descarga
            curr = prev / TP_CONST
        else:
            # Regla de Carga
            # Calculamos T(n) on-the-fly
            tn = estimar_T(n)
            curr = prev + tn
            
        psi[n] = curr
        log_trend[n] = PENDIENTE_TEORICA * math.log(n, math.e)
        
    return psi, log_trend


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script 3: Sismógrafo Dinámico")
    parser.add_argument("--steps", type=int, default=5000, help="Pasos de simulación")
    args = parser.parse_args()

    explicar_contexto()
    
    psi_vals, trend_vals = simular_sismografo(args.steps)
    
    # Graficar
    x = np.arange(3, args.steps + 1)
    y_psi = psi_vals[3:]
    y_trend = trend_vals[3:]
    
    plt.figure(figsize=(14, 7))
    
    # Gráfica 1: Evolución Absoluta
    plt.subplot(2, 1, 1)
    plt.plot(x, y_psi, label=r"Sismógrafo $\Psi_E(n)$ (Modelo)", color='blue', linewidth=0.8)
    plt.plot(x, y_trend, label=r"Tendencia Teórica $(K_{MF})\log n$", color='red', linestyle='--')
    plt.title(f"Dinámica de Tensión Aritmética (n={args.steps})")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfica 2: El Error (La supuesta equivalencia con Riemann)
    plt.subplot(2, 1, 2)
    error = y_psi - y_trend
    plt.plot(x, error, color='green', linewidth=0.5)
    plt.axhline(0, color='black', linewidth=1)
    plt.title(r"Residuo $\mathcal{E}_{MF}(n) = \Psi_E - C \log n$ (¿Ruido acotado?)")
    plt.ylabel("Desviación")
    plt.xlabel("n")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sismografo_mfn.png')
    print("\n¡Gráfico guardado como 'sismografo_mfn.png' en la misma carpeta!")
