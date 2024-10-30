x = 2; y = 3;
if (x > y):
    result = x;
else:
    result = y;
# ODP: Tak, kod jest poprawnie składniowy w pythonie. Nie trzeba używać tutaj średników, gdyż kod został poprawnie rozdzielony na linie,
# ale w niczym one nie przeszkadzają.


for i in "axby": if ord(i) < 100: print (i)

# ODP: Kod nie jest poprawny składniowo, ponieważ if jest tutaj pełnoprawną instrukcją warunkową i wymaga określenia do jakiego bloku kodu się odnosi.
# Robimy to poprzez podzielenie kodu na oddzielne linie, a tutaj został zawarty w jednej linii.

for i in "axby": print (ord(i) if ord(i) < 100 else i)

# Kod jest poprawny składniowo, ponieważ if został zastosowany jako wyrażenie warunkowe, które określa co wypisze print.



