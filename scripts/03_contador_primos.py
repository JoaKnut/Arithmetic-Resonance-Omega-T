import argparse
import mpmath
from mpmath import mp

# Configuración de precisión (50 decimales para estabilidad en exponentes)
mp.dps = 50

def calculate_K_MF():
    """
    Calcula la Impedancia Fundamental K_MF resolviendo la ecuación de balance:
    (2 - 2^-s) * zeta(s) = 4
    Referencia: Teorema 6.5 y Ec. (13)[cite: 686, 649].
    """
    # Definimos la función f(s) = (2 - 2^-s)zeta(s) - 4
    f = lambda s: (2 - mp.power(2, -s)) * mp.zeta(s) - 4
    
    # Buscamos la raíz cerca de 1.5645 usando el método de secante
    k_mf = mp.findroot(f, 1.5645)
    return k_mf

def get_li(n):
    """Calcula la Integral Logarítmica Li(n)."""
    return mp.li(n)

def knuttzen_discrete_correction(n, k_mf):
    """
    Calcula la corrección discreta basada en la paridad exacta R(k).
    Fórmula: Suma de Resolución Fina (Sección Nueva / Teorema de Suma).
    Costo: O(N) - Lineal. Precisión absoluta.
    """
    correction_sum = mp.mpf(0)
    
    # Iteramos k desde 2 hasta floor(n)
    # R(k) = 0.5 * (-1)^(floor(k)-1) -> +0.5 si impar, -0.5 si par[cite: 646].
    
    # Nota: Para n muy grandes, esto es lento.
    limit = int(n)
    
    # Pre-cálculos para el bucle
    term_s = k_mf
    
    # Bucle de suma
    for k in range(2, limit + 1):
        # Determinamos paridad: k impar (+0.5), k par (-0.5)
        # (-1)^(k-1)
        r_k = 0.5 if k % 2 != 0 else -0.5
        
        # Integral del decaimiento entre k y k+1
        # Int(s * t^-(s+1)) = k^-s - (k+1)^-s
        decay = mp.power(k, -term_s) - mp.power(k+1, -term_s)
        
        correction_sum += r_k * decay

    # Factor de escala: -(2*pi / ln(n)) [cite: 690, 696]
    scale = -(2 * mp.pi) / mp.log(n)
    
    return scale * correction_sum

def knuttzen_analytic_correction(n, k_mf):
    """
    Calcula la corrección continua usando la integral cosenoidal (Aproximación Gamma).
    Fórmula: Ley de Proyección Cosenoidal.
    Costo: O(1) vía Cuadratura Gaussiana.
    Referencia: Definición 6.6 y Teorema 7.3[cite: 654, 690].
    """
    # Definimos el integrando: cos(pi*t) / t^(s+1)
    # Nota: Usamos la forma de cuadratura numérica de alta precisión de mpmath
    # que es equivalente a evaluar la Gamma Incompleta pero más directa para límites finitos.
    
    integrand = lambda t: mp.cos(mp.pi * t) / mp.power(t, k_mf + 1)
    
    # Integral definida de 2 a n
    integral_val = mp.quad(integrand, [2, n])
    
    # Factor de escala derivado: (pi * s) / ln(n)
    # Nota: El factor 2pi se cancela con el 0.5 del residuo cosenoidal R(x) = -0.5 cos(pi x).
    # Signo positivo porque R(x) y la corrección tienen signos opuestos en la identidad.
    scale = (mp.pi * k_mf) / mp.log(n)
    
    return scale * integral_val

def main():
    parser = argparse.ArgumentParser(description='Calculadora de Primos MFN (Modelo Frecuencial de Knuttzen)')
    parser.add_argument('n', type=float, help='Número hasta el cual contar primos')
    parser.add_argument('--exactly', action='store_true', help='Usar cálculo discreto (lento, máxima precisión)')
    parser.add_argument('--aprox', action='store_true', help='Usar cálculo analítico continuo (rápido, alta precisión asintótica)')
    
    args = parser.parse_args()
    n = mp.mpf(args.n)
    
    print("-" * 50)
    print(f"CALCULADORA DE RESONANCIA GEOMÉTRICA (MFN)")
    print("-" * 50)

    # 1. Calcular K_MF
    print("Calculando constante de impedancia K_MF con alta precisión...")
    k_mf = calculate_K_MF()
    print(f"K_MF (Calculado): {k_mf}")
    print("-" * 50)

    # 2. Calcular Li(n)
    li_val = get_li(n)
    print(f"Li({int(n)}): {li_val}")

    # 3. Calcular Corrección
    correction = 0
    method = ""

    if args.exactly:
        if n > 1000000:
            print("ADVERTENCIA: El modo --exactly es O(N). Para N > 10^6 se recomienda --aprox.")
        print("Ejecutando corrección discreta (Suma de Paridad)...")
        correction = knuttzen_discrete_correction(n, k_mf)
        method = "Discreto (Exacto)"
        
    elif args.aprox:
        print("Ejecutando corrección analítica (Integral Cosenoidal/Gamma)...")
        correction = knuttzen_analytic_correction(n, k_mf)
        method = "Analítico (Cosenoidal)"
    else:
        print("Por favor seleccione un modo: --exactly o --aprox")
        return

    # 4. Resultado Final
    pi_mfn = li_val + correction
    
    print("-" * 50)
    print(f"RESULTADOS para N = {int(n)}")
    print(f"Método: {method}")
    print(f"Corrección MFN (Energía): {correction}")
    print(f"Predicción pi(N): {pi_mfn}")
    print(f"Valor Entero: {int(mp.nint(pi_mfn))}")
    print("-" * 50)

if __name__ == "__main__":
    main()
