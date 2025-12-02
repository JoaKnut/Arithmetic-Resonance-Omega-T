import numpy as np
import matplotlib.pyplot as plt
import math

def calcular_omega_fast(n):
    # Implementación rápida de d(2n)-4
    if n == 1: return -2
    m = 2 * n
    divs = 0
    for i in range(1, int(math.isqrt(m)) + 1):
        if m % i == 0:
            divs += 1
            if i*i != m: divs += 1
    return divs - 4

def radical(n):
    prod = 1
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            prod *= d
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        prod *= temp
    return prod

def test_abc_tension(limit):
    print(f"Buscando ternas ABC hasta {limit}...")
    resultados = [] # (Radical, Tension)
    
    # Búsqueda simple (se puede optimizar)
    for a in range(1, limit):
        for b in range(a, limit):
            c = a + b
            if c > limit: break
            
            # Condición: coprimos
            if math.gcd(a, b) != 1: continue
            
            # Calcular métricas MFN
            tens_a = calcular_omega_fast(a)
            tens_b = calcular_omega_fast(b)
            tens_c = calcular_omega_fast(c)
            
            tension_total = tens_a + tens_b + tens_c
            rad_abc = radical(a * b * c)
            
            # Log-Log para comparar con la conjetura estándar
            resultados.append((math.log(rad_abc), tension_total))

    return np.array(resultados)

# Uso:
# data = test_abc_tension(2000)
# plt.scatter(data[:,0], data[:,1], alpha=0.5, s=2)
# plt.xlabel("log(rad(abc))")
# plt.ylabel("Tensión Armónica Total Omega_ABC")
# plt.savefig('mfn_abc.png')