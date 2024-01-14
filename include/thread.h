#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <condition_variable>
#include <functional>

class ThreadPool {
public:
    // Constructor: Initialize the thread pool with the specified number of threads
    ThreadPool(size_t num_threads) : threads_(), is_stopping_(false) {
        for (size_t i = 0; i < num_threads; ++i) {
            threads_.emplace_back(&ThreadPool::workerThread, this);
        }
    }

    // Destructor: Stop the threads and wait for all tasks to finish
    ~ThreadPool() {
        stop();
        wait();
    }

    // Function to add a task to the thread pool
    template <typename Function, typename... Args>
    void addTask(Function &&func, Args &&... args) {
        {
            std::unique_lock<std::mutex> lock(task_mutex_);
            task_queue_.emplace([func, args...] { func(args...); });
        }

        task_cv_.notify_one();
    }

    // Stop the thread pool
    void stop() {
        {
            std::unique_lock<std::mutex> lock(task_mutex_);
            is_stopping_ = true;
        }

        task_cv_.notify_all();
    }

    // Wait for all tasks to complete
    void wait() {
        for (std::thread &thread : threads_) {
            if (thread.joinable()) {
                thread.join();
            }
        }
    }

private:
    // Worker thread function
    void workerThread() {
        while (true) {
            std::function<void()> task;

            {
                std::unique_lock<std::mutex> lock(task_mutex_);

                task_cv_.wait(lock, [this] { return is_stopping_ || !task_queue_.empty(); });

                if (is_stopping_ && task_queue_.empty()) {
                    return;
                }

                task = std::move(task_queue_.front());
                task_queue_.pop();
            }

            task();
        }
    }

    // Member variables
    std::vector<std::thread> threads_;
    std::queue<std::function<void()>> task_queue_;
    std::mutex task_mutex_;
    std::condition_variable task_cv_;
    bool is_stopping_;
};

// Helper function to create a ThreadPool with a specified number of threads
ThreadPool createThreadPool(size_t num_threads) {
    return ThreadPool(num_threads);
}