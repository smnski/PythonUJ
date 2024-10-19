line = "raz dwa \n trzy cztery \t piec szesc"
words = line.split()

longest = max(words, key=len)
length = len(longest)

print("Najdluzszy wyraz: " + longest + "\nDlugosc: " + str(length))