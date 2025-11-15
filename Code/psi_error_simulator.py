import numpy as np
import matplotlib.pyplot as plt
from math import isqrt
from functools import cache

# =============================================================================
# CONSTANTES DEL MODELO
# =============================================================================

# Constante armónica de los primos (de tu documento, Prop. 8.2)
T_p = 2.410142264177218

# N máximo para esta simulación de prototipo (ej. 10k o 50k)
# Python puro es lento; 10,000 tarda unos segundos.
N_MAX = 100000000

# =============================================================================
# FUNCIONES BÁSICAS DEL MODELO (optimizadas con @cache)
# =============================================================================

@cache
def is_prime(n):
    """Verificador de primalidad simple."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

@cache
def get_divisors_count_d(m):
    """Calcula d(m), la cantidad de divisores de m."""
    if m == 0: return 0
    count = 0
    for i in range(1, isqrt(m) + 1):
        if m % i == 0:
            count += 2 if i * i != m else 1
    return count

@cache
def get_omega(n):
    """Calcula Omega(n) = d(2n) - 4."""
    return get_divisors_count_d(2 * n) - 4

@cache
def get_T(n):
    """Calcula T(n) (Sección 8)."""
    total_T = 1.0  # k=0 (producto vacío)
    term_product = 1.0
    
    # Iteramos para k >= 1. 
    # 20 iteraciones es más que suficiente para la convergencia.
    for k in range(20): 
        n_2j = n * (2**k) # n * 2^j donde j=k
        
        # El denominador es (1 + Omega(n * 2^j))
        denominator = 1 + get_omega(n_2j)
        
        # El término es el producto de k=0 hasta k-1
        # Aquí j va de 0 a k.
        term_product /= denominator
        
        # Si el término es muy pequeño, dejamos de sumar
        if term_product < 1e-15:
            break
        
        total_T += term_product
        
    return total_T

# =============================================================================
# SIMULACIÓN PRINCIPAL
# =============================================================================

print(f"Iniciando simulación del Modelo MK hasta N = {N_MAX}...")

# Arrays para guardar los resultados
n_values = np.arange(3, N_MAX + 1)
psi_e_values = np.zeros(len(n_values))
psi_e = 0.0  # Psi_E(2) = 0

for i, n in enumerate(n_values):
    if is_prime(n):
        psi_e /= T_p
    else:
        psi_e += get_T(n)
    
    psi_e_values[i] = psi_e

print("Simulación completa. Analizando tendencia...")

# =============================================================================
# ANÁLISIS DE REGRESIÓN (para encontrar C)
# =============================================================================

# 1. Creamos el eje log(n)
log_n_values = np.log(n_values)

# 2. Usamos polyfit para encontrar la tendencia lineal C*log(n) + K
#    Ajustamos y = C*x + K, donde x = log(n)
C, K = np.polyfit(log_n_values, psi_e_values, 1)

# 3. Creamos la línea de tendencia
trend_line = C * log_n_values + K

# 4. ¡Calculamos el Error! (Los residuales del ajuste)
error_values = psi_e_values - trend_line

print(f"Análisis completo. Tendencia encontrada: C={C:.4f}")

# =============================================================================
# VISUALIZACIÓN (Versión Corregida)
# =============================================================================

# **CORRECCIÓN 1: Se eliminó plt.style.use()**
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# **CORRECCIÓN 2: Se usó 'r' (raw string) para el título**
fig.suptitle(r"Análisis del Modelo de Resonancia $\Psi_E(n)$", fontsize=16)

# --- Gráfico 1: La Tendencia (lo que SÍ funciona) ---
# **CORRECCIÓN 2: Se usó 'r' y 'rf' para las etiquetas**
ax1.plot(log_n_values, psi_e_values, 'o', markersize=1, alpha=0.5, label=r"$\Psi_E(n)$ (Datos)")
ax1.plot(log_n_values, trend_line, 'r-', linewidth=2, label=rf"Tendencia $C \cdot \log(n) + K$\n(C={C:.4f})")
ax1.set_xlabel(r"$\log(n)$")
ax1.set_ylabel(r"Valor de $\Psi_E(n)$")
ax1.set_title("Verificación de la Tendencia Logarítmica (Prop. 9.2)")
ax1.legend()
# **CORRECCIÓN 1: Se añadió la cuadrícula manualmente**
ax1.grid(True)

# --- Gráfico 2: El Error (lo que querías ver) ---
ax2.plot(n_values, error_values, label="Error de Resonancia", color="purple")
ax2.set_xlabel("Número (n) [escala lineal]")
# **CORRECCIÓN 2: Se usó 'r' para la etiqueta**
ax2.set_ylabel(r"Error $\Psi_E(n) - (C \cdot \log(n) + K)$")
ax2.set_title("Gráfico de Error de Resonancia (Conjetura 9.3)")
ax2.legend()
# **CORRECCIÓN 1: Se añadió la cuadrícula manualmente**
ax2.grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('analisis_resonancia.png')
print("\n¡Gráfico guardado como 'analisis_resonancia.png' en la misma carpeta!")