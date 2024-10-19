line = "raz dwa \n trzy cztery \t piec szesc"
words = line.split()

print(sum(len(word) for word in words))