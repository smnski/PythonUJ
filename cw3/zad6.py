def build(length, width):
    part_one = "+---"
    part_two = "|   "

    output = (part_one * width + "+\n" + part_two * width + "|\n") * length + part_one * width + "+"

    return output

if __name__ == "__main__":
    length = int(input("Input length: "))
    width = int(input("Input width: "))

    output = build(length, width)
    print(output)