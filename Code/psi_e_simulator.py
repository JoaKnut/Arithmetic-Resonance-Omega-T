import math
import functools

# =============================================================================
# DEFINICIONES BASE (Secciones 3, 4, 7)
# =============================================================================

@functools.lru_cache(maxsize=None)
def count_divisors(m):
    """Calcula d(m), el número de divisores de m."""
    if m == 0:
        return 0
    count = 0
    limit = int(math.sqrt(m))
    for i in range(1, limit + 1):
        if m % i == 0:
            count += 2  # Añade i y m/i
    if limit * limit == m:
        count -= 1  # Corrige si es un cuadrado perfecto
    return count

@functools.lru_cache(maxsize=None)
def omega(n):
    """
    Implementa Omega(n) = d(2n) - 4 (Proposición 3.2).
    Usamos n >= 3 según la definición 3.1.
    """
    if n < 3:
        return 0  # Definido para n >= 3
    return count_divisors(2 * n) - 4

# Constante de Primos (Prop. 7.5)
T_p = 1.0 + math.sqrt(math.pi / 2.0) * math.exp(0.5) * math.erf(1.0 / math.sqrt(2.0))
# T_p ≈ 2.410142264...

# Límite de la serie infinita T(n)
T_SERIES_LIMIT = 5

@functools.lru_cache(maxsize=None)
def T(n):
    """
    Implementa T(n) (Definición 7.1).
    Aproximamos la serie infinita truncándola en T_SERIES_LIMIT.
    """
    # Caso especial T(4) = e (Prop. 7.6)
    if n == 4:
        return math.e
    
    # Caso especial T(p) (Prop. 7.5)
    if n > 4 and omega(n) == 0: # Es primo
        return T_p

    T_n = 1.0  # Término k=0 (producto vacío)
    current_product = 1.0

    for k in range(1, T_SERIES_LIMIT):
        j = k - 1
        denominator = 1.0 + omega(n * (2**j))
        
        # Si el denominador es 0 (ej. omega(n*2^j) = -1), la serie diverge.
        # Esto no debería pasar con omega = d(2n)-4, ya que d(m) >= 2 para m >= 2.
        if denominator == 0:
            return float('inf') 

        current_product *= (1.0 / denominator)
        T_n += current_product
        
        # Si el término es muy pequeño, paramos pronto
        if current_product < 1e-100:
            break
            
    return T_n

@functools.lru_cache(maxsize=None)
def is_prime(n):
    """Test de primalidad simple para la definición de Psi."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.sqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True

# =============================================================================
# SIMULACIÓN DEL SISMÓGRAFO (Sección 8)
# =============================================================================

def analyze_resonance_error(N_limit):
    """
    Calcula Psi_E(n) hasta N_limit y analiza el error
    respecto a la Conjetura 8.3 (Equivalencia HR).
    """
    print(f"Iniciando simulación del Modelo Knuttzen hasta N = {N_limit}...")
    print(f"Constante de Primos T_p = {T_p:.6f}")
    print(f"Aproximando T(n) con {T_SERIES_LIMIT} términos.\n")
    
    # Psi_E(2) = 0 (Def. 8.1)
    psi_E = 0.0
    psi_values = {2: 0.0}

    # --- PASO 1: Calcular todos los valores de Psi_E(n) ---
    # Esto es intensivo y puede tardar.
    for n in range(3, N_limit + 1):
        if is_prime(n):
            # Regla de Drenaje (Primos)
            if psi_E == 0:
                # Evitar división por cero si el primo anterior era 2
                psi_E = 0.0
            else:
                psi_E = psi_E / T_p
        else:
            # Regla de Fuente (Compuestos)
            psi_E = psi_E + T(n)
        
        psi_values[n] = psi_E
        
        if n % (N_limit // 10) == 0:
            print(f"  Calculando... {n}/{N_limit}")

    print("\nCálculo de Psi_E(n) completo.")
    
    # --- PASO 2: Estimar C y analizar el Error ---
    # Prop. 8.2: Psi_E(n) ≈ C * log(n)
    # Estimamos C usando el valor final
    
    if N_limit < 10:
        print("N_limit demasiado bajo para estimar C.")
        return

    C_estimated = psi_values[N_limit] / math.log(N_limit)
    print(f"Constante 'C' estimada (C ≈ Psi_E(N)/log(N)): {C_estimated:.6f}\n")
    
    print("--- Análisis del Error (Conjetura 8.3 vs. HR) ---")
    print("La HR es verdadera si 'Error_Ratio' permanece acotado.")
    print("-" * 70)
    print(f"{'n':>10} | {'Psi_E(n)':>12} | {'Error |Psi-C*log(n)|':>22} | {'Ratio [Error/sqrt(n)]':>22}")
    print("-" * 70)

    # Analizamos el error en 20 puntos de muestra
    sample_points = sorted(list(set(int(N_limit * (i / 20.0)) for i in range(1, 21))))
    
    for n in sample_points:
        if n < 10: continue # Evitar log(n) pequeños
        
        psi_E = psi_values[n]
        
        # El "comportamiento esperado" (TNP)
        trend = C_estimated * math.log(n)
        
        # El "Error de Resonancia" (Def. 8.2)
        error = abs(psi_E - trend)
        
        # El límite de la HR (Conjetura 8.3)
        hr_bound = math.sqrt(n)
        
        # El ratio que debe permanecer acotado
        error_ratio = error / hr_bound
        
        print(f"{n:>10} | {psi_E:>12.4f} | {error:>22.4f} | {error_ratio:>22.6f}")

# =============================================================================
# EJECUCIÓN
# =============================================================================

# ADVERTENCIA: N=10,000 puede tardar varios minutos.
# N=100,000 puede tardar horas.
# N=10^10 (como se mencionó) es computacionalmente imposible
# con este script simple.
analyze_resonance_error(N_limit=1000000)