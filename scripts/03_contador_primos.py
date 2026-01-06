import numpy as np
import argparse
import time
from mpmath import mp

# Configuración de precisión para cálculos trascendentes
mp.dps = 50

def generar_semilla_rapida(N):
    """
    [EXACTO] Genera la señal base de paridad alpha(n).
    A(n) = 2 (impar/base), 1 (par).
    """
    A = np.ones(N + 1, dtype=np.float64)
    A[1] = 2.0
    A[3::2] = 2.0 
    return A

def inversion_espectral_rapida(A, N):
    """
    [EXACTO] Decodifica Lambda(n) usando convolución recursiva.
    Resuelve: (Lambda * alpha)(n) = alpha(n) ln n
    Complejidad: O(N log N)
    """
    indices = np.arange(N + 1, dtype=np.float64)
    indices[0] = 1.0 
    ln_n = np.log(indices)
    ln_n[0] = 0.0
    
    B = A * (-ln_n)
    C = np.zeros(N + 1, dtype=np.float64)
    inv_A1 = 1.0 / A[1] 
    
    print(f"[INFO] Ejecutando Sismógrafo de Paridad (Convolución) para N={N}...")
    start_time = time.time()
    
    for i in range(1, N + 1):
        val = (B[i] + C[i]) * inv_A1
        C[i] = val
        
        # Propagación de la señal a múltiplos (Criba aditiva)
        if abs(val) < 1e-9: continue
        
        if 2 * i <= N:
            k_limit = N // i
            multiples = np.arange(2 * i, (k_limit + 1) * i, i)
            factors_A = A[2 : k_limit + 1]
            C[multiples] -= val * factors_A
            
    print(f"[INFO] Espectro decodificado en {time.time() - start_time:.2f}s")
    return -C 

def mobius(n):
    """Calcula mu(n) para limpieza de armónicos."""
    if n == 1: return 1
    p = 2
    count = 0
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            temp //= p
            count += 1
            if temp % p == 0: return 0 # Cuadrado perfecto
        p += 1
    if temp > 1: count += 1
    return -1 if count % 2 == 1 else 1

def correccion_armonicos_exacta(J_counts, N):
    """
    [EXACTO] Inversión de Möbius sobre el potencial discreto J calculado.
    Recupera pi(x) limpiando los ecos p^k de la señal J_MFN.
    """
    print("[INFO] Aplicando Inversión de Möbius (Limpieza Espectral)...")
    pi_corrected = np.zeros(N + 1)
    max_k = int(np.log2(N))
    
    mu_vals = [mobius(k) for k in range(max_k + 2)]
    
    for k in range(1, max_k + 1):
        if mu_vals[k] == 0: continue
        
        weight = mu_vals[k] / k
        indices = np.arange(N + 1)
        roots = (indices ** (1.0/k)).astype(int)
        pi_corrected += J_counts[roots] * weight
        
    return pi_corrected

def calculo_aproximado_mfn(N):
    """
    [APROX] Implementación de la Linearización Esquelética MFN.
    Fórmula: pi(x) ~ Sum_{k=1}^{log2 x} (mu(k)/k) * Li(x^(1/k))
    
    Esta función asume que el potencial J_MFN sigue perfectamente al atractor
    logarítmico (J ~ Li), ignorando la oscilación local de paridad.
    Complejidad: O(log N) - Instantáneo.
    """
    print(f"[INFO] Ejecutando Linearización MFN (Esqueleto Logarítmico)...")
    start = time.time()
    
    total = mp.mpf(0)
    limit_k = int(np.log2(N))
    
    for k in range(1, limit_k + 1):
        m_k = mobius(k)
        if m_k == 0: continue
        
        # Núcleo de la aproximación: Li(N^(1/k))
        # Se podría agregar aquí el término de inercia (1 - Tp/t) si se desea mayor precisión en rangos bajos.
        root = mp.power(N, 1.0/k)
        term = mp.li(root)
        
        total += (m_k / k) * term
        
    print(f"[INFO] Cálculo completado en {time.time() - start:.6f}s")
    return float(total)

def get_real_pi(N):
    """Obtiene el valor real de pi(x) para referencia."""
    if N <= 100_000_000:
        print(f"[REF] Cribando para obtener pi(x) real exacto...")
        sieve = np.ones(N+1, dtype=bool); sieve[:2]=False
        for i in range(2, int(N**0.5)+1):
            if sieve[i]: sieve[i*i::i] = False
        return np.sum(sieve)
    else:
        print(f"[REF] N muy grande, usando Li(x) como proxy de 'Real' (referencia teórica)...")
        return float(mp.li(N))

def main():
    parser = argparse.ArgumentParser(description="Calculadora MFN: Determinismo de Paridad vs Ingeniería Espectral")
    parser.add_argument('N', type=int, help='Límite superior N')
    parser.add_argument('--exactly', action='store_true', help='Calcula pi(x) desde cero usando convolución de paridad (Lento, demuestra ontología)')
    parser.add_argument('--aprox', action='store_true', help='Calcula pi(x) usando la fórmula linearizada MFN (Rápido, ingeniería)')
    
    args = parser.parse_args()
    N = args.N
    
    if not (args.exactly or args.aprox):
        print("Error: Debes especificar un modo: --exactly (Teoría) o --aprox (Ingeniería).")
        return

    # Referencia
    real_pi = get_real_pi(N)
    results = {}

    # --- MODO EXACTO (Knuttzen Ontológico) ---
    if args.exactly:
        A = generar_semilla_rapida(N)
        Lambda_raw = inversion_espectral_rapida(A, N)
        Lambda_clean = np.where(Lambda_raw > 0.1, Lambda_raw, 0) # Filtro de ruido numérico
        
        # Integración J(x)
        inv_log = np.zeros(N + 1)
        inv_log[2:] = 1.0 / np.log(np.arange(2, N + 1))
        J_x = np.cumsum(Lambda_clean * inv_log)
        
        pi_exact_arr = correccion_armonicos_exacta(J_x, N)
        results['Exacto (Paridad)'] = pi_exact_arr[N]

    # --- MODO APROXIMADO (Ingeniería MFN) ---
    if args.aprox:
        val_aprox = calculo_aproximado_mfn(N)
        results['Aprox (Linear)'] = val_aprox

    # Reporte
    print("\n" + "="*70)
    print(f"RESULTADOS FINALES (N = {N:,})")
    print("="*70)
    print(f"{'MÉTODO':<25} | {'VALOR':<18} | {'DIFERENCIA':<15}")
    print("-" * 70)
    print(f"{'Real (Referencia)':<25} | {real_pi:<18,.0f} | {'0':<15}")
    
    for method, val in results.items():
        diff = val - real_pi
        print(f"{method:<25} | {val:<18,.2f} | {diff:<+15,.4f}")
    print("-" * 70)

if __name__ == "__main__":
    main()