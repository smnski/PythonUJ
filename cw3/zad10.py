def getNumVal(rom):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
    result = 0
    previous = 0

    for symbol in reversed(rom):
        current = roman_values[symbol]

        if current >= previous:
            result += current
        else:
            result -= current

        previous = current

    return result

if __name__ == '__main__':
    assert getNumVal("IX") == 9
    assert getNumVal("CXXXVII") == 137