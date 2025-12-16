import numpy as np
import matplotlib.pyplot as plt

class KnuttzenDecoder:
    def __init__(self):
        # Definición de la Paleta Humana Estándar (K-STD)
        # Mapea Pendiente (d(i)) -> Matiz Base (RGB Normalizado)
        self.palette = {
            1: [1.0, 1.0, 1.0],  # Pendiente 1: Estructura/Neutro (Blanco)
            2: [0.0, 0.8, 1.0],  # Pendiente 2: Primos/Fundamental (Cian/Azul)
            3: [1.0, 0.0, 0.3],  # Pendiente 3: Cuadrados/Singularidad (Rojo/Magenta)
            4: [1.0, 0.8, 0.0],  # Pendiente 4+: Compuestos/Denso (Amarillo/Oro)
        }

    def _get_odd_seed(self, n):
        """Extrae la semilla impar 'i' de n = i * 2^k."""
        if n == 0: return 0
        while n % 2 == 0:
            n //= 2
        return n

    def _get_slope_nabla(self, n):
        """
        Calcula la Pendiente Estructural Rigurosa: Nabla = d(i).
        Esta es la constante física de la familia.
        """
        i_seed = self._get_odd_seed(n)
        if i_seed == 1: return 1
        
        divisors = 0
        limit = int(np.sqrt(i_seed))
        for k in range(1, limit + 1):
            if i_seed % k == 0:
                divisors += 2 if k*k != i_seed else 1
        return divisors

    def _calculate_intensity(self, n, slope):
        """
        Calcula la Intensidad basada en la 'Fricción con el Campo'.
        Identidad General: Omega = (k+2)*slope - 4.
        A mayor Omega, menor T(n) (más oscuro).
        """
        # Calcular k (Profundidad de iteración)
        k = 0
        temp = n
        while temp > 0 and temp % 2 == 0:
            temp //= 2
            k += 1
            
        # Resonancia Total (Masa Estructural)
        omega = (k + 2) * slope - 4
        
        # Modelo de Decaimiento de Señal (Simulación de T(n))
        # La señal decae hiperbólicamente con la resistencia del campo.
        # Factor 0.08 calibrado para rango dinámico visual.
        intensity = 1.0 / (1.0 + 0.08 * omega)
        return np.clip(intensity, 0, 1)

    def decode(self, artifact_matrix):
        """Procesa la matriz de enteros y devuelve imagen RGB."""
        height, width = artifact_matrix.shape
        img_rgb = np.zeros((height, width, 3))

        print(f"Decodificando Artefacto de {width}x{height}...")

        for y in range(height):
            for x in range(width):
                n = artifact_matrix[y, x]
                
                # 1. Determinación de Clase (¿QUÉ ES?)
                slope = self._get_slope_nabla(n)
                
                # 2. Determinación de Estado (¿CÓMO ESTÁ?)
                intensity = self._calculate_intensity(n, slope)
                
                # 3. Mapeo a Interfaz Humana
                # Si la pendiente es > 4, la tratamos como clase 4 (Compuesta densa)
                palette_key = slope if slope <= 3 else 4
                base_color = np.array(self.palette[palette_key])
                
                # Síntesis del Píxel: Color Base * Intensidad
                final_pixel = base_color * intensity
                img_rgb[y, x] = final_pixel

        return img_rgb

# --- GENERACIÓN DE ARTEFACTO DE PRUEBA (SIMULACIÓN DE ARCHIVO .KNT) ---
# Creamos una imagen sintética de 100x100
# Fondo: Pendiente 1 (Cielo/Vacío)
# Planeta: Pendiente 2 (Primos/Materia Pura)
# Núcleo: Pendiente 3 (Cuadrados/Energía)
# Anillos: Pendiente 4 (Compuestos/Polvo)

artifact = np.zeros((100, 100), dtype=object)
center_x, center_y = 50, 50

for y in range(100):
    for x in range(100):
        dx, dy = x - center_x, y - center_y
        dist = np.sqrt(dx**2 + dy**2)
        
        # Lógica de construcción del archivo (Encoder implícito)
        # La 'k' (potencia de 2) simula sombras/profundidad
        k_shadow = int(dist / 5) 
        
        if dist < 10: 
            # Núcleo (Rojo/Cuadrados) -> i = 9 (3^2)
            n = 9 * (2 ** (k_shadow // 2)) # Menos sombra, núcleo brillante
        elif dist < 30:
            # Planeta (Azul/Primos) -> i = 3
            n = 3 * (2 ** k_shadow)
        elif 35 < dist < 45:
            # Anillos (Dorado/Compuestos) -> i = 15
            n = 15 * (2 ** k_shadow)
        else:
            # Espacio (Gris/Neutro) -> i = 1
            n = 1 * (2 ** (k_shadow + 2)) # Fondo más oscuro
            
        artifact[y, x] = int(n)

# --- EJECUCIÓN ---
decoder = KnuttzenDecoder()
imagen_recuperada = decoder.decode(artifact)

plt.figure(figsize=(8, 8))
plt.imshow(imagen_recuperada)
plt.title("Visualización del Decodificador Espectral de Knuttzen\n(Datos generados puramente por estructura aritmética)")
plt.axis('off')
plt.show()
