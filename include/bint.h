#include <iostream>
#include <gmpxx.h>
#include <regex>

class bint {
private:
    mpz_class value;

public:
    // Constructors
    bint() : value(0) {}

    // Constructor from hex or decimal string
    bint(const std::string& val) {
        initializeFromString(val);
    }

    // Constructor from hex or decimal string
    bint(const std::string& val) {
        std::regex hex_pattern("^0x[0-9a-fA-F]+$");
        std::regex decimal_pattern("^\\d+$");

        if (std::regex_match(val, hex_pattern)) {
            // Hexadecimal string
            value = mpz_class(val.c_str() + 2, 16);
        } else if (std::regex_match(val, decimal_pattern)) {
            // Decimal string
            value = mpz_class(val);
        } else {
            // Invalid string format, default to 0
            std::cerr << "Error: Invalid string format. Defaulting to 0." << std::endl;
            value = 0;
        }
    }

    // Arithmetic operators
    bint operator+(const bint& other) const {
        bint result;
        result.value = value + other.value;
        return result;
    }

    bint operator-(const bint& other) const {
        bint result;
        result.value = value - other.value;
        return result;
    }

    bint operator*(const bint& other) const {
        bint result;
        result.value = value * other.value;
        return result;
    }

    bint operator/(const bint& other) const {
        if (other.value != 0) {
            bint result;
            result.value = value / other.value;
            return result;
        } else {
            // Handle division by zero (you may want to throw an exception or handle it differently)
            std::cerr << "Error: Division by zero." << std::endl;
            return bint();
        }
    }
    // Assignment operator
    bint& operator=(const bint& other) {
        value = other.value;
        return *this;
    }

    // Increment and Decrement operators
    bint& operator++() {
        value++;
        return *this;
    }

    bint operator++(int) {
        bint temp = *this;
        ++(*this);
        return temp;
    }

    bint& operator--() {
        value--;
        return *this;
    }

    bint operator--(int) {
        bint temp = *this;
        --(*this);
        return temp;
    }

    // Compound assignment operators
    bint& operator+=(const bint& other) {
        value += other.value;
        return *this;
    }

    bint& operator-=(const bint& other) {
        value -= other.value;
        return *this;
    }

    bint& operator*=(const bint& other) {
        value *= other.value;
        return *this;
    }

    bint& operator/=(const bint& other) {
        if (other.value != 0) {
            value /= other.value;
        } else {
            // Handle division by zero
            std::cerr << "Error: Division by zero." << std::endl;
            value = 0;
        }
        return *this;
    }

    // Unary minus operator
    bint operator-() const {
        bint result;
        result.value = -value;
        return result;
    }

    // Modulus operator
    bint operator%(const bint& other) const {
        if (other.value != 0) {
            bint result;
            result.value = value % other.value;
            return result;
        } else {
            // Handle modulus by zero
            std::cerr << "Error: Modulus by zero." << std::endl;
            return bint();
        }
    }

    // Comparison operators
    bool operator==(const bint& other) const {
        return value == other.value;
    }

    bool operator!=(const bint& other) const {
        return value != other.value;
    }

    bool operator<(const bint& other) const {
        return value < other.value;
    }

    bool operator<=(const bint& other) const {
        return value <= other.value;
    }

    bool operator>(const bint& other) const {
        return value > other.value;
    }

    bool operator>=(const bint& other) const {
        return value >= other.value;
    }
    // Bitwise AND operator
    bint operator&(const bint& other) const {
        bint result;
        result.value = value & other.value;
        return result;
    }

    // Bitwise OR operator
    bint operator|(const bint& other) const {
        bint result;
        result.value = value | other.value;
        return result;
    }

    // Bitwise XOR operator
    bint operator^(const bint& other) const {
        bint result;
        result.value = value ^ other.value;
        return result;
    }

    // Bitwise NOT operator
    bint operator~() const {
        bint result;
        result.value = ~value;
        return result;
    }

    // Left shift operator
    bint operator<<(int n) const {
        bint result;
        result.value = value << n;
        return result;
    }

    // Right shift operator
    bint operator>>(int n) const {
        bint result;
        result.value = value >> n;
        return result;
    }
    // Logical AND operator
    bool operator&&(const bint& other) const {
        return value && other.value;
    }

    // Logical OR operator
    bool operator||(const bint& other) const {
        return value || other.value;
    }

    // Logical NOT operator
    bool operator!() const {
        return !value;
    }
    // Bitwise AND assignment operator
    bint& operator&=(const bint& other) {
        value &= other.value;
        return *this;
    }

    // Bitwise OR assignment operator
    bint& operator|=(const bint& other) {
        value |= other.value;
        return *this;
    }

    // Bitwise XOR assignment operator
    bint& operator^=(const bint& other) {
        value ^= other.value;
        return *this;
    }
    // Equality operator for strings
    bool operator==(const std::string& str) const {
        return value == mpz_class(str);
    }

    // Inequality operator for strings
    bool operator!=(const std::string& str) const {
        return value != mpz_class(str);
    }
    // Conversion operator to std::string
    operator std::string() const {
        return value.get_str();
    }

    // Output operator
    friend std::ostream& operator<<(std::ostream& os, const bint& num) {
        os << num.value.get_str();
        return os;
    }
};
