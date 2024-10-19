line = "raz dwa \n trzy cztery \t piec szesc"
words = line.split()

result_first = "".join(word[0] for word in words)
result_last = "".join(word[len(word)-1] for word in words)

print("Pierwsze znaki: " + result_first)
print("Ostatnie znaki: " + result_last)