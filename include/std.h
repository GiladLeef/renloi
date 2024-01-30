#include <iostream>
#include <vector>

using size = size_t;

// Function to mimic the print function
template <typename... Args>
void print(const Args&... args) {
    (std::cout << ... << args) << std::endl;
}

// Function to mimic the input function
template<typename T>
void input(T& variable) {
    std::cin >> variable;
}

// Function to mimic the range function
template<typename T>
std::vector<T> range(T start, T end, T step = 1) {
    std::vector<T> result;
    for (T i = start; i < end; i += step) {
        result.push_back(i);
    }
    return result;
}

// Function to mimic the map function
template<typename Function, typename... Args>
auto map(Function func, const Args&... args) {
    return std::vector<decltype(func(args...))>{func(args...)...};
}

// Function to mimic the filter function
template<typename Predicate, typename Container>
auto filter(Predicate pred, const Container& container) {
    std::vector<typename Container::value_type> result;
    for (const auto& element : container) {
        if (pred(element)) {
            result.push_back(element);
        }
    }
    return result;
}
