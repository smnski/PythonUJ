def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i

    return result

if __name__ == "__main__":
    n = int(input("Enter a number: "))
    result = factorial(n)
    print(str(result))