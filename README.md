# 🌟 Marco de Resonancia Aritmética ($\Omega(n)$ y $T(n)$)

Este repositorio contiene la teoría, el código de simulación y el código fuente LaTeX del artículo **"Resonancia Aritmética: Un marco unificado para la primalidad, la Conjetura ABC y la Hipótesis de Riemann"**.

El trabajo propone un nuevo marco para la Teoría de Números basado en la función elemental $\Omega(n)$=d(2n)-4, extendiéndolo a un modelo dinámico ($\Psi(n)$) para estudiar el equilibrio estructural de los enteros.

---

## 🔬 Componentes del Proyecto

### 1. Funciones de Resonancia

* **$\Omega(n)$ (Tensión Armónica):** Caracteriza la primalidad ($\Omega(n)=0$ si $n$ es primo o $n=4$). Utilizada para proponer una nueva formulación de la **Conjetura ABC** (Sección 7).
* **$T(n)$ (Resonancia de Fondo):** Una función iterada que revela constantes fundamentales, incluyendo $T(4)=e$, una constante $\mathcal{T}_p$ para primos, y la **Constante de Amortiguamiento Perfecto** $C_{Perf} \approx 0.864$.
* **$\Psi(n)$ (Sismógrafo Dinámico):** Un modelo recursivo cuya desviación de su tendencia logarítmica es postulada como equivalente a la **Hipótesis de Riemann** (Sección 9).

### 2. Estructura del Repositorio

| Carpeta | Contenido | Propósito |
| :--- | :--- | :--- |
| **`Article/`** | Código fuente en LaTeX (`.tex`) y la versión final en PDF. | Contiene la prueba formal y las demostraciones. |
| **`Code/`** | Scripts en Python utilizados para el cálculo de $T(n)$, $C_{Perf}$ y la simulación de $\Psi_E(n)$. | Permite la reproducibilidad de los resultados numéricos y gráficos. |
| **`Figures/`** | Imágenes de las simulaciones y espectros utilizados en el artículo. | Resultados visuales generados por el código. |

---

## 🔗 Citas y Estado del Preprint

Este trabajo está registrado y disponible para citación inmediata:

[* **DOI (Zenodo):** https://doi.org/10.5281/zenodo.8475

Este repositorio está bajo la licencia **CC BY 4.0** (Creative Commons Attribution 4.0). Si utilizas este trabajo, por favor, cita la versión con DOI o el preprint de arXiv.
