L = [1, 2, 3, 11, 22, 33, 111, 222, 333]

result = " ".join(str(num).zfill(3) for num in L)
print(result)