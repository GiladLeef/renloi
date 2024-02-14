#ifndef tensor_h
#define tensor_h

#include <iostream>
#include <vector>

template <typename T>
class Tensor {
private:
    std::vector<std::vector<T>> data;
    size_t rows;
    size_t cols;

public:
    // Constructor
    Tensor(size_t rows, size_t cols) : rows(rows), cols(cols), data(rows, std::vector<T>(cols)) {}

    // Access element at position (i, j)
    T& at(size_t i, size_t j) {
        return data.at(i).at(j);
    }

    // Get number of rows
    size_t getRows() const {
        return rows;
    }

    // Get number of columns
    size_t getCols() const {
        return cols;
    }

    // Display the tensor
    void display() const {
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                std::cout << data[i][j] << "\t";
            }
            std::cout << std::endl;
        }
    }
    // Initialize default tensor elements
    void init() {
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                at(i, j) = i * cols + j;
            }
        }
    }
};

#endif // tensor_h
