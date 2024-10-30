L = [3, 5, 4] ; L = L.sort()
# Do zmiennej L zostanie przypisana wartosc "None".
# Linijka "L = L.sort()" oznacze przypisanie do L tego, co zwroci sort, a sort niczego nie zwraca.
# Powinnismy zastosowac po prostu "L.sort()" a nie "L = L.sort()"

x, y = 1, 2, 3
# Po prawej stronie znaku "=" jest wiecej wartosci, niz po lewej, przez co dochodzi do bledu.

X = 1, 2, 3 ; X[1] = 4
# Wyrazenie to tworzy tuple, ktore sa niemutowalne. Proba zmiany wartosci poprzez "X[1] = 4" powoduje zatem blad.

X = [1, 2, 3] ; X[3] = 4
# X[3] jest poza zakresem tej listy, gdyz jej kolejne elementy maja indeksy: 0, 1, 2.

X = "abc" ; X.append("d")
# X jest ciagiem znakow typu str, w Pythonie str nie posiada takiej metody, jak "append".

L = list(map(pow, range(8)))
# Funkcja pow wymaga dwoch argumentow, zas przekazujemy jej tylko jeden.