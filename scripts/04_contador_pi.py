import numpy as np
import time
import argparse
import math

def explicar_contexto():
    print("""
    ===========================================================================
    SCRIPT 4: CONTADOR DE PRIMOS DE KNUTTZEN (Teorema 5.2)
    ===========================================================================
    
    Implementación exacta de la fórmula analítica:
    
        pi(N) = floor( Sum_{n=3}^{N} N^(-Omega(n)) )
        
    Método:
    1. Generamos el vector Omega(n) usando la Semilla Lambda_MF (sin factorizar).
       Identidad: Omega = Lambda_MF * 1 (Sintetizador Aditivo).
       
    2. Calculamos la suma de potencias inversas.
       - Si n es primo (o 4), Omega(n)=0  => Término = N^0 = 1.
       - Si n es compuesto,   Omega(n)>=1 => Término <= 1/N.
       
    3. La parte entera (floor) elimina los residuos decimales de los compuestos.
    
    Este método transforma el conteo de primos en un problema de 
    procesamiento de señal y suma de amplitudes.
    """)

def generar_omega_con_semilla(N):
    """
    Genera el array de Omega(n) usando la identidad de convolución de la Semilla.
    Complejidad: O(N log N)
    """
    # Array inicializado a 0. Tamaño N+1 para usar índices directos.
    omega = np.zeros(N + 1, dtype=int)
    
    print(f"[INFO] Generando campo de resonancia Omega hasta N={N}...")
    t0 = time.time()
    
    # 1. Contribución de la unidad (n=1): Semilla = -2
    # Se suma a todos los enteros (múltiplos de 1)
    omega[1::1] += -2
    
    # 2. Contribución de los pares (n=2, 4, 6...): Semilla = 1
    # Se suma a sus múltiplos.
    for i in range(2, N + 1, 2):
        omega[i::i] += 1
        
    # 3. Contribución de los impares > 1 (n=3, 5, 7...): Semilla = 2
    # Se suma a sus múltiplos.
    for i in range(3, N + 1, 2):
        omega[i::i] += 2
        
    dt = time.time() - t0
    print(f"[INFO] Campo generado en {dt:.4f} s.")
    return omega

def calcular_pi_knuttzen(N, omega_arr):
    """
    Aplica la fórmula S_N = sum( N^(-Omega(n)) ) para n en [3, N].
    Retorna el valor crudo (float) y el valor entero (pi).
    """
    print(f"[INFO] Calculando suma armónica S_{N}...")
    
    suma_S = 0.0
    
    # Iteramos desde n=3 hasta N (según definición del paper)
    # Nota: Usamos longdouble para mayor precisión en N grandes, 
    # aunque la convergencia es robusta.
    
    # Optimizacion vectorizada con numpy para velocidad
    # Extraemos el subarray de interés [3...N]
    sub_omega = omega_arr[3:N+1]
    
    # Calculamos términos: N ** (-Omega)
    # Nota matemática: 
    # Si Omega=0 -> 1
    # Si Omega>0 -> muy pequeño
    
    # Para evitar overflow/underflow con N muy grandes en float estándar,
    # separamos lógica:
    
    ceros = np.sum(sub_omega == 0) # Términos que suman exactamente 1
    compuestos = sub_omega[sub_omega > 0] # Términos residuales
    
    # Suma principal (Parte Entera)
    suma_enteros = float(ceros)
    
    # Suma residual (Parte Decimal)
    # terminos_residuales = N ** (-compuestos)
    # Usamos logaritmos para estabilidad si N es gigante, o directo si cabe en float.
    # Dado que N^(-k) decae rapidísimo, la suma directa suele ser segura.
    terminos_residuales = np.power(float(N), -compuestos.astype(float))
    suma_residual = np.sum(terminos_residuales)
    
    S_total = suma_enteros + suma_residual
    return S_total, int(math.floor(S_total))

def pi_referencia(N):
    """Cálculo estándar de pi(x) para comparar (Criba simple)."""
    if N < 2: return 0
    criba = np.ones(N+1, dtype=bool)
    criba[0:2] = False
    for i in range(2, int(math.isqrt(N))+1):
        if criba[i]:
            criba[i*i::i] = False
    return np.sum(criba)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script 4: Calculadora Pi(N) de Knuttzen")
    parser.add_argument("N", type=int, help="Límite superior N")
    parser.add_argument("--verbose", action="store_true", help="Ver detalles")
    args = parser.parse_args()

    explicar_contexto()
    
    if args.N < 4:
        print("Error: N debe ser mayor o igual a 4 según la definición.")
        exit()

    # 1. Generar Omega usando la Semilla
    omega = generar_omega_con_semilla(args.N)
    
    # 2. Aplicar Fórmula de Knuttzen
    S_val, pi_calc = calcular_pi_knuttzen(args.N, omega)
    
    # 3. Obtener valor real para validar
    pi_real = pi_referencia(args.N)
    
    print("-" * 60)
    print(f"RESULTADOS PARA N = {args.N}")
    print("-" * 60)
    print(f"Valor de la Suma S_N (Teórico): {S_val:.10f}...")
    print(f"Parte Entera floor(S_N):      {pi_calc}")
    print(f"Valor Real pi(N):             {pi_real}")
    print("-" * 60)
    
    if pi_calc == pi_real:
        print(">> VERIFICACIÓN: EXITOSA. La fórmula coincide exactamente.")
    else:
        diff = abs(pi_calc - pi_real)
        print(f">> VERIFICACIÓN: FALLIDA. Diferencia de {diff}.")
        
    # Análisis del Residuo (Curiosidad matemática)
    residuo = S_val - pi_calc
    print(f"\n[Análisis del Residuo]")
    print(f"El término residual R(N) fue: {residuo:.10f}")
    print(f"Según el paper, debe ser 0 < R(N) < 1. ¿Cumple?: {0 < residuo < 1}")
