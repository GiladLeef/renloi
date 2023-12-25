#include <cmath>

double sqrt(double x) {
    return std::sqrt(x);
}

int abs(int x) {
    return std::abs(x);
}

double pow(double base, double exponent) {
    return std::pow(base, exponent);
}

double round(double x) {
    return std::round(x);
}

template <typename T>
T min(T a, T b) {
    return std::min(a, b);
}

template <typename T>
T max(T a, T b) {
    return std::max(a, b);
}
