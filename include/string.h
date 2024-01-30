#include <iostream>
#include <string>

class String {
public:
    static std::string replace(const std::string& original, const std::string& toReplace, const std::string& replacement) {
        std::string result = original;
        size_t pos = 0;

        while ((pos = result.find(toReplace, pos)) != std::string::npos) {
            result.replace(pos, toReplace.length(), replacement);
            pos += replacement.length();
        }

        return result;
    }

    static std::string upperCase(const std::string& str) {
        std::string result = str;
        for (char& c : result) {
            c = std::toupper(c);
        }
        return result;
    }

    static std::string lowerCase(const std::string& str) {
        std::string result = str;
        for (char& c : result) {
            c = std::tolower(c);
        }
        return result;
    }

    static bool startsWith(const std::string& str, const std::string& prefix) {
        return str.compare(0, prefix.length(), prefix) == 0;
    }

    static bool endsWith(const std::string& str, const std::string& suffix) {
        if (suffix.length() > str.length()) {
            return false;
        }
        return str.compare(str.length() - suffix.length(), suffix.length(), suffix) == 0;
    }

    static std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(' ');
        size_t last = str.find_last_not_of(' ');

        if (first == std::string::npos || last == std::string::npos) {
            return ""; // Empty or all-whitespace string
        }

        return str.substr(first, last - first + 1);
    }
};
