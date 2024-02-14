#ifndef tensor_h
#define tensor_h

#include <iostream>
#include <vector>

template <typename T>
class Tensor {
private:
    std::vector<std::vector<T>> data;
    size rows;
    size cols;

public:
    // Constructor
    Tensor(size rows, size cols) : rows(rows), cols(cols), data(rows, std::vector<T>(cols)) {}

    // Access element at position (i, j)
    T& at(size i, size j) {
        return data.at(i).at(j);
    }

    // Get number of rows
    size getRows() const {
        return rows;
    }

    // Get number of columns
    size getCols() const {
        return cols;
    }

    // Display the tensor
    void display() const {
        for (size i = 0; i < rows; ++i) {
            for (size j = 0; j < cols; ++j) {
                std::cout << data[i][j] << "\t";
            }
            std::cout << std::endl;
        }
    }
    // Initialize default tensor elements
    void init() {
        for (size i = 0; i < rows; ++i) {
            for (size j = 0; j < cols; ++j) {
                at(i, j) = i * cols + j;
            }
        }
    }
};

#endif // tensor_h
