/**
 * KM_DeepProbe: Análisis Asintótico del Modelo Knuttzen hasta 10^20
 * Compilar con: g++ -O3 -fopenmp KM_DeepProbe.cpp -o KM_probe
 * Requiere sistema de 64 bits (GCC/Clang) para soporte __int128
 * Compilar: g++ KM_DeepProbe.cpp -o KM_probe -std=c++17 -O3 -march=native -fopenmp -Wall 
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>
#include <iomanip>
#include <random>
#include <omp.h>
#include <algorithm>

// --- CONFIGURACIÓN ---
// Usamos __int128 para soportar hasta 10^38.
typedef unsigned __int128 u128;
typedef unsigned long long u64;

// Constantes del Modelo KM
const double TP = 2.410142264; 
const double K_KM_MINUS_1 = 0.728; // Tu hipótesis C = K_KM - 1

// --- UTILIDADES MATEMÁTICAS OPTIMIZADAS ---

// Función para imprimir u128 (cout no lo soporta nativamente)
std::ostream& operator<<(std::ostream& os, u128 n) {
    if (n == 0) return os << "0";
    std::string s;
    while (n > 0) {
        s += (char)('0' + (n % 10));
        n /= 10;
    }
    for (int i = 0; i < s.length() / 2; ++i) std::swap(s[i], s[s.length() - 1 - i]);
    return os << s;
}

// Multiplicación modular segura (a*b)%m para 128 bits
u64 mul_mod(u64 a, u64 b, u64 m) {
    return (u64)((u128)a * b % m);
}

// Potencia modular (base^exp)%mod
u64 power(u64 base, u64 exp, u64 mod) {
    u64 res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = mul_mod(res, base, mod);
        base = mul_mod(base, base, mod);
        exp /= 2;
    }
    return res;
}

// Test de Primalidad Miller-Rabin (Determinista para u64)
bool is_prime_mr(u64 n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;
    
    u64 d = n - 1;
    int s = 0;
    while (d % 2 == 0) {
        d /= 2;
        s++;
    }
    
    // Bases para determinismo hasta 2^64
    static const u64 bases[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (u64 a : bases) {
        if (n <= a) break;
        u64 x = power(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}

// Algoritmo Pollard's Rho para encontrar un factor no trivial
u64 pollard_rho(u64 n) {
    if (n % 2 == 0) return 2;
    if (is_prime_mr(n)) return n;
    
    u64 x = 2, y = 2, d = 1, c = 1;
    auto f = [&](u64 x) { return (mul_mod(x, x, n) + c) % n; };
    
    while (d == 1) {
        x = f(x);
        y = f(f(y));
        d = std::gcd((x > y ? x - y : y - x), n);
        if (d == n) { // Fallo, cambiar constante
            x = rand() % (n - 2) + 2;
            y = x;
            c = rand() % (n - 1) + 1;
            d = 1;
        }
    }
    return d;
}

// Factorización completa y conteo de divisores d(n)
u64 count_divisors(u64 n) {
    if (n == 1) return 1;
    std::vector<u64> factors;
    
    // Extraer factores
    while (n > 1 && !is_prime_mr(n)) {
        u64 factor = pollard_rho(n);
        while (!is_prime_mr(factor)) factor = pollard_rho(factor);
        while (n % factor == 0) {
            factors.push_back(factor);
            n /= factor;
        }
    }
    if (n > 1) factors.push_back(n);
    
    // Calcular d(n)
    if (factors.empty()) return 2; // Caso primo ya detectado antes
    
    std::sort(factors.begin(), factors.end());
    u64 total_divs = 1;
    int current_count = 1;
    for (size_t i = 1; i < factors.size(); ++i) {
        if (factors[i] == factors[i-1]) {
            current_count++;
        } else {
            total_divs *= (current_count + 1);
            current_count = 1;
        }
    }
    total_divs *= (current_count + 1);
    return total_divs;
}

// --- FUNCIONES DEL MODELO KM ---

// Omega(n) = d(2n) - 4
double get_omega(u64 n) {
    // Optimización: d(2n). Si n es par, n = 2^k * m. 2n = 2^(k+1)*m.
    // d(2n) = d(m) * (k+2).
    // Si n es impar, d(2n) = d(n) * 2.
    
    int k = 0;
    while ((n & 1) == 0) {
        n >>= 1;
        k++;
    }
    // n ahora es la parte impar m
    u64 d_m = count_divisors(n);
    u64 d_2n = d_m * (k + 2);
    return (double)d_2n - 4.0;
}

// Función T(n) aproximada (los términos decaen rapidísimo)
double calculate_T(u64 n) {
    double total = 1.0;
    double prod = 1.0;
    
    // Iteramos los primeros 12 términos (suficiente precisión)
    for (int j = 0; j < 12; ++j) {
        // El argumento es n * 2^j
        // omega(n * 2^j)
        // Si n = 2^k * m, entonces n*2^j = 2^(k+j) * m
        // d(2 * n * 2^j) = d(2^(k+j+1) * m) = d(m) * (k+j+2)
        
        // Recalculamos d(m) solo una vez para optimizar
        // Pero para mantener el código limpio aquí llamamos a get_omega
        // Nota: En producción se factorizaría n una sola vez fuera del loop.
        
        // Truco de optimización: Omega crece, 1/(1+Om) decrece.
        // Calculamos omega directamente sin re-factorizar todo
        
        u64 temp_n = n;
        int k = 0;
        while ((temp_n & 1) == 0) {
             temp_n >>= 1;
             k++;
        }
        // temp_n es 'm' (impar). 
        // omega(n*2^j) = d(m)*(k+j+2) - 4
        // Necesitamos d(m) solo una vez.
        static thread_local u64 cached_n = 0;
        static thread_local u64 cached_dm = 0;
        
        u64 d_m;
        if (n == cached_n) {
            d_m = cached_dm;
        } else {
            d_m = count_divisors(temp_n); // Costoso, se hace solo en j=0
            cached_n = n;
            cached_dm = d_m;
        }

        double omega_val = (double)(d_m * (k + j + 2)) - 4.0;
        prod *= (1.0 / (1.0 + omega_val));
        total += prod;
        
        if (prod < 1e-6) break; 
    }
    return total;
}

int main() {
    std::cout << "--- SONDA DE ESPACIO PROFUNDO KM (C++ Optimizado) ---" << std::endl;
    std::cout << "Target C = K_KM - 1 = " << K_KM_MINUS_1 << std::endl;
    std::cout << "Analizando estabilidad de T_bar y O(sqrt(n))..." << std::endl << std::endl;
    
    // Magnitudes a testear: 10^9, 10^12, 10^15, 10^18, 10^19 (Límite u64)
    // Para 10^20 real se necesita aritmética BigInt completa en la factorización
    // pero 10^19 es suficiente para ver la asíntota.
    std::vector<u64> magnitudes = {
        1000000000ULL,          // 10^9
        1000000000000ULL,       // 10^12
        1000000000000000ULL,    // 10^15
        1000000000000000000ULL, // 10^18
        9000000000000000000ULL  // 9x10^18 (Max u64 approx)
    };
    
    int sample_size = 50000; // Muestra estadística robusta
    
    std::cout << std::setw(0) << "Magnitud (N)" 
              << std::setw(15) << "T_bar Local" 
              << std::setw(15) << "C Proyectado" 
              << std::setw(15) << "Diff Target" 
              << std::setw(10) << "Var(T)" << std::endl;
    std::cout << std::string(85, '-') << std::endl;

    for (u64 mag : magnitudes) {
        double sum_T = 0;
        double sum_sq_T = 0; // Para varianza
        
        // Paralelización con OpenMP
        #pragma omp parallel for reduction(+:sum_T, sum_sq_T)
        for (int i = 0; i < sample_size; ++i) {
            // Usamos números aleatorios alrededor de la magnitud para evitar sesgos locales
            // O secuenciales para ver un tramo continuo. Secuencial es mejor para sismógrafo.
            u64 n = mag + i; 
            double t = calculate_T(n);
            sum_T += t;
            sum_sq_T += t * t;
        }
        
        double t_bar = sum_T / sample_size;
        double variance = (sum_sq_T / sample_size) - (t_bar * t_bar);
        double std_dev = std::sqrt(variance);
        
        // C = T_bar / (Tp - 1)
        double c_proj = t_bar / (TP - 1.0);
        double diff = c_proj - K_KM_MINUS_1;
        
        std::cout << std::scientific << std::setprecision(2) << (double)mag 
                  << std::fixed << std::setprecision(5) 
                  << std::setw(15) << t_bar 
                  << std::setw(15) << c_proj 
                  << std::setw(15) << diff 
                  << std::setw(15) << variance << std::endl;
    }
    
    return 0;
}