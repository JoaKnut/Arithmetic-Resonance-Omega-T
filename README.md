# 🔱 Modelo Frecuencial de los Números (MFN) | v1.0.1

[![Status](https://img.shields.io/badge/Status-Anal%C3%ADtico%20y%20Heur%C3%ADstico-blue)](https://github.com/Knuttzen/MFN)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🧭 Overview del Proyecto

El Modelo Frecuencial de los Números (MFN) es un marco teórico que establece un **isomorfismo analítico** entre la geometría de las subdivisiones de polígonos y la teoría de divisores, interpretando la distribución de los enteros no como una secuencia estática, sino como un sistema dinámico regido por la **resonancia**.

El proyecto se estructura en dos pilares:
1.  **Fundamentos Analíticos (Parte I):** Deducción rigurosa de las identidades.
2.  **Modelos Heurísticos (Parte II):** Aplicación de las identidades para simular problemas abiertos (Riemann, ABC).

### 🔑 Resultados Analíticos Clave (Sección 6 & 9)

| Concepto | Identidad Rigurosa | Interpretación |
| :--- | :--- | :--- |
| **Resonancia ($\Omega$)** | $\Omega(n) = d(2n) - 4$ | Cuantificación del exceso de divisores en el espacio $2n$. |
| **Semilla ($\Lambda_{MF}$)** | $L(s) = (2 - 2^{-s})\zeta(s) - 4$ | La estructura elemental de $\Omega(n)$, determinada solo por la **paridad** de $n$. |
| **Impedancia ($\mathcal{K}_{MF}$)** | $(2 - 2^{-\mathcal{K}_{MF}})\zeta(\mathcal{K}_{MF}) = 4$ | La **Constante de Equilibrio Espectral**. El exponente al que el sistema se mantiene en un estado de **no-divergencia**. |

---

## 🧮 Scripts de Simulación y Verificación

Los scripts en este repositorio están diseñados para validar empíricamente los teoremas y las conjeturas del artículo, demostrando la **coherencia estructural** del modelo dinámico con los resultados analíticos.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_criba_resonancia.py` | **Cálculo de $\pi(N)$ basado en la Semilla.** Implementa la fórmula de $\pi(N)$ utilizando la **Convolución de Dirichlet** de la semilla $\Lambda_{MF}$. Prueba la validez conceptual de la Semilla como base para un contador de primos. |
| **02** | `02_espectro_t.py` | **Análisis del Espectro de Resonancia $T(n)$.** Valida la convergencia a las constantes fundamentales ($T(4) \to e$ y $T(p) \to \mathcal{T}_p$). Confirma que la función $T(n)$ es una medida precisa de la **entropía estructural** del entero. |
| **03** | `03_sismografo.py` | **Simulación de la Dinámica Espectral.** Simula el proceso de carga/descarga $\Psi_E(n)$. Compara el camino dinámico con el **Atractor Teórico** $\mathcal{K}_{MF} \ln(n)$ para demostrar empíricamente la **regresión a la media** y el confinamiento del error. |
| **04** | `04_contador_pi.py` | **Contador de Primos (Referencia).** Implementación del contador $\pi(N) = \lfloor \sum N^{-\Omega(n)} \rfloor$ (Sección 4). Útil como herramienta de referencia, aunque es computacionalmente ineficiente. |
| **05** | `05_abc_tension.py` | **Simulador de Tensión en la Conjetura ABC.** Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) a las ternas, probando la conjetura heurística de que las ternas con alto contenido de potencias colapsan a estados de baja resonancia. |

---

## 🎯 Futuras Vías de Investigación (v1.1.0)

La próxima *release* se enfocará en el rigor de la Parte II:

* **Formalización del Error $\epsilon_{dyn}$:** Uso de los Teoremas de Perron y Tauberianos para acotar rigurosamente el término de error del Sismógrafo.
* **Cuantificación de la Coherencia:** Análisis del **Acoplamiento Espectral** entre $\zeta(\mathcal{K}_{MF})$ y $T_p$ para investigar la cuasi-identidad ($\approx 99.8\%$).
