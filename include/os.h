#include <iostream>
#include <cstdlib>

class OS {
public:
    static void execute(const std::string& command) {
        int result = std::system(command.c_str());
        if (result != 0) {
            std::cerr << "Command execution failed." << std::endl;
        }
    }

    static std::string name() {
        #ifdef _WIN32
            return "Windows";
        #elif __linux__
            return "Linux";
        #else
            return "Unknown";
        #endif
    }
};
