#include <iostream>
#include <string>
#include <optional>
#include <stdexcept>

// factorial関数は、負の数にはstd::nulloptを返し、それ以外の場合は階乗の計算結果を返します。
// 結果が大きくなる可能性があるため、long long型を使用しています。
std::optional<long long> factorial(int n) {
    if (n < 0) {
        // 負の数の階乗は定義されていないため、std::nulloptを返す。
        return std::nullopt;
    } else if (n == 0) {
        // 0の階乗は1
        return 1LL;
    } else {
        long long result = 1LL;
        for (int i = 1; i <= n; ++i) {
            // 注意: 非常に大きなNに対してはlong longでもオーバーフローする可能性があります。
            // 本実装では一般的な範囲の入力に対しては十分とみなしています。
            result *= i;
        }
        return result;
    }
}

int main() {
    // 標準入出力の同期を解除して高速化（任意だがC++ではよく行われるプラクティス）
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    std::cout << "階乗を計算する数値を入力してください: ";
    std::string line;
    std::getline(std::cin, line); // ユーザーからの入力を一行読み込む

    try {
        int num = std::stoi(line); // 文字列を整数に変換

        std::optional<long long> result = factorial(num);

        if (result.has_value()) {
            // 階乗が計算できた場合（負の数ではなかった場合）
            std::cout << num << "の階乗は " << result.value() << " です" << std::endl;
        } else {
            // 階乗が定義されていなかった場合（n < 0）
            std::cout << "負の数の階乗は定義されていません" << std::endl;
        }

    } catch (const std::invalid_argument& e) {
        // std::stoiが文字列を整数に変換できない場合（例: "abc"などの非数値入力）
        std::cout << "無効な入力です。整数を入力してください。" << std::endl;
    } catch (const std::out_of_range& e) {
        // std::stoiが変換できたが、int型で表現できる範囲を超えていた場合
        std::cout << "入力された数値が大きすぎるか小さすぎます。" << std::endl;
    }

    return 0;
}
