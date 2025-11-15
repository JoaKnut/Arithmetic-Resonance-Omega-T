import math
from omega_d2n_core import omega # Importa la función base

def T(n, max_iter=50):
    """
    Calcula la función de Resonancia de Fondo T(n) usando la serie.
    T(n) = sum_{k=0}^{inf} prod_{j=0}^{k-1} [ 1 / (1 + Omega(n * 2^j)) ]
    
    max_iter: Límite de términos para asegurar que la serie converge.
    """
    
    total_sum = 0.0
    # k=0 (Término inicial)
    # El producto (prod) de j=0 a -1 es 1 (producto vacío)
    total_sum += 1.0 
    
    current_product = 1.0
    
    for k in range(1, max_iter + 1):
        # j = k-1 (el último término del producto)
        j = k - 1
        
        # Calcula Omega(n * 2^j)
        omega_val = omega(n * (2**j))
        
        # Evita división por cero si Omega(n*2^j) fuera -1 (teóricamente no debería pasar)
        denominator = 1.0 + omega_val
        if denominator == 0:
            break
            
        current_product *= (1.0 / denominator)
        
        # Si el término es muy pequeño, detenemos la suma
        if current_product < 1e-100:
            break
            
        total_sum += current_product
        
    return total_sum

def T_p_analytic(x=1.0/math.sqrt(2)):
    """
    Calcula el valor T(p) analíticamente usando la fórmula de erf(x).
    T(p) = 1 + sqrt(pi/2) * e^(1/2) * erf(1/sqrt(2))
    """
    e_half = math.exp(0.5)
    sqrt_pi_2 = math.sqrt(math.pi / 2.0)
    erf_val = math.erf(x)
    
    return 1.0 + sqrt_pi_2 * e_half * erf_val

def calculate_C_Perf():
    """
    Calcula la Constante de Amortiguamiento Perfecto (C_Perf).
    C_Perf = sum_{k=0}^{inf} [ 1 / (2*p_k - 1) ]
    Donde p_k son los exponentes de los primos de Mersenne.
    """
    
    # Exponentes de los primos de Mersenne conocidos (M51)
    mersenne_exponents = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 
        2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 
        23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 
        1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 
        24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 
        43112609, 57885161, 74207281, 77232917, 82589933
    ]
    
    c_perf_sum = 0.0
    for p in mersenne_exponents:
        # A_k = 1 / (1 + Omega(N_k)) = 1 / (1 + 2(p-1)) = 1 / (2p - 1)
        term = 1.0 / (2.0 * p - 1.0)
        c_perf_sum += term
        
    return c_perf_sum

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("--- Verificación de T_n_and_constants.py ---")
    
    # 1. Caso T(4) (Debe ser e ≈ 2.71828)
    # Omega(4*2^j) = Omega(2^(j+2)) = (j+2)-2 = j
    # T(4) = sum(1/k!)
    print(f"Calculando T(4) [Serie]: {T(4, max_iter=20)}")
    print(f"Valor real de e:       {math.e}")
    
    print("-" * 20)

    # 2. Caso T(p) (Debe ser T_p ≈ 2.41014)
    # Omega(p*2^0) = Omega(p) = 0
    # Omega(p*2^j) = 2j (para j >= 1)
    print(f"Calculando T(3) [Serie]: {T(3, max_iter=50)}")
    print(f"Calculando T(5) [Serie]: {T(5, max_iter=50)}")
    print(f"Valor analítico T_p:   {T_p_analytic()}")
    
    print("-" * 20)
    
    # 3. Caso C_Perf (Debe ser ≈ 0.86386)
    print(f"Calculando C_Perf (Suma de 51 términos): {calculate_C_Perf()}")
