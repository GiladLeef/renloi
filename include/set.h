#ifndef set_h
#define set_h

#include <set>
#include <iostream>

template <typename T>
class Set {
private:
    std::set<T> internalSet;

public:
    // Add an element to the set
    void add(const T& element) {
        internalSet.insert(element);
    }

    // Remove an element from the set
    void remove(const T& element) {
        internalSet.erase(element);
    }

    // Check if an element is in the set
    bool contains(const T& element) const {
        return internalSet.find(element) != internalSet.end();
    }

    // Get the size of the set
    size_t size() const {
        return internalSet.size();
    }

    // Print the elements of the set
    void print() const {
        for (const auto& elem : internalSet) {
            std::cout << elem << " ";
        }
        std::cout << std::endl;
    }
};
#endif // set_h
