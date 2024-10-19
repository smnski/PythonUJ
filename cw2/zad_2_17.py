line = "raz dwa trzy cztery piec szesc"
sorted_1 = " ".join(sorted(line.split()))
sorted_2 = " ".join(sorted(line.split(), key=len, reverse=True))

print("Alfabetycznie: " + sorted_1)
print("Wzgledem dlugosci: " + sorted_2)