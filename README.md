# 🔱 Modelo Frecuencial de los Números (MFN) | v1.2.0

[![Status](https://img.shields.io/badge/Status-Resoluci%C3%B3n%20Anal%C3%ADtica%20Determinista-blue)](https://github.com/Knuttzen/MFN)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18110601.svg)](https://doi.org/10.5281/zenodo.18110601)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## 🧭 Overview del Proyecto

El **Modelo Frecuencial de los Números (MFN)** es un marco teórico que establece un **isomorfismo analítico** entre la geometría de las subdivisiones de polígonos regulares y la teoría de divisores aritméticos. Interpreta la distribución de los enteros no como una secuencia estática, sino como un sistema dinámico **Input-to-State Stable (ISS)** regido por una impedancia fundamental $\mathcal{K}_{MF}$.

En la versión **v1.2.0**, el proyecto alcanza un hito crítico: la **Resolución Analítica del Conteo de Primos**. Se demuestra que la función $\pi(x)$ no es estocástica, sino la consecuencia determinista de una interferencia de onda cosenoidal amortiguada, permitiendo el cálculo de primos en magnitudes astronómicas en tiempo constante $O(1)$.

### 🔑 Nuevos Resultados Analíticos (v1.2.0)

| Concepto | Identidad / Cota | Interpretación Física del Modelo |
| :--- | :--- | :--- |
| **Ley de Proyección Cosenoidal** | $\pi_{MFN}(x) \approx Li(x) + \frac{\pi \mathcal{K}_{MF}}{\ln x} \int \frac{\cos(\pi t)}{t^{\mathcal{K}+1}} dt$ | **Resolución Asintótica**. La ubicación de los primos a gran escala es una onda suave determinista. Permite cálculo $O(1)$ mediante Gamma Incompleta. |
| **Corrección Discreta** | $\epsilon_{disc} = \sum R(k)(k^{-\mathcal{K}} - (k+1)^{-\mathcal{K}})$ | **Resolución Fina**. Recuperación exacta ("píxel a píxel") del conteo mediante suma de paridad $R(k)$, con error $<1$ en rangos medios. |
| **Impedancia $\mathcal{K}_{MF}$** | $\mathcal{K}_{MF} \approx 1.564498...$ | Constante fundamental de amortiguamiento del sistema, raíz de la ecuación de balance espectral de la semilla $\Lambda_{MF}$. |
| **Identidad de Acople** | $\epsilon_{dyn}(n) \sim -\frac{1}{2\pi} \ln(n) (\pi(n) - Li(n))$ | Vinculación mecánica directa entre el error del sismógrafo y el error en el conteo de primos. |

---

## 🧮 Scripts de Simulación y Verificación

El repositorio incluye 7 algoritmos diseñados para validar empíricamente los teoremas y cotas del artículo.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_espectro_t.py` | **Análisis del Espectro $T(n)$**.<br> Valida la convergencia a las constantes fundamentales ($T(4) \to e$, $T(p) \to \mathcal{T}_p$). |
| **02** | `02_sismografo.py` | **Simulador Dinámico**.<br> Ejecuta la dinámica de carga/descarga de energía $\Psi_E$ para verificar la estabilidad ISS del sistema. |
| **03** | `03_contador_primos.py` | **Calculadora Espectral Unificada**.<br> Implementa las fórmulas analíticas deterministas (v1.2.0). Permite calcular $\pi(x)$ con precisión arbitraria mediante modos discretos (`--exactly`) para corrección fina o integrales cosenoidales (`--aprox`) para magnitudes astronómicas, superando la estimación por cotas. |
| **04** | `04_abc_tension.py` | **Simulador de Tensión (ABC)**.<br> Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) a ternas coprimas para testear el colapso espectral. |
| **05** | `05_zeta_approx.py` | **Aproximación de Riemann**.<br> Calcula $\zeta(s)$ para $\text{Re}(s)>1$ usando la **Linealización Estructural** (Teorema 6.7), separando el esqueleto algebraico de la corrección de onda integral. |
| **06** | `06_Knuttzen_Abel_Integral.py` | **Visualizador de Balance**.<br> Descomposición visual interactiva de $\zeta(s)$ en componentes Estructural ($S$) y Oscilatorio ($I_{osc}$) en el plano complejo. |
| **07** | `07_Generador_Imagen_Omega.py` | **Utilería Gráfica**.<br> Generación de renderizados de alta resolución para la función de resonancia y la dinámica del sismógrafo. |

---

## 📄 Citación

Si utilizas algún concepto desarrollado en el repositorio, cita el trabajo original:

> Knuttzen, J. (2025). *Resonancia Geométrica en los Enteros: Una derivación armónica de la función divisor y su dinámica espectral*. DOI: 10.5281/zenodo.18110601

---

## 🎯 Roadmap (v1.3.0 - Próximos Pasos)

Con la resolución analítica completada, el foco se desplaza hacia las implicaciones físicas y computacionales:

1. **Termodinámica Computacional:** Investigar la aplicación de la "economía de resonancia" para optimización de computación reversible (Límite de Landauer).
2. **Seguridad Espectral:** Análisis de vulnerabilidad en criptografía RSA mediante detección de clase espectral ($\nabla=4$) usando la fórmula de energía analítica (Side-channel matemático).
3. **Formalización de la HR:** Vincular la estabilidad de la integral cosenoidal con la ausencia de ceros de Siegel.
