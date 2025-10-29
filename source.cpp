#include <iostream>
#include <string>
#include <stdexcept>

// Python: def factorial(n):
// C++: long long factorial(int n)
long long factorial(int n) {
    // Python: if n < 0: return "負の数の階乗は定義されていません"
    // C++: Throw an exception for consistency and type safety.
    // The main function will catch this and print the desired message to replicate Python's output.
    if (n < 0) {
        throw std::invalid_argument("負の数の階乗は定義されていません");
    }
    // Python: elif n == 0: return 1
    if (n == 0) {
        return 1;
    }
    // Python: else: result = 1; for i in range(1, n + 1): result *= i; return result
    else {
        long long result = 1;
        // Factorials grow very quickly. long long can handle up to 20!.
        // For n > 20, an overflow might occur, which is not explicitly handled
        // in the original Python version either.
        for (int i = 1; i <= n; ++i) {
            result *= i;
        }
        return result;
    }
}

// Python: def main(): ... if __name__ == "__main__": main()
// C++: int main() { ... }
int main() {
    std::cout << "階乗を計算する数値を入力してください: ";
    std::string input_str;
    std::getline(std::cin, input_str); // Read entire line to handle potential non-integer input

    try {
        int num = std::stoi(input_str); // Convert string to integer. Can throw std::invalid_argument or std::out_of_range.
        
        // Python: print(f"{num}の階乗は {factorial(num)} です")
        long long result = factorial(num); // Call factorial. Can throw std::invalid_argument for negative n.
        std::cout << num << "の階乗は " << result << " です" << std::endl;

    } catch (const std::invalid_argument& e) {
        // This catch block handles:
        // 1. `std::stoi` throwing `std::invalid_argument` (input string is not a valid integer).
        // 2. `factorial` throwing `std::invalid_argument` (for negative n).
        
        // Check if the exception message matches the one from our factorial function for negative numbers.
        if (std::string(e.what()) == "負の数の階乗は定義されていません") {
            // Replicate Python's f-string behavior for negative numbers
            // Python: print(f"{num}の階乗は 負の数の階乗は定義されていません です")
            // Here, input_str contains the original input, which might be "-5", etc.
            std::cout << input_str << "の階乗は " << e.what() << " です" << std::endl;
        } else {
            // This is likely from std::stoi indicating non-integer input.
            // Python: except ValueError: print("無効な入力です。整数を入力してください。")
            std::cout << "無効な入力です。整数を入力してください。" << std::endl;
        }
    } catch (const std::out_of_range& e) {
        // This catch block handles `std::stoi` throwing `std::out_of_range`
        // (input integer is too large or too small for `int` type).
        // Python: except ValueError: print("無効な入力です。整数を入力してください。")
        std::cout << "無効な入力です。整数を入力してください。" << std::endl;
    } catch (const std::exception& e) {
        // Generic catch-all for any other unexpected exceptions.
        std::cerr << "予期せぬエラーが発生しました: " << e.what() << std::endl;
    }

    return 0; // Indicate successful execution
}
