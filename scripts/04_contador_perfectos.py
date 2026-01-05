import numpy as np
import time

def generar_semilla_rapida(N):
    """
    Genera la señal de Paridad A(n).
    1 = Par, 2 = Impar (normalizado por base).
    """
    A = np.ones(N + 1, dtype=np.float64)
    A[1] = 2.0
    A[3::2] = 2.0 
    return A

def inversion_espectral_semilla(N):
    """
    Calcula la Semilla Lambda_MF(n) mediante convolución inversa.
    Esta es la 'Tensión' del sistema en cada entero.
    """
    print(f"[FISICA] Cargando sistema de paridad hasta N={N}...")
    
    # 1. Definir A y su inverso logarítmico B
    A = generar_semilla_rapida(N)
    indices = np.arange(N + 1, dtype=np.float64)
    indices[0] = 1.0 
    ln_n = np.log(indices)
    ln_n[0] = 0.0
    
    B = A * (-ln_n) # Parte derecha de la ecuación de convolución
    
    # 2. Resolver la convolución Lambda * A = B
    # Lambda = (B - Sum_{d|n, d<n} Lambda(d)A(n/d)) / A(1)
    Lambda = np.zeros(N + 1, dtype=np.float64)
    inv_A1 = 1.0 / A[1] 
    
    start = time.time()
    
    # Algoritmo "Push-Forward" (Criba aditiva de Dirichelt) O(N log N)
    # En lugar de buscar divisores hacia atrás, empujamos el valor hacia adelante.
    
    # Inicializamos Lambda con B (el término fuente)
    Lambda = B.copy()
    
    for i in range(1, N + 1):
        # En el paso i, Lambda[i] ya tiene acumuladas las restas de sus divisores anteriores
        # Solo falta normalizar por A(1)
        val = Lambda[i] * inv_A1
        Lambda[i] = val
        
        # Si el valor es significativo, propagar a los múltiplos (futuros n)
        if abs(val) < 1e-9: continue
        
        # Restar val * A(k) a todos los múltiplos k*i
        # El rango comienza en 2*i
        if 2 * i <= N:
            # Vectorización numpy para velocidad
            k_limit = N // i
            multiples = np.arange(2 * i, (k_limit + 1) * i, i)
            
            # Los factores A correspondientes son A[2], A[3]... A[k_limit]
            factors_A = A[2 : k_limit + 1]
            
            Lambda[multiples] -= val * factors_A
            
    print(f"[SISTEMA] Campo Lambda generado en {time.time() - start:.2f}s")
    return Lambda

def detector_perfectos_mfn(Lambda, N):
    """
    Implementa la Ecuación Determinista P(x).
    Verifica la tensión en M_p = 2^p - 1.
    """
    print("\n" + "="*70)
    print(f"{'CANDIDATO (p)':<15} | {'INDICE (Mp)':<15} | {'TENSION (L)':<15} | {'ESTADO'}")
    print("="*70)
    
    # Lista de exponentes primos a probar
    # p=11 genera 2047 (23*89) -> NO debe ser perfecto
    exponentes = [2, 3, 5, 7, 11, 13, 17] 
    
    perfectos_hallados = 0
    
    for p in exponentes:
        Mp = 2**p - 1
        
        if Mp > N:
            print(f"p={p:<13} | {Mp:<15} | {'FUERA DE RANGO':<15} | --")
            continue
            
        tension = Lambda[Mp]
        esperado = np.log(Mp)
        
        # Criterio de Resonancia: ¿La tensión es igual al logaritmo?
        # Usamos una tolerancia pequeña por errores flotantes
        es_resonante = abs(tension - esperado) < 1e-4
        
        estado = ""
        if es_resonante:
            estado = ">> PERFECTO DETECTADO <<"
            perfectos_hallados += 1
            num_perfecto = Mp * (2**(p-1))
            # Nota: Imprimimos el Número Perfecto generado
        elif tension < 1e-4:
            estado = "VACIO (Compuesto)"
        else:
            estado = "RUIDO (No primo)"
            
        print(f"p={p:<13} | {Mp:<15} | {tension:<15.4f} | {estado}")
        if es_resonante:
            print(f"   -> Genera N = {Mp} * 2^{p-1} = {Mp * (2**(p-1))}")

    print("-" * 70)
    print(f"Total detectados en rango [1, {N}]: {perfectos_hallados}")

if __name__ == "__main__":
    # N = 140000 es suficiente para M17 (131071)
    N_TEST = 140000 
    Lambda_field = inversion_espectral_semilla(N_TEST)
    detector_perfectos_mfn(Lambda_field, N_TEST)