#include <iostream>

using size = size_t;

// Function to mimic the print function
template <typename... Args>
void print(const Args&... args) {
    (std::cout << ... << args) << std::endl;
}

template<typename T>
void input(T& variable) {
    std::cin >> variable;
}
