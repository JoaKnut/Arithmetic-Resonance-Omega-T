# 🔱 Modelo Frecuencial de los Números (MFN) | v1.3.0

[![Status](https://img.shields.io/badge/Status-Resoluci%C3%B3n%20Anal%C3%ADtica%20Determinista-blue)](https://github.com/Knuttzen/MFN)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18124255.svg)](https://doi.org/10.5281/zenodo.18124255)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## 🧭 Overview del Proyecto

El **Modelo Frecuencial de los Números (MFN)** es un marco teórico que establece un **isomorfismo analítico** entre la geometría de las subdivisiones de polígonos regulares y la teoría de divisores. En la versión **v1.3.0**, el modelo trasciende la descripción asintótica para alcanzar la **Génesis de la Paridad**. 

Se demuestra que los números primos y perfectos no son entidades estocásticas, sino "nudos espectrales" necesarios e inevitables resultantes de la vibración de la paridad sobre la recta numérica.

### 🔑 Hitos de la Desmitificación (v1.3.0)

| Concepto | Identidad / Cota | Significado Ontológico |
| :--- | :--- | :--- |
| **Inversión Espectral de Möbius** | $\pi(x) = \sum_{k=1}^{\lfloor \log_2 x \rfloor} \frac{\mu(k)}{k} J_{MFN}(x^{1/k})$ | **Resolución Aritmética Exacta**. Reconstrucción determinista del conteo de primos mediante el filtrado de armónicos del potencial resonante $J_{MFN}$, eliminando la necesidad de términos de error probabilísticos. || **Impedancia $\mathcal{K}_{MF}$** | $\mathcal{K}_{MF} \approx 1.564498...$ | Constante fundamental de amortiguamiento del sistema, raíz de la ecuación de balance espectral de la semilla $\Lambda_{MF}$. |
| **Identidad de Acople** | $\epsilon_{dyn}(n) \sim -\frac{1}{2\pi} \ln(n) (\pi(n) - Li(n))$ | Vinculación mecánica directa entre el error del sismógrafo y el error en el conteo de primos. |
| **Génesis de la Semilla** | $\Lambda_{MF} * \alpha = \alpha \cdot \ln$ | La información de la primalidad nace de la paridad ($\alpha$). Los primos son consecuencias deterministas de la estructura binaria. |
| **Resolución de $\pi(x)$** | $\pi(x) = \sum \frac{\mu(k)}{k} J_{MFN}(x^{1/k})$ | **Determinismo Total**. El conteo de primos se sintetiza desde la semilla, eliminando el azar del modelo de Cramér. |
| **Filtro de Mersenne** | $P(x) = \sum \delta_{\epsilon}(\Lambda_{MF}(M_p) - \ln M_p)$ | **Resolución de la Perfección**. Función contadora exacta para números perfectos basada en resonancia de fase, no en búsqueda de divisores. |

---

## 🧮 Scripts de Simulación y Verificación

El repositorio incluye 8 algoritmos diseñados para validar empíricamente la rigidez del universo aritmético.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_espectro_t.py` | **Análisis del Espectro $T(n)$**.<br> Valida la convergencia a las constantes fundamentales ($T(4) \to e$, $T(p) \to \mathcal{T}_p$). |
| **02** | `02_sismografo.py` | **Simulador Dinámico**.<br> Ejecuta la dinámica de carga/descarga de energía $\Psi_E$ para verificar la estabilidad ISS del sistema. |
| **03** | `03_contador_primos.py` | **Calculadora Espectral Unificada**.<br> Implementa las fórmulas analíticas deterministas (v1.2.0). Permite calcular $\pi(x)$ con precisión arbitraria mediante modos discretos. |
| **04** | `04_abc_tension.py` | **Simulador de Tensión (ABC)**.<br> Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) a ternas coprimas para testear el colapso espectral. |
| **05** | `05_zeta_approx.py` | **Aproximación de Riemann**.<br> Calcula $\zeta(s)$ para $\text{Re}(s)>1$ usando la **Linealización Estructural** (Teorema 6.7), separando el esqueleto algebraico de la corrección de onda integral. |
| **06** | `06_Knuttzen_Abel_Integral.py` | **Visualizador de Balance**.<br> Descomposición visual interactiva de $\zeta(s)$ en componentes Estructural ($S$) y Oscilatorio ($I_{osc}$) en el plano complejo. |
| **07** | `07_Generador_Imagen_Omega.py` | **Utilería Gráfica**.<br> Generación de renderizados de alta resolución para la función de resonancia y la dinámica del sismógrafo. |
| **01** | `01_espectro_t.py` | **Análisis del Espectro $T(n)$**.<br> Valida la convergencia a constantes fundamentales ($T(4) \to e$, $T(p) \to \mathcal{T}_p$). |
| **02** | `02_sismografo.py` | **Simulador Dinámico**.<br> Verifica la estabilidad ISS del sistema de carga/descarga de energía $\Psi_E$. |
| **03** | `03_contador_primos.py` | **Calculadora Espectral Unificada**.<br> Implementa el conteo exacto de $\pi(x)$ mediante la inversión de Möbius de la semilla. |
| **04** | `04_contador_perfectos.py` | **Detector de Resonancia de Mersenne**.<br> Calcula $P(x)$ detectando "ecos" de paridad en índices de Mersenne. |
| **05** | `05_abc_tension.py` | **Simulador de Tensión (ABC)**.<br> Testea el colapso espectral en la suma de estructuras ricas. |
| **06** | `06_zeta_approx.py` | **Aproximación de Riemann**.<br> Separa el esqueleto algebraico de $\zeta(s)$ de su corrección de onda integral. |
| **07** | `07_Knuttzen_Abel_Integral.py` | **Visualizador de Balance**.<br> Descomposición interactiva de $\zeta(s)$ en componentes $S$ e $I_{osc}$. |
| **08** | `08_Generador_Imagen_Omega.py` | **Utilería Gráfica**.<br> Renderizados de la función de resonancia y la dinámica del sismógrafo. |

---

## 📄 Citación

Si utilizas algún concepto desarrollado en el repositorio, cita el trabajo original:

> Knuttzen, J. (2025). *Resonancia Geométrica en los Enteros: Una derivación armónica de la función divisor y su dinámica espectral*. DOI: 10.5281/zenodo.18124255

---

## 🎯 Roadmap (v1.4.0 - Siguiente Fase)

1. **Formalización de la HR:** Vincular la estabilidad de la integral de paridad con la ausencia de ceros de Siegel.
2. **Termodinámica de la Información:** Aplicar $C_{Perf}$ para la prueba definitiva de la inexistencia de perfectos impares.
3. **Criptografía de Paridad:** Desarrollo de protocolos de verificación instantánea mediante firma espectral.
