import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import math

def explicar_contexto():
    print("""
    ===========================================================================
    SCRIPT 1: LA CRIBA DE RESONANCIA (Sintetizador Aditivo MFN)
    Referencia: Secciones 2, 3, 5 y 9 del paper de J. Knuttzen.
    ===========================================================================
    
    Este script prueba la hipótesis de que la función Omega(n) puede construirse
    mediante la propagación de la 'Semilla Frecuencial' Lambda_MF, sin necesidad
    de factorización de enteros.
    
    La identidad a probar es: Omega = Lambda_MF * 1 (Convolución)
    
    Valores de la Semilla:
      - n=1:       -2
      - n par:      1
      - n impar>1:  2
      
    El script genera un array, propaga estas ondas y verifica si los ceros 
    resultantes corresponden a los números primos (y n=4).
    """)

def criba_resonancia(N):
    """
    Calcula Omega(n) usando la propagación de la semilla (O(N log N)).
    """
    # Inicializamos array de ceros. Indice i corresponde al número i.
    # Usamos N+1 para ignorar el índice 0 y hacerlo directo.
    omega_arr = np.zeros(N + 1, dtype=int)
    
    print(f"[INFO] Iniciando propagación de semilla hasta N={N}...")
    t0 = time.time()

    # 1. Caso n=1: Valor -2. Se suma a TODOS los múltiplos de 1.
    omega_arr[1::1] += -2
    
    # 2. Caso n par: Valor 1. Se suma a todos los múltiplos de números pares.
    # Los pares son 2, 4, 6...
    for i in range(2, N + 1, 2):
        omega_arr[i::i] += 1
        
    # 3. Caso n impar > 1: Valor 2. Se suma a múltiplos de impares.
    for i in range(3, N + 1, 2):
        omega_arr[i::i] += 2
        
    dt = time.time() - t0
    print(f"[INFO] Criba completada en {dt:.4f} segundos.")
    return omega_arr

def verificar_primalidad(omega_arr, N):
    """
    Verifica cuantos primos fueron detectados correctamente (Omega=0).
    Recordar: El paper dice que Omega(n)=0 <-> n es primo o n=4.
    """
    errores = 0
    falsos_positivos = []
    falsos_negativos = [] # Primos que no dieron 0
    
    # Lista simple de primos para verificación (usando criba clásica para ground truth)
    es_primo_truth = np.ones(N + 1, dtype=bool)
    es_primo_truth[0:2] = False
    for i in range(2, int(math.sqrt(N)) + 1):
        if es_primo_truth[i]:
            es_primo_truth[i*i::i] = False
            
    detected_count = 0
    
    print("[INFO] Verificando contra Ground Truth...")
    
    for n in range(3, N + 1): # Empezamos en 3 según definición del paper
        val = omega_arr[n]
        is_p = es_primo_truth[n]
        
        # Predicción del modelo MFN
        modelo_dice_primo = (val == 0)
        
        if n == 4:
            # Excepción conocida del modelo
            if val != 0: 
                print(f"  [ALERTA] n=4 no dio 0. Valor: {val}")
            continue

        if modelo_dice_primo and not is_p:
            errores += 1
            falsos_positivos.append(n)
        elif not modelo_dice_primo and is_p:
            errores += 1
            falsos_negativos.append(n)
        elif modelo_dice_primo and is_p:
            detected_count += 1

    return errores, falsos_positivos, falsos_negativos, detected_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script 1: Criba de Resonancia MFN")
    parser.add_argument("--max", type=int, default=100000, help="Número máximo N para la simulación")
    parser.add_argument("--plot", action="store_true", help="Graficar los primeros 100 valores")
    args = parser.parse_args()

    explicar_contexto()
    
    omega_sintetizado = criba_resonancia(args.max)
    err, fp, fn, count = verificar_primalidad(omega_sintetizado, args.max)
    
    print("\nResultados de Validación:")
    print(f"  - Rango analizado: [3, {args.max}]")
    print(f"  - Primos detectados (Omega=0): {count}")
    print(f"  - Errores totales: {err}")
    
    if len(fp) > 0:
        print(f"  - Falsos Positivos (Dicen ser primos y no lo son): {fp[:10]} ...")
    else:
        print("  - Falsos Positivos: 0 (Validación Exitosa)")
        
    if len(fn) > 0:
        print(f"  - Falsos Negativos (Son primos y Omega!=0): {fn[:10]} ...")
    else:
        print("  - Falsos Negativos: 0 (Validación Exitosa)")

    if args.plot:
        plt.figure(figsize=(12, 6))
        x = np.arange(3, 103)
        y = omega_sintetizado[3:103]
        colors = ['red' if val==0 else 'blue' for val in y]
        plt.bar(x, y, color=colors)
        plt.title(r"Valores de $\Omega(n)$ generados por Semilla (Rojo = Primos + n=4)")
        plt.xlabel("n")
        plt.ylabel(r"$\Omega(n)$")
        plt.grid(True, alpha=0.3)
        plt.savefig('criba_mfn.png')
        print("\n¡Gráfico guardado como 'criba_mfn.png' en la misma carpeta!")
