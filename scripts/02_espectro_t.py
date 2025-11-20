import math
import argparse
from decimal import Decimal, getcontext

# Aumentamos precisión para ver convergencia fina
getcontext().prec = 50

def explicar_contexto():
    print("""
    ===========================================================================
    SCRIPT 2: ESPECTRO DE RESONANCIA T(n)
    Referencia: Sección 8 del paper.
    ===========================================================================
    
    Calcula la suma infinita T(n) = Sum [ Prod (1 / (1 + Omega(n*2^j))) ].
    
    Objetivos de verificación:
      1. Primos (p): Deben converger a ~2.410142 (Constante Gaussiana).
      2. n=4: Debe converger a 'e' (2.71828...).
      3. Perfectos (6, 28...): Deben tender a 1 a medida que p crece.
    """)

def omega_fast(n):
    """Calcula Omega(n) = d(2n) - 4 directamente."""
    # Factorización simple para d(m)
    m = 2 * n
    if m == 1: return -3 # Ajuste técnico, d(2)=2 -> 2-4=-2
    
    divisors = 0
    limit = int(math.isqrt(m))
    for i in range(1, limit + 1):
        if m % i == 0:
            divisors += 1
            if i*i != m:
                divisors += 1
    return divisors - 4

def calcular_T(n, max_iter=100):
    """
    Calcula la serie T(n) hasta que el término sea despreciable o max_iter.
    Usa Decimal para precisión.
    """
    suma_total = Decimal(0)
    producto_acumulado = Decimal(1)
    
    # El término k=0 es el producto vacío = 1.
    # La fórmula es Sum_{k=0} Prod_{j=0}^{k-1} ...
    
    # k=0
    suma_total += producto_acumulado 
    
    for k in range(1, max_iter):
        # Calculamos el factor del producto para j = k-1
        # term = 1 / (1 + Omega(n * 2^(k-1)))
        arg = n * (2**(k-1))
        om = omega_fast(arg)
        denom = 1 + om
        
        if denom == 0:
            # Evitar división por cero si Omega = -1 (no debería pasar para n>=3)
            break
            
        factor = Decimal(1) / Decimal(denom)
        producto_acumulado *= factor
        
        suma_total += producto_acumulado
        
        if producto_acumulado < Decimal("1e-20"):
            break
            
    return suma_total

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script 2: Analizador Espectral T(n)")
    parser.add_argument("--target", type=int, help="Calcular T(n) para un número específico")
    args = parser.parse_args()

    explicar_contexto()

    targets = []
    if args.target:
        targets = [("Usuario", args.target)]
    else:
        targets = [
            ("Primo (p=5)", 5),
            ("Primo (p=13)", 13),
            ("Base (n=4)", 4),
            ("Perfecto (p=2)", 6),
            ("Perfecto (p=3)", 28),
            ("Perfecto (p=5)", 496),
            ("Perfecto (p=7)", 8128)
        ]

    # Constantes teóricas
    TEORICA_P = Decimal(1) + Decimal(math.sqrt(math.pi/2)) * Decimal(math.exp(0.5)) * Decimal(math.erf(1/math.sqrt(2)))
    TEORICA_4 = Decimal(math.e)

    print(f"{'TIPO (n)':<20} | {'T(n) CALCULADO':<25} | {'TEORÍA / NOTAS'}")
    print("-" * 75)

    for label, n in targets:
        val = calcular_T(n)
        nota = ""
        
        if n == 4:
            diff = val - TEORICA_4
            nota = f"Error vs e: {diff:.2e}"
        elif omega_fast(n) == 0 and n != 4: # Primo
            diff = val - TEORICA_P
            nota = f"Error vs Tp: {diff:.2e}"
        elif label.startswith("Perfecto"):
            nota = f"Distancia a 1: {val - 1:.6f}"
            
        print(f"{label + ' (' + str(n) + ')':<20} | {val:.10f}...            | {nota}")
