import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expi
import sympy

def Li(x):
    """Función Logaritmo Integral (aproximación offset)."""
    # li(x) = Ei(ln x). Para x > 1, usamos la parte principal.
    return expi(np.log(x))

def sismografo_aritmetico(limit):
    """
    Simula el sismógrafo aritmético y recupera pi(x) usando la 
    Identidad de Acople Armónico (Teorema 7.3).
    """
    # Constantes del paper (Sección 5 y 7.2)
    Tp = 2.410142  # Constante gaussiana T(p)
    K_mf = 1.5645  # Impedancia K_MF
    
    # Estado inicial
    psi = 1.0  # Energía del sismógrafo
    pi_real = 0
    
    results = {
        'n': [],
        'pi_real': [],
        'pi_sismografo': [],
        'error_dinamico': []
    }
    
    print(f"Simulando Sismógrafo hasta N={limit}...")
    
    for n in range(2, limit + 1):
        # 1. Dinámica del Sismógrafo (Ec. 11)
        es_primo = sympy.isprime(n)
        
        if es_primo:
            psi = psi / Tp  # Descarga Resonante
            pi_real += 1
        else:
            psi = psi + 1   # Carga de Entropía
            
        # 2. Cálculo del Error Dinámico (Ec. 14)
        epsilon_dyn = psi - K_mf * np.log(n)
        
        # 3. Recuperación de pi(n) usando el Teorema 7.3 (Ec. 15 invertida)
        # epsilon_dyn ~ -1/(2pi) * ln(n) * (pi(n) - Li(n))
        # => pi(n) ~ Li(n) - (2*pi * epsilon_dyn) / ln(n)
        
        term_recuperacion = (2 * np.pi * epsilon_dyn) / np.log(n)
        pi_estimado = Li(n) - term_recuperacion
        
        results['n'].append(n)
        results['pi_real'].append(pi_real)
        results['pi_sismografo'].append(pi_estimado)
        results['error_dinamico'].append(epsilon_dyn)

    return results

# Ejecución
N_LIMIT = 10000
data = sismografo_aritmetico(N_LIMIT)

# Gráfica
plt.figure(figsize=(12, 6))

# Comparación pi(x)
plt.subplot(1, 2, 1)
plt.plot(data['n'], data['pi_real'], 'k-', label='$\pi(x)$ Real', linewidth=1.5)
plt.plot(data['n'], data['pi_sismografo'], 'r--', label='$\pi(x)$ Sismógrafo (Knuttzen)', linewidth=1)
plt.plot(data['n'], [Li(x) for x in data['n']], 'g:', label='$Li(x)$ (Riemann)', alpha=0.6)
plt.title('Recuperación de $\pi(x)$ vía Sismógrafo')
plt.xlabel('n')
plt.ylabel('Conteo de Primos')
plt.legend()
plt.grid(True, alpha=0.3)

# Error Dinámico
plt.subplot(1, 2, 2)
plt.plot(data['n'], data['error_dinamico'], color='purple', linewidth=0.8)
plt.title('Error Dinámico $\epsilon_{dyn}(n)$')
plt.xlabel('n')
plt.ylabel('Amplitud')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Verificación numérica final
print(f"Resultados para N={N_LIMIT}:")
print(f"Pi Real:      {data['pi_real'][-1]}")
print(f"Li(N):        {int(Li(N_LIMIT))}")
print(f"Pi Sismógrafo:{int(data['pi_sismografo'][-1])}")
