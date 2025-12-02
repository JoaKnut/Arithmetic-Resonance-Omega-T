# 🔱 Modelo Frecuencial de los Números (MFN) | v1.0.1
[![Status](https://img.shields.io/badge/Status-Anal%C3%ADtico%20y%20Heur%C3%ADstico-blue)](https://github.com/Knuttzen/MFN)

---

## 🧭 Overview del Proyecto

El **Modelo Frecuencial de los Números (MFN)** es un marco teórico que establece un **isomorfismo analítico** entre la geometría de las subdivisiones de polígonos regulares y la teoría de divisores aritméticos, interpretando la distribución de los enteros no como una secuencia estática, sino como un sistema dinámico de **resonancia y disipación**.

El proyecto se estructura epistemológicamente en dos pilares:
1. **Fundamentos Analíticos (Parte I):** Deducción rigurosa de identidades y propiedades de series de Dirichlet.
2. **Modelos Heurísticos (Parte II):** Aplicación de estas identidades para modelar problemas abiertos bajo una dinámica espectral.

### 🔑 Resultados Analíticos Clave (v1.0.1)

| Concepto | Identidad Rigurosa | Interpretación Física del Modelo |
| :--- | :--- | :--- |
| **Resonancia ($\Omega$)** | $\Omega(n) = d(2n) - 4$ | Cuantificación exacta del "exceso de estructura" o divisores en el espacio duplicado $2n$. |
| **Semilla ($\Lambda_{MF}$)** | $L(s) = (2 - 2^{-s})\zeta(s) - 4$ | La estructura atómica de $\Omega(n)$. Es una señal determinista dependiente solo de la **paridad**, aislada mediante convolución de Dirichlet. |
| **Impedancia ($\mathcal{K}_{MF}$)** | $(2 - 2^{K_{MF}})\zeta(K_{MF}) = 4$ | La **Constante de Equilibrio Espectral**. Es el exponente crítico al cual el sistema se estabiliza, evitando la divergencia de la suma de resonancias. |

---

## 🧮 Scripts de Simulación y Verificación

Este repositorio incluye algoritmos diseñados para validar empíricamente los teoremas y conjeturas del artículo. Los scripts demuestran la **coherencia estructural** entre el modelo dinámico y los resultados analíticos derivados.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_criba_resonancia.py` | **Verificación de la Equivalencia $\Omega(n)$ vs. $\Lambda_{MF}$**.<br> Implementa la convolución $\Omega = \Lambda_{MF} * 1$ para reconstruir $\Omega(n)$ y verifica que sus ceros coincidan exactamente con los números primos y con $n=4$. |
| **02** | `02_espectro_t.py` | **Análisis del Espectro de Resonancia $T(n)$**.<br> Valida la convergencia de la Resonancia Iterada a las constantes fundamentales derivadas teóricamente ($T(4) \to e$ y $T(p) \to \mathcal{T}_p$). Confirma $T(n)$ como medida de la **entropía estructural**. |
| **03** | `03_sismografo.py` | **Simulación de la Dinámica Espectral ($\Psi_E$)**.<br> Simula el proceso de carga/descarga de divisores. Compara la evolución temporal con el **Atractor Teórico** $\mathcal{K}_{MF} \ln(n)$, demostrando empíricamente la **regresión a la media** y el confinamiento dinámico del error. |
| **04** | `04_abc_tension.py` | **Simulador de Tensión (Conjetura ABC)**.<br> Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) a ternas coprimas, testeando la hipótesis de que las configuraciones de alta potencia colapsan obligatoriamente a estados de baja resonancia. |
| **05** | `05_Knuttzen_Abel.py` | **Visualizador de la Condición de Balance Zeta (HR)**.<br> Herramienta interactiva que descompone la función Zeta en sus componentes Estructural ($S$) y Oscilatorio ($I_{osc}$) para verificar visualmente que $|I_{osc}| = |S|$ solo ocurre en la línea crítica. |

---

## 📄 Citación y Licencia

Este trabajo está registrado y disponible para citación inmediata. Si utilizas las ecuaciones, el código o el marco teórico del MFN, por favor, **cita la versión con DOI**.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17674007.svg)](https://doi.org/10.5281/zenodo.17674007)

**Licencia:**  
Este repositorio y su contenido están bajo la licencia **CC BY 4.0** (Creative Commons Attribution 4.0).

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## 🎯 Roadmap (v1.1.0)

La investigación activa se centra actualmente en:
* **Formalización del Criterio de Estabilidad Dinámica (HR):** Demostrar la **desigualdad estricta**, $|I_{osc}(s) < S(s)|$ para $\sigma > 1/2$. Esto requiere una acotación analítica rigurosa de la integral oscilatoria $I_{osc}(s)$ para probar que su amplitud es insuficiente para romper el equilibrio fuera de la línea crítica.
* **Formalización del Error $\epsilon_{dyn}$:** Aplicación de Teoremas de Perron y Tauberianos para acotar analíticamente el término de error del Sismógrafo.
* **Acoplamiento Espectral:** Investigación de la cuasi-identidad $\zeta(\mathcal{K}_{MF}) \approx T_p$ (99.85%) como evidencia de la fricción aritmética en modelos gaussianos de primos.
