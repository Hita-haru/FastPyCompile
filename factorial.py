def factorial(n):
    if n < 0:
        return "負の数の階乗は定義されていません"
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

def main():
    try:
        num = int(input("階乗を計算する数値を入力してください: "))
        print(f"{num}の階乗は {factorial(num)} です")
    except ValueError:
        print("無効な入力です。整数を入力してください。")

if __name__ == "__main__":
    main()
