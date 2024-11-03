# Funkcja do zadania 5
def make_ruler(n):
    part = "|...."
    top = ""
    bot = "0"

    for i in range (1, n + 1):
        top += part
        bot += str(i).rjust(len(part))

    top += "|"
    output = top + "\n" + bot

    return output

# Funkcja do zadania 6
def make_grid(rows, cols):
    part_one = "+---"
    part_two = "|   "

    output = (part_one * cols + "+\n" + part_two * cols + "|\n") * rows + part_one * cols + "+"

    return output

if __name__ == "__main__":
    length = int(input("Input ruler length: "))
    rows = int(input("Input grid rows: "))
    cols = int(input("Input grid columns: "))
    print() # \n

    print("Ruler:")
    print(make_ruler(length))
    print() # \n

    print("Grid:")
    print(make_grid(rows, cols))