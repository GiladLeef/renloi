#include <iostream>
#include <string>

class String {
public:
    static std::string replace(const std::string& original, const std::string& toReplace, const std::string& replacement) {
        std::string result = original;
        size pos = 0;

        while ((pos = result.find(toReplace, pos)) != std::string::npos) {
            result.replace(pos, toReplace.length(), replacement);
            pos += replacement.length();
        }

        return result;
    }
};
