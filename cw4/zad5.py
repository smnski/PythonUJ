def odwracanie_rec(L: list, left: int, right: int) -> None:
    if left >= right:
        return
    
    L[left], L[right] = L[right], L[left]
    odwracanie_rec(L, left + 1, right - 1)

def odwracanie_iter(L: list, left: int, right: int) -> None:
    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

if __name__ == "__main__":
    L1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    L2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # odwróci numery od 1 do 6 w miejscu w obu przypadkach
    odwracanie_rec(L1, 1, 5) 
    odwracanie_iter(L2, 1, 5)

    assert L1 == L2 == [1, 6, 5, 4, 3, 2, 7, 8, 9]