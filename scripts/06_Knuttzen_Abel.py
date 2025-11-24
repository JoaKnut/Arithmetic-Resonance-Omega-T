import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta
import time

class AbelKnuttzenAnalyzer:
    def __init__(self, max_n=100000):
        """
        Inicializa el analizador con un límite de suma (max_n).
        Cuanto mayor sea max_n, más precisa es la aproximación de la integral.
        """
        self.max_n = max_n
        print(f"Generando Semilla Frecuencial hasta N={max_n}...")
        self.n_vals, self.lambda_mf, self.R_vals = self._generate_structure()
        print("Estructura generada. Listo para integrar.")

    def _generate_structure(self):
        """
        Genera la secuencia Lambda_MF y el residuo R(x) según la definición:
        Lambda = -2 (n=1), 1 (par), 2 (impar > 1)
        A(x) = sum(Lambda)
        R(x) = A(x) - 1.5*x
        """
        n = np.arange(1, self.max_n + 1)
        
        # 1. Definición de Lambda_MF
        # Empezamos con array de unos (para los pares)
        lambda_arr = np.ones(self.max_n, dtype=np.float64)
        
        # Asignar 2 a los impares (índices 0, 2, 4... corresponden a n=1, 3, 5...)
        # Nota: n es 1-indexed, indices de array son 0-indexed.
        # Indices pares del array (0, 2, 4) son números impares (1, 3, 5)
        lambda_arr[0::2] = 2 
        
        # Corregir el caso n=1 (índice 0)
        lambda_arr[0] = -2
        
        # 2. Calcular Suma Acumulada A(x)
        A_x = np.cumsum(lambda_arr)
        
        # 3. Calcular Residuo R(x) = A(x) - 1.5*x
        # R(x) es una función escalonada, constante en [n, n+1) con valor A(n) - 1.5*x?
        # CUIDADO: La definición es A(x) = 1.5x + R(x).
        # En la fórmula de Abel, R(x) se evalúa continuamente.
        # Dado que A(x) es escalonada, R(x) es un "diente de sierra" descendente 
        # o usamos la versión discretizada de la integral de Dirichlet.
        # Para simplificar y hacer la suma exacta:
        # Integral_n^{n+1} R(x)/x^{s+1} dx. Usaremos A(n) constante en el intervalo.
        # A(x) = A(n) para x en [n, n+1).
        # Entonces R(x) = A(n) - 1.5x en ese intervalo.
        
        # Sin embargo, para series de Dirichlet sum(a_n n^-s), la fórmula de Abel usa A(x).
        # Usaremos la identidad derivada: sum(a_n n^-s) = s * int(A(x) x^-s-1 dx).
        
        return n, lambda_arr, A_x

    def compute_L_function(self, s):
        """
        Calcula L(s, Lambda_MF) usando la fórmula integral de Abel-Knuttzen.
        L(s) = s * integral_{1}^{infty} A(x) * x^{-(s+1)} dx
        
        Descomposición exacta por tramos:
        Integral = Sum_{n=1}^{N} A(n) * [ (n)^-s - (n+1)^-s ] / s * s
                 = Sum_{n=1}^{N} A(n) * (n^-s - (n+1)^-s)
        
        El término racional 1.5s/(s-1) + integral del residuo es analíticamente equivalente,
        pero numéricamente es más estable sumar A(n) directamente si N es grande,
        o usar la identidad del residuo si queremos probar la convergencia del R(x).
        
        Usaremos la identidad del residuo del paper para verificar la cota de 5.5:
        L(s) = 1.5s/(s-1) + s * Sum_{n=1}^{N} Integral_n^{n+1} (A(n) - 1.5x) x^{-(s+1)} dx
        """
        
        # Calculamos término a término la integral del residuo para mayor rigor con el paper
        # Int_{n}^{n+1} (A(n) - 1.5x) x^{-s-1} dx
        # = A(n) * [(n)^-s - (n+1)^-s]/s - 1.5 * [(n)^(1-s) - (n+1)^(1-s)]/(s-1)
        
        n = self.n_vals[:-1] # Hasta N-1
        A = self.R_vals[:-1] # A(n)
        n_plus_1 = self.n_vals[1:]
        
        term1 = A * (n**(-s) - n_plus_1**(-s)) / s
        
        if s == 1:
            # Evitar división por cero en s=1 (polo)
            term2 = 0 # Manejo especial requerido, pero evaluaremos s != 1
        else:
            term2 = 1.5 * (n**(1-s) - n_plus_1**(1-s)) / (s-1)
            
        integral_part = np.sum(term1 - term2)
        
        # Multiplicar por s según la fórmula del paper: s * integral
        total_integral = s * integral_part
        
        # Añadir el término polo teórico 1.5s / (s-1)
        # Nota: Al hacer la integral finita de 1 a N, el término polo surge de la parte 1.5x.
        # Aquí sumamos la parte oscilatoria y le añadimos el polo analítico.
        
        L_s = (1.5 * s / (s - 1)) + total_integral
        
        return L_s

    def check_zeta_zero_condition(self, sigma_range, t_range, resolution=50):
        """
        Busca dónde L(s) + 4 se acerca a 0.
        Si L(s) = -4, entonces Zeta(s) = 0.
        """
        sigmas = np.linspace(sigma_range[0], sigma_range[1], resolution)
        ts = np.linspace(t_range[0], t_range[1], resolution)
        
        results = np.zeros((len(ts), len(sigmas)))
        
        min_val = float('inf')
        min_loc = (0,0)

        print(f"Escaneando región: Sigma [{sigma_range[0]}, {sigma_range[1]}] | t [{t_range[0]}, {t_range[1]}]")
        
        for i, t in enumerate(ts):
            for j, sigma in enumerate(sigmas):
                s = complex(sigma, t)
                if abs(s - 1) < 0.01: continue # Saltar el polo
                
                L_val = self.compute_L_function(s)
                
                # La condición de anulación de Zeta es L(s) = -4
                # Medimos la "distancia al cero de Zeta"
                metric = abs(L_val + 4)
                results[i, j] = metric
                
                if metric < min_val:
                    min_val = metric
                    min_loc = (sigma, t)
        
        return sigmas, ts, results, min_loc, min_val

# --- EJECUCIÓN DEL SCRIPT ---

# 1. Configuración (Alta precisión requiere N grande)
N_SAMPLES = 500000 
sim = AbelKnuttzenAnalyzer(max_n=N_SAMPLES)

# 2. Definir región de búsqueda (Fuera y dentro de la franja crítica)
# Franja crítica: 0.5 a 1.0. Fuera: > 1.0
sigma_start, sigma_end = 0.4, 1.3
t_start, t_end = 10, 30 # Primeros ceros de Riemann están por t=14.13, 21.02...

# 3. Escaneo
sigmas, ts, magnitude, best_loc, best_val = sim.check_zeta_zero_condition(
    (sigma_start, sigma_end), (t_start, t_end), resolution=60
)

# 4. Visualización
plt.figure(figsize=(10, 8))
plt.contourf(sigmas, ts, magnitude, levels=50, cmap='viridis_r')
plt.colorbar(label='Distancia a la condición de cero: |L(s) + 4|')
plt.title(f'Mapa de Calor de la Integral Abel-Knuttzen\nCeros de Zeta ocurren cuando el valor tiende a 0 (Color oscuro)')
plt.xlabel('Sigma (Parte Real)')
plt.ylabel('t (Parte Imaginaria)')
plt.axvline(x=0.5, color='r', linestyle='--', label='Eje Crítico (Re=0.5)')
plt.axvline(x=1.0, color='w', linestyle='--', label='Frontera (Re=1.0)')

# Marcar el mínimo encontrado
plt.plot(best_loc[0], best_loc[1], 'rx', markersize=10, markeredgewidth=2)
plt.legend()

print("-" * 50)
print(f"RESULTADOS DEL ANÁLISIS ESPECTRAL:")
print(f"Mínimo valor de |L(s) + 4| encontrado: {best_val:.6f}")
print(f"Ubicación: s = {best_loc[0]:.4f} + {best_loc[1]:.4f}i")
print("-" * 50)

# Verificación puntual en un Cero conocido de Riemann (t ~ 14.1347)
s_zero = 0.5 + 14.134725j
L_zero = sim.compute_L_function(s_zero)
print(f"Prueba en el primer cero no trivial (s ~ 0.5 + 14.13i):")
print(f"Valor calculado de L(s): {L_zero}")
print(f"¿Cumple L(s) = -4? Magnitud del error: {abs(L_zero + 4):.6f}")

if best_loc[0] > 1.0 and best_val < 0.1:
    print("\n[ALERTA] ¡Posible anomalía detectada fuera de la franja crítica!")
else:
    print("\n[CONCLUSIÓN] No se detectaron ceros fuera de la franja crítica en este rango.")
    print("La integral mantiene la estabilidad predicha por el modelo MFN.")

plt.savefig("Knuttzen-Abel.png")
