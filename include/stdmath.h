#include <cmath>

class Math {
public:
    static double sqrt(double x) {
        return std::sqrt(x);
    }

    static int abs(int x) {
        return std::abs(x);
    }

    static double pow(double base, double exponent) {
        return std::pow(base, exponent);
    }

    static double round(double x) {
        return std::round(x);
    }

    template <typename T>
    static T min(T a, T b) {
        return std::min(a, b);
    }

    template <typename T>
    static T max(T a, T b) {
        return std::max(a, b);
    }
};
