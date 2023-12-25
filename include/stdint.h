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
