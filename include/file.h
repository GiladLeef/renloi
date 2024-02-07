#include <iostream>
#include <fstream>
#include <sstream>

class File {
public:
    template <typename T>
    static void write(const char *filename, const T &content) {
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Error opening file " << filename << " for writing." << std::endl;
            return;
        }

        // Use the << operator to write content to the file
        file << content;

        // The file will be closed automatically when 'file' goes out of scope
    }

    static std::string read(const char *filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Error opening file " << filename << " for reading." << std::endl;
            exit(EXIT_FAILURE);
        }

        // Read the file content into a string
        std::ostringstream content_stream;
        content_stream << file.rdbuf();
        std::string content = content_stream.str();

        return content;
    }
    static bool createDirectory(const std::string& path) {
        int status = mkdir(path.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        return (status == 0);
    }

    static bool fileExists(const std::string& filePath) {
        struct stat buffer;
        return (stat(filePath.c_str(), &buffer) == 0);
    }
};
