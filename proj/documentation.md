# Opis projektu
Projekt jest moją implementacją popularnej gry w statki.
Po własnoręcznym ustawieniu statków na swojej planszy, bądź zrobieniem tego automatycznie przygotowaną wcześniej funkcją, rozgrywamy partię na przeciwnika kontrolowanego przez komputer.

# Kluczowe elementy kodu

## Klasa WelcomeScreen
`placeShipsYourself()` - Pozwala graczowi na ustawienie statków na planszy własnoręcznie.  

`autoPlaceShips()` - Pozwala graczowi ustawić statki na planszy automatycznie. Rozstawia także statki dla przeciwnika (komputera).  

`canPlace()`, `place()` - Stanowią kluczowe elementy powyższych funkcji, sprawdzając czy statek można ustawić na danym polu, a następnie go tam ustawiając.
