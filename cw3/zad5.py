def build(size):
    part = "|...."
    top = ""
    bot = "0"

    for i in range (1, size + 1):
        top += part
        bot += str(i).rjust(len(part))

    top += "|"
    output = top + "\n" + bot

    return output

if __name__ == "__main__":
    size = int(input("Input length: "))
    output = build(size)
    print(output)