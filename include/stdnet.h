#include <iostream>
#include <string>
#include <curl/curl.h>

class Net {
public:
    class Http {
    public:
        static std::string get(const std::string& url) {
            return performHttpRequest(url, CURLOPT_HTTPGET);
        }

        static std::string post(const std::string& url, const std::string& data) {
            return performHttpRequest(url, CURLOPT_POSTFIELDS, data.c_str(), CURLOPT_POST);
        }

        static std::string put(const std::string& url, const std::string& data) {
            return performHttpRequest(url, CURLOPT_POSTFIELDS, data.c_str(), CURLOPT_CUSTOMREQUEST, "PUT");
        }

    private:
        static std::string performHttpRequest(const std::string& url, ...) {
            CURL* curl;
            CURLcode res;

            curl_global_init(CURL_GLOBAL_DEFAULT);

            curl = curl_easy_init();
            if (curl) {
                // Set the URL
                curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

                // Set additional options based on variable arguments
                va_list args;
                va_start(args, url);
                int option;
                while ((option = va_arg(args, int)) != 0) {
                    curl_easy_setopt(curl, option, va_arg(args, void*));
                }
                va_end(args);

                // Set the callback function to write the received data into a string
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
                std::string response;

                // Set the pointer to the response string
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

                // Perform the HTTP request
                res = curl_easy_perform(curl);

                // Check for errors
                if (res != CURLE_OK) {
                    std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
                }

                // Clean up
                curl_easy_cleanup(curl);

                return response;
            }

            return "";
        }

        // Callback function to write the received data into a string
        static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
            size_t totalSize = size * nmemb;
            response->append(static_cast<char*>(contents), totalSize);
            return totalSize;
        }
    };
};
