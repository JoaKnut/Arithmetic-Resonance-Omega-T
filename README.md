# 🔱 Modelo Frecuencial de los Números (MFN) | v1.0.1
[![Status](https://img.shields.io/badge/Status-Anal%C3%ADtico%20y%20Heur%C3%ADstico-blue)](https://github.com/Knuttzen/MFN)

---

## 🧭 Overview del Proyecto

[cite_start]El **Modelo Frecuencial de los Números (MFN)** es un marco teórico que establece un **isomorfismo analítico** [cite: 6] [cite_start]entre la geometría de las subdivisiones de polígonos regulares y la teoría de divisores aritméticos [cite: 6, 7][cite_start], interpretando la distribución de los enteros no como una secuencia estática, sino como un sistema dinámico de **resonancia y disipación**[cite: 241].

El proyecto se estructura epistemológicamente en dos pilares:
1.  [cite_start]**Fundamentos Analíticos (Parte I):** Deducción rigurosa de identidades y propiedades de series de Dirichlet[cite: 8].
2.  [cite_start]**Modelos Heurísticos (Parte II):** Aplicación de estas identidades para modelar problemas abiertos bajo una dinámica espectral[cite: 240, 241].

### 🔑 Resultados Analíticos Clave (v1.0.1)

| Concepto | Identidad Rigurosa | Interpretación Física del Modelo |
| :--- | :--- | :--- |
| **Resonancia ($\Omega$)** | [cite_start]$\Omega(n) = d(2n) - 4$ [cite: 53] | [cite_start]Cuantificación exacta del "exceso de estructura" o divisores en el espacio duplicado $2n$[cite: 69, 43]. |
| **Semilla ($\Lambda_{MF}$)** | [cite_start]$L(s) = (2 - 2^{-s})\zeta(s) - 4$ [cite: 189] | [cite_start]La estructura atómica de $\Omega(n)$[cite: 177]. [cite_start]Es una señal determinista dependiente solo de la **paridad**, aislada mediante convolución de Dirichlet[cite: 179]. |
| **Impedancia ($\mathcal{K}_{MF}$)** | [cite_start]$(2 - 2^{-\mathcal{K}_{MF}})\zeta(\mathcal{K}_{MF}) = 4$ [cite: 297] | [cite_start]La **Constante de Equilibrio Espectral**[cite: 295]. [cite_start]Es el exponente crítico al cual el sistema se estabiliza, evitando la divergencia de la suma de resonancias[cite: 307]. |

---

## 🧮 Scripts de Simulación y Verificación

Este repositorio incluye algoritmos diseñados para validar empíricamente los teoremas y conjeturas del artículo. Los scripts demuestran la **coherencia estructural** entre el modelo dinámico y los resultados analíticos derivados.

| ID | Script | Propósito y Rigor Científico |
| :--- | :--- | :--- |
| **01** | `01_criba_resonancia.py` | **Verificación de la Equivalencia $\Omega(n)$ vs. $\Lambda_{MF}$**. [cite_start]<br> Implementa la convolución $\Omega = \Lambda_{MF} * 1$ [cite: 179] [cite_start]para reconstruir $\Omega(n)$ y verifica que sus ceros coincidan exactamente con los números primos y $n=4$[cite: 71, 76]. |
| **02** | `02_espectro_t.py` | **Análisis del Espectro de Resonancia $T(n)$**. [cite_start]<br> Valida la convergencia de la Resonancia Iterada a las constantes fundamentales derivadas teóricamente ($T(4) \to e$ y $T(p) \to \mathcal{T}_p$)[cite: 151, 137]. [cite_start]Confirma $T(n)$ como medida de la **entropía estructural**[cite: 173]. |
| **03** | `03_sismografo.py` | **Simulación de la Dinámica Espectral ($\Psi_E$)**. [cite_start]<br> Simula el proceso de carga/descarga de divisores[cite: 290, 293]. [cite_start]Compara la evolución temporal con el **Atractor Teórico** $\mathcal{K}_{MF} \ln(n)$ [cite: 304][cite_start], demostrando empíricamente la **regresión a la media** y el confinamiento dinámico del error[cite: 317]. |
| **04** | `04_abc_tension.py` | **Simulador de Tensión (Conjetura ABC)**. [cite_start]<br> Aplica la métrica de **Tensión Armónica Total** ($\Omega_{ABC}$) [cite: 274] [cite_start]a ternas coprimas, testeando la hipótesis de que las configuraciones de alta potencia colapsan obligatoriamente a estados de baja resonancia[cite: 280]. |
| **05** | `05_Knuttzen_Abel.py` | **Visualizador de la Condición de Balance Zeta (HR)**. <br> Herramienta interactiva que descompone la función Zeta en sus componentes Estructural ($S$) y Oscilatorio ($I_{osc}$) para verificar visualmente que $|I_{osc}| [cite_start]= |S|$ solo ocurre en la línea crítica[cite: 231, 233]. |

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
* [cite_start]**Formalización del Error $\epsilon_{dyn}$:** Aplicación de Teoremas de Perron y Tauberianos [cite: 327, 328] [cite_start]para acotar analíticamente el término de error del Sismógrafo[cite: 325].
* [cite_start]**Acoplamiento Espectral:** Investigación de la cuasi-identidad $\zeta(\mathcal{K}_{MF}) \approx T_p$ (99.85%) como evidencia de la fricción aritmética en modelos gaussianos de primos[cite: 174].
