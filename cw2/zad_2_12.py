line = "raz dwa \n trzy cztery \t piec szesc"
words = line.split()
result = "".join(word[0] for word in words)

print(result)