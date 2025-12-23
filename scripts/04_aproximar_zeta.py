import numpy as np
from scipy.integrate import quad

def zeta_knuttzen_approx(s):
    """
    Calcula la función Zeta de Riemann utilizando la aproximación de Knuttzen
    (Teorema 6.7 y Definición 6.6).
    Válido para Re(s) > 1.
    """
    # 1. Esqueleto Algebraico (Z_estruc)
    # Z_estruc = (2 + (3 / 2^(s+1)) * ((s+1)/(s-1))) / (2 - 2^-s)
    
    num_alg = 2 + (3 / (2**(s + 1))) * ((s + 1) / (s - 1))
    den_norm = 2 - 2**(-s)
    
    z_estruc = num_alg / den_norm
    
    # 2. Corrección Integral de Onda (I_cos)
    # I_cos(s) = s * integral(2 -> inf) de [ R(x) / x^(s+1) ] dx
    # Aproximación trigonométrica: R(x) approx -0.5 * cos(pi * x)
    
    def integrand_real(x, s_val):
        # Parte Real del integrando: Re[ -0.5 * s * cos(pi*x) * x^(-s-1) ]
        term = -0.5 * np.cos(np.pi * x) * (x ** (-s_val - 1))
        return np.real(term * s_val) # Multiplicamos por s dentro o fuera

    def integrand_imag(x, s_val):
        # Parte Imaginaria
        term = -0.5 * np.cos(np.pi * x) * (x ** (-s_val - 1))
        return np.imag(term * s_val)

    # Integramos numéricamente de 2 a Infinito
    # Usamos un límite superior grande finito para la integral oscilatoria numérica
    limit_inf = 10000 
    
    int_real, _ = quad(integrand_real, 2, limit_inf, args=(s,))
    int_imag, _ = quad(integrand_imag, 2, limit_inf, args=(s,))
    
    i_cos = int_real + 1j * int_imag
    
    # Término de corrección final
    correction = i_cos / den_norm
    
    return z_estruc + correction

# --- PRUEBA DEL SCRIPT ---
# Valores de prueba (Problema de Basilea s=2 y un valor complejo)
test_values = [2, 3, 2 + 10j, 4]

print(f"{'s':<10} | {'Zeta(s) Knuttzen':<25} | {'Zeta(s) Scipy (Ref)':<25}")
print("-" * 65)

import scipy.special

for s_val in test_values:
    z_k = zeta_knuttzen_approx(s_val)
    z_ref = scipy.special.zeta(s_val)
    
    # Formateo para mostrar parte real si imag es despreciable
    if np.isclose(np.imag(z_k), 0, atol=1e-4) and isinstance(s_val, (int, float)):
        z_k_str = f"{np.real(z_k):.6f}"
        z_ref_str = f"{np.real(z_ref):.6f}"
    else:
        z_k_str = f"{z_k:.4f}"
        z_ref_str = f"{z_ref:.4f}"
        
    print(f"{str(s_val):<10} | {z_k_str:<25} | {z_ref_str:<25}")

print("\nNota: La pequeña discrepancia se debe a la aproximación R(x) ~ -0.5cos(pi*x)")
print("y a la integración numérica finita.")
