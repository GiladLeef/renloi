#include <iostream>

// Function to mimic the print function
template <typename... Args>
void print(const Args&... args) {
    (std::cout << ... << args) << std::endl;
}
