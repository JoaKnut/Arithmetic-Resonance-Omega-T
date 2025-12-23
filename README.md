# 🔱 Modelo Frecuencial de los Números (MFN) | v1.1.0

[![Status](https://img.shields.io/badge/Status-Cota%20Din%C3%A1mica%20Probada-success)](https://github.com/Knuttzen/MFN)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17674007.svg)](https://doi.org/10.5281/zenodo.17674007)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## 🧭 Overview del Proyecto

El **Modelo Frecuencial de los Números (MFN)** es un marco teórico que establece un **isomorfismo analítico** entre la geometría de las subdivisiones de polígonos regulares y la teoría de divisores aritméticos. Interpreta la distribución de los enteros no como una secuencia estática, sino como un sistema dinámico **Input-to-State Stable (ISS)**.

En la versión **v1.1.0**, el proyecto avanza desde la heurística hacia la formalización de cotas, incorporando la **Cota BHP (Baker-Harman-Pintz)** para demostrar que la energía del error dinámico está estrictamente acotada por $O(n^{0.525})$.

### 🔑 Nuevos Resultados Analíticos (v1.1.0)

| Concepto | Identidad / Cota | Interpretación Física del Modelo |
| :--- | :--- | :--- |
| **Resonancia ($\Omega$)** | $\Omega(n) = d(2n) - 4$ | Cuantificación exacta del "exceso de estructura" en el espacio duplicado. |
| **Identidad de Acople** | $\epsilon_{dyn}(n) \sim -\frac{1}{2\pi} \ln(n) (\pi(n) - Li(n))$ | Vinculación mecánica directa entre el error del sismógrafo y el error en el conteo de primos. |
| **Estabilidad (ISS)** | $\epsilon_{dyn}(n) \ll O(n^{0.525})$ | **Teorema de Estabilidad Mecánica**. Demostración de que el sistema no diverge, imponiendo un "muro duro" al error de Riemann en $\sigma = 0.525$. |
| **Semilla ($\Lambda_{MF}$)** | $L(s) = (2 - 2^{-s})\zeta(s) - 4$ | Estructura atómica determinista aislada mediante convolución de Dirichlet. |

---

## 🧮 Scripts de Simulación y Verificación

El repositorio incluye 7 algoritmos diseñados para validar empíricamente los teoremas y cotas del artículo.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_espectro_t.py` | **Análisis del Espectro $T(n)$**.<br> Valida la convergencia a las constantes fundamentales ($T(4) \to e$, $T(p) \to \mathcal{T}_p$). |
| **02** | `02_sismografo.py` | **Simulador Dinámico**.<br> Ejecuta la dinámica de carga/descarga de energía $\Psi_E$ para verificar la estabilidad ISS del sistema. |
| **03** | `03_contador_primos.py` | **Recuperación de $\pi(x)$**.<br> Cálculo de la función contadora utilizando la cota de error del sismógrafo del autor (O($n^{0.525}$)), logrando una estimación con **error menor al 0.3%** respecto al valor real. |
| **04** | `04_abc_tension.py` | **Simulador de Tensión (ABC)**.<br> Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) a ternas coprimas para testear el colapso espectral. |
| **05** | `05_zeta_approx.py` | **Aproximación de Riemann**.<br> Calcula $\zeta(s)$ para $\text{Re}(s)>1$ usando la **Linealización Estructural** (Teorema 6.7), separando el esqueleto algebraico de la corrección de onda integral. |
| **06** | `06_Knuttzen_Abel_Integral.py` | **Visualizador de Balance**.<br> Descomposición visual interactiva de $\zeta(s)$ en componentes Estructural ($S$) y Oscilatorio ($I_{osc}$) en el plano complejo. |
| **07** | `07_Generador_Imagen_Omega.py` | **Utilería Gráfica**.<br> Generación de renderizados de alta resolución para la función de resonancia y la dinámica del sismógrafo. |

---

## 📄 Citación

Si utilizas algún concepto desarrollado en el repositorio, cita el trabajo original:

> Knuttzen, J. (2025). *Resonancia Geométrica en los Enteros: Una derivación armónica de la función divisor y su dinámica espectral*. DOI: 10.5281/zenodo.17674007

---

## 🎯 Roadmap (v1.2.0 - Próximos Pasos)

El foco actual es reducir la cota probada desde el "Muro BHP" hacia la línea crítica:

1. **Refinamiento de la Cota:** Investigar si la propiedad de **autocorrelación negativa** de la Semilla $\Lambda_{MF}$ permite mejorar la cota de entrada del sismógrafo de $n^{0.525}$ a $n^{0.5+\epsilon}$.
2. **Análisis de Fricción:** Formalizar el "costo energético" $C_{Perf}$ como un límite termodinámico de Landauer.
