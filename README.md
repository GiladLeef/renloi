## Renloi: An easier alternative to C++

Renloi is a programming language designed to offer a simpler and more user-friendly development experience compared to C++, while still leveraging its power and performance through compilation. 

### Key features

* **Simplified syntax:** Renloi emphasizes readability and maintainability with a cleaner and more concise syntax.
* **Familiar concepts:** The core programming concepts in Renloi are similar to C++, making it easier for programmers with C++ experience to pick up.
* **C++ compilation:** Renloi code is compiled to C++ code, ensuring compatibility with existing C++ codebases.
* **GCC backend:** Renloi leverages the power and optimization capabilities of the GNU Compiler Collection (GCC) for compilation to machine code.

### Example

Here's a simple Renloi program that prints "Hello, world!":

```c++
#include <std.h>

int main() {
  print("Hello, world!");
  return 0;
}
```
In this example:
- `#include <std.h>` imports the standard library header file.
- `int main()` defines the entry point of the program.
- `print("Hello, world!");` outputs "Hello, world!" to the console.
- `return 0;` indicates successful program completion.
