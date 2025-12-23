import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# --- MOTOR MATEMÁTICO (Basado en Knuttzen, Sec 6) ---

def calcular_estructura(sigma, t):
    """
    Calcula el término estructural S(s).
    Ref: Teorema 6.4
    """
    s = complex(sigma, t)
    # S(s) = 2 + 1.5 * 2^(-s) * ((s+1)/(s-1))
    term = 2 + 1.5 * (2**(-s)) * ((s + 1) / (s - 1))
    return term

def calcular_oscilacion(sigma, t, n_terms=50000):
    """
    Calcula la integral oscilatoria I_osc(s) usando series vectorizadas.
    Ref: Teorema 6.6
    La integral de R(x) se convierte en una suma alternada de diferencias de potencias.
    """
    s = complex(sigma, t)
    
    # Vectorización para velocidad (Cálculo instantáneo de 50k términos)
    k = np.arange(2, n_terms + 2)
    
    # R(x) alterna signo: -0.5, 0.5, -0.5... comenzando en k=2
    # El coeficiente es 0.5 * (-1)^(k-1)
    signs = 0.5 * ((-1.0)**(k - 1))
    
    # Integral analítica por tramos: (k^-s - (k+1)^-s)
    # Nota: El factor 's' de la integral se cancela con el denominador de la integración
    diffs = (k**(-s)) - ((k + 1)**(-s))
    
    # Suma total
    val = np.sum(signs * diffs)
    
    # Ajuste fino: I_osc debe oponerse a S(s). 
    # En la identidad (S + I = 0), I = -S. Graficamos I tal cual sale de la fórmula.
    return val

# --- INTERFAZ GRÁFICA ---

fig = plt.figure(figsize=(12, 6))
fig.suptitle('Simulador de Resonancia de Knuttzen (Balance de Energía)', fontsize=14)

# Configuración de los subgráficos
ax_polar = fig.add_subplot(1, 2, 1) # Plano Complejo
ax_bar = fig.add_subplot(1, 2, 2)   # Barras de Energía

# Espacio para controles sliders
plt.subplots_adjust(bottom=0.25)

# --- VALORES INICIALES (Primer Cero de Riemann) ---
init_sigma = 0.5
init_t = 14.1347

# --- FUNCIÓN DE DIBUJO ---
def update(val):
    sigma = s_sigma.val
    t = s_t.val
    
    # 1. Cálculos
    S_val = calcular_estructura(sigma, t)
    I_val = calcular_oscilacion(sigma, t)
    
    # 2. Plot Polar (Vectores)
    ax_polar.clear()
    ax_polar.set_title(f"Plano Complejo (s = {sigma:.2f} + {t:.2f}i)")
    
    # Vector Azul: Estructura (S)
    ax_polar.arrow(0, 0, S_val.real, S_val.imag, head_width=0.05, head_length=0.1, fc='blue', ec='blue', label='Estructura (Barrera)')
    
    # Vector Rojo: Oscilación (I_osc)
    # IMPORTANTE: Para que haya balance cero, S + I = 0, por lo tanto I debe llegar al origen partiendo de S
    # O visualmente: S y -I deben ser iguales. 
    # Graficamos I_osc desde el origen para comparar magnitudes y fases.
    ax_polar.arrow(0, 0, I_val.real, I_val.imag, head_width=0.05, head_length=0.1, fc='red', ec='red', label='Oscilación (I_osc)')
    
    # Círculo de referencia unitario y límites
    limit = 2.5
    ax_polar.set_xlim(-limit, limit)
    ax_polar.set_ylim(-limit, limit)
    ax_polar.grid(True)
    ax_polar.legend(loc='upper right')
    ax_polar.axhline(0, color='black', lw=0.5)
    ax_polar.axvline(0, color='black', lw=0.5)

    # 3. Plot Barras (Energía/Magnitud)
    ax_bar.clear()
    ax_bar.set_title("Comparación de Magnitud (Energía)")
    
    mag_S = abs(S_val)
    mag_I = abs(I_val)
    
    bars = ax_bar.bar(['Estructura |S|', 'Oscilación |I|'], [mag_S, mag_I], color=['blue', 'red'])
    ax_bar.set_ylim(0, 2.5)
    
    # Etiquetas de valor
    ax_bar.text(0, mag_S + 0.05, f"{mag_S:.4f}", ha='center', color='blue', fontweight='bold')
    ax_bar.text(1, mag_I + 0.05, f"{mag_I:.4f}", ha='center', color='red', fontweight='bold')
    
    # Indicador de Desigualdad
    if mag_S > mag_I + 0.01: # Margen de tolerancia
        status = "ESTABLE (HR Compatible)\nLa oscilación NO alcanza la barrera."
        col = "green"
    elif abs(mag_S - mag_I) < 0.05:
        status = "RESONANCIA (Cero Posible)\nEnergías igualadas."
        col = "orange"
    else:
        status = "INESTABLE (Contraejemplo)\nLa oscilación rompe la barrera."
        col = "red"
        
    ax_bar.text(0.5, 2.0, status, ha='center', bbox=dict(facecolor='white', edgecolor=col, boxstyle='round'))

# --- CONTROLES (SLIDERS) ---
# Eje Sigma (Parte Real)
ax_sigma = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
s_sigma = Slider(ax_sigma, 'Sigma (σ)', 0.4, 1.0, valinit=init_sigma, valstep=0.01)

# Eje T (Parte Imaginaria - Altura)
ax_t = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
s_t = Slider(ax_t, 'Tiempo (t)', 10.0, 20.0, valinit=init_t)

# Conectar actualización
s_sigma.on_changed(update)
s_t.on_changed(update)

# Botón de Reset al Cero de Riemann
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Ir al Cero', hovercolor='0.975')

def reset(event):
    s_sigma.set_val(0.5)
    s_t.set_val(14.1347)
button.on_clicked(reset)

# Inicializar
update(None)
plt.show()
