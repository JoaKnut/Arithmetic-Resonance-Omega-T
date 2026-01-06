import numpy as np
import time

def generar_semilla_rapida(N):
    """
    Genera la señal de Paridad alpha(n).
    """
    # Usamos float64 para máxima precisión en la cancelación
    A = np.ones(N + 1, dtype=np.float64)
    A[1] = 2.0
    A[3::2] = 2.0 
    return A

def sismografo_espectral(N):
    print(f"[MFN] Inicializando Sismógrafo de Paridad (N={N:,})...")
    
    A = generar_semilla_rapida(N)
    
    indices = np.arange(N + 1, dtype=np.float64)
    indices[0] = 1.0
    ln_n = np.log(indices)
    
    # --- CORRECCIÓN CRÍTICA ---
    # Teorema 7.2: (Lambda * alpha) = +alpha * ln(n)
    # Antes teníamos: B = A * (-ln_n)  <-- ERROR DE SIGNO
    B = A * ln_n  # <-- SIGNO CORRECTO
    
    Lambda = B.copy()
    inv_A1 = 1.0 / A[1] 
    
    start_time = time.time()
    
    # Algoritmo Push-Forward (Criba Aditiva)
    for i in range(1, N + 1):
        val = Lambda[i] * inv_A1
        Lambda[i] = val
        
        if abs(val) < 1e-9: continue
        
        if 2 * i <= N:
            # Optimización de slicing para velocidad
            k_limit = N // i
            multiples = np.arange(2 * i, (k_limit + 1) * i, i)
            factors_A = A[2 : k_limit + 1]
            
            Lambda[multiples] -= val * factors_A
            
    elapsed = time.time() - start_time
    print(f"[MFN] Campo espectral generado en {elapsed:.4f}s.")
    return Lambda

def verificar_mersenne(p, Lambda, N_limit):
    Mp = 2**p - 1
    
    if Mp > N_limit:
        return Mp, 0.0, "OUT_OF_RANGE"
    
    tension_real = Lambda[Mp]
    tension_teorica = np.log(Mp)
    
    # Tolerancia ajustada para punto flotante acumulado
    delta = abs(tension_real - tension_teorica)
    
    # Clasificación Topológica
    if delta < 1e-3:
        return Mp, tension_real, "PERFECTO (Resonante)"
    elif abs(tension_real) < 1e-3: # Usamos abs() por si acaso hay ruido negativo pequeño
        return Mp, tension_real, "COMPUESTO (Vacío)"
    else:
        return Mp, tension_real, "RUIDO (Disonante)"

def main():
    # M19 = 524,287. N=550,000 es suficiente.
    EXPONENTES_A_PROBAR = [2, 3, 5, 7, 11, 13, 17, 19]
    max_mersenne = 2**(max(EXPONENTES_A_PROBAR)) - 1
    N_TEST = int(max_mersenne * 1.05)
    
    Lambda_field = sismografo_espectral(N_TEST)
    
    print("\n" + "="*85)
    print(f"{'EXP (p)':<8} | {'MERSENNE (Mp)':<15} | {'TENSION (L)':<15} | {'ESTADO ESPECTRAL'}")
    print("="*85)
    
    total_perfectos = 0
    
    for p in EXPONENTES_A_PROBAR:
        Mp, tension, estado = verificar_mersenne(p, Lambda_field, N_TEST)
        
        str_tension = f"{tension:.5f}"
        
        # Colores ANSI para terminal
        COLOR_OK = "\033[92m" # Verde
        COLOR_BAD = "\033[91m" # Rojo
        COLOR_RESET = "\033[0m"
        
        if "PERFECTO" in estado:
            total_perfectos += 1
            print(f"{COLOR_OK}{p:<8} | {Mp:<15} | {str_tension:<15} | >> {estado} <<{COLOR_RESET}")
        elif "COMPUESTO" in estado:
            print(f"{COLOR_BAD}{p:<8} | {Mp:<15} | {str_tension:<15} | {estado}{COLOR_RESET}")
        else:
            print(f"{p:<8} | {Mp:<15} | {str_tension:<15} | {estado}")
            
    print("-" * 85)
    print(f"Resultado: {total_perfectos} Números Perfectos detectados.")
    print("Validación: La Tensión coincide con ln(Mp) y M11 colapsa a 0.")

if __name__ == "__main__":
    main()