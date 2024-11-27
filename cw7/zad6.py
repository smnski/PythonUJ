import random
import itertools

def iter_binary():
    return itertools.cycle([0, 1])

def iter_direction():
    while True:
        yield random.choice("NESW")

def iter_week():
    return itertools.cycle(range(7))

def tests():
    iter1 = iter_binary()
    iter2 = iter_direction()
    iter3 = iter_week()

    print("Test iteratora binarnego: ")
    for _ in range(20):
        print(next(iter1), end=" ")
    print()

    print("Test iteratora kierunku: ")
    for _ in range(20):
        print(next(iter2), end=" ")
    print()

    print("Test iteratora dni tygodnia: ")
    for _ in range(20):
        print(next(iter3), end=" ")
    print()

if __name__ == "__main__":
    tests()