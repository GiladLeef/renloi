#include <cmath>
#include <iostream>
#include <cstdint>
#include <random>

using uint64 = uint64_t;
using int64 = int64_t;

int randint(int low, int high) {
    std::random_device rd;  // Use random_device to seed the generator
    std::mt19937 mt(rd());  // Mersenne Twister 19937 generator
    std::uniform_int_distribution<int> dist(low, high);  // Uniform distribution between low and high

    return dist(mt);
}

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
