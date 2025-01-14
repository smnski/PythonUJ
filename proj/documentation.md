# Opis projektu
Projekt jest moją implementacją popularnej gry w statki.
Po własnoręcznym ustawieniu statków na swojej planszy, bądź zrobieniem tego automatycznie przygotowaną wcześniej funkcją, rozgrywamy partię na przeciwnika kontrolowanego przez komputer.

# Kluczowe elementy kodu

## Klasa WelcomeScreen
`placeShipsYourself()` - Pozwala graczowi na ustawienie statków na planszy własnoręcznie.  

`autoPlaceShips()` - Pozwala graczowi ustawić statki na planszy automatycznie. Rozstawia także statki dla przeciwnika (komputera).  

`canPlace()`, `place()` - Stanowią kluczowe elementy powyższych funkcji, sprawdzając czy statek można ustawić na danym polu, a następnie go tam ustawiając.  

`run()` - Obsługuje wejście z myszki użytkownika, czyli wybraną opcję ustawienia statków.  

`startGame()` - Wywołuje odpowiednie funkcje do ustawienia statków, a następnie rozpoczyna rozgrywkę, poprzez przejście do klasy `Gameplay`.

## Klasa Gameplay
`drawPlayerGrid()` - Na podstawie planszy przekazanej przez klasę `WelcomeScreen`, rysuje planszę użytkownika, wraz z rozstawionymi przez niego statkami.  

`drawEnemyGrid()` - Na podstawie planszy przekazanej przez klasę `WelcomeScreen`, rysuje planszę przeciwnika, na której statki są ukryte.  

`handleClickOnEnemyGrid()` - Obsługuję logikę naciśnięcia na planszę przeciwnika przez użytkownika. Sprawdza, czy wybrane zostało prawidłowe pole, a następnie ukazuje wynik oddanego strzału.  

`selectionAI()` - W funkcji zawarta jest sztuczna inteligencja, która mierzy się z użytkownikiem. Gdy na planszy nie ma pól z odkrytym statkiem, to wybiera losowe pole. Natomiast, gdy trafiła wcześniej we fragment statku, to wpierw sprawdza otaczające go pola.  

`handleGameTurn()` - Przeprowadza pojedynczą turę gry, wpierw oczekując na ruch gracza, a następnie wywołując ruch przeciwnika.  

`run()` - Obsługuje wejście z myszki użytkownika, czyli wybrane pole, na które użytkownik próbuje oddać strzał.

# Instalacja i uruchomienie
1. Pobranie, bądź sklonowanie projektu z repozytorium.
2. Instalacja biblioteki pygame poprzez polecenie `pip install pygame`.
3. Uruchomienie gry poleceniem `python3 main.py`.

## Sterowanie
#### Rozstawianie statków własnoręcznie
Aby ustawić statek, należy kliknąć na wybrane pole. Statki nie mogą ze sobą sąsiadować, ani na siebie nachodzić.
Przyciskiem `R` zmieniamy ułożenie statku między pionowym, a poziomym.

#### Oddawanie strzału na planszę przeciwnika
Aby oddać strzał na wybrane pole przeciwnika, należy kliknąć na nie myszką. Oddawać strzały możemy jedynie na nieodkryte pola.

# Oznaczenia kolorów na planszy
### W trakcie ustawiania statków
- Szary - Puste pole.
- Zielony - Puste pola, na które możemy ustawić wybrany statek.
- Niebieski - Ustawiony statek.
- Czerwony - Pola, na których nie możemy ustawić statku.

### W trakcie gry
##### Plansza gracza
- Szary - Puste pole.
- Ciemnoszary - Trafione pole, które okazało się puste.
- Ciemnozielony - Pole z ustawionym statkiem.
- Niebieski - Pole z trafionym fragmentem statku.
- Czerwony - Pole z zatopionym statkiem.
##### Plansza przeciwnika
- Szary - Puste pole.
- Ciemnoszary - Trafione pole, które okazało się puste.
- Niebieski - Pole z trafionym fragmentem statku.
- Czerwony - Pole z zatopionym statkiem.

# Autor
Szymon Urbański, na potrzeby kursu języka Python, realizowanego na piątym semestrze Informatyki Stosowanej na Uniwersytecie Jagiellońskim.