import math

def d(n):
    """
    Calcula la función de divisor d(n): el número de divisores positivos de n.
    """
    if n <= 0:
        return 0
    n = int(n)
    count = 0
    limit = int(math.sqrt(n))

    for i in range(1, limit + 1):
        if n % i == 0:
            # Si los divisores son iguales (ej. n=9, i=3), solo cuenta uno.
            if i * i == n:
                count += 1
            # De lo contrario, cuenta ambos (ej. n=12, i=2, cuenta 2 y 6).
            else:
                count += 2
    return count

def omega(n):
    """
    Calcula la función de Resonancia Armónica Omega(n), definida como d(2n) - 4.
    """
    if n <= 0:
        return None # Omega no está definida para n <= 0 en este contexto.
    
    # La definición central de la teoría
    return d(2 * n) - 4

# --- Bloque de Prueba ---
if __name__ == "__main__":
    """
    Ejecuta algunas pruebas básicas para verificar las funciones omega(n) y d(n).
    Basado en las proposiciones del artículo:
    - Omega(p) = 0 (para p primo > 2)
    - Omega(4) = 0
    - Omega(potencia_primo)
    """
    print("--- Verificación de omega_d2n_core.py ---")
    
    # 1. Primos (deben ser 0)
    print(f"Omega(3) [Primo]: {omega(3)}")  # d(6)-4 = 4-4 = 0
    print(f"Omega(5) [Primo]: {omega(5)}")  # d(10)-4 = 4-4 = 0
    print(f"Omega(7) [Primo]: {omega(7)}")  # d(14)-4 = 4-4 = 0
    
    # 2. Caso n=4 (debe ser 0)
    print(f"Omega(4) [Caso Base]: {omega(4)}") # d(8)-4 = 4-4 = 0
    
    # 3. Compuestos (deben ser > 0)
    print(f"Omega(6) [Compuesto]: {omega(6)}") # d(12)-4 = 6-4 = 2
    print(f"Omega(8) [Compuesto]: {omega(8)}") # d(16)-4 = 5-4 = 1
    
    # 4. Fórmula (d): Omega(2^r) = r-2
    print(f"Omega(16) [2^4]: {omega(16)}") # d(32)-4 = 6-4 = 2. (r-2 = 4-2 = 2)
    print(f"Omega(32) [2^5]: {omega(32)}") # d(64)-4 = 7-4 = 3. (r-2 = 5-2 = 3)
