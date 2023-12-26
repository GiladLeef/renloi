#include <iostream>
#include <string>
#include <curl/curl.h>

class Net {
public:
    class Http {
    public:
        static std::string get(const std::string& url) {
            CURL* curl;
            CURLcode res;

            curl_global_init(CURL_GLOBAL_DEFAULT);

            curl = curl_easy_init();
            if (curl) {
                // Set the URL
                curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

                // Set the callback function to write the received data into a string
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
                std::string response;

                // Set the pointer to the response string
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

                // Perform the HTTP GET request
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

    private:
        // Callback function to write the received data into a string
        static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
            size_t totalSize = size * nmemb;
            response->append(static_cast<char*>(contents), totalSize);
            return totalSize;
        }
    };
};
