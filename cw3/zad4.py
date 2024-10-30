if __name__ == '__main__':
    while(True):
        user_input = input("Input a real number: ")
        if(user_input == "stop"):
            break

        try:
            x = float(user_input)
            print("x = " + str(x))
            print("x^3 = " + str(x*x*x))
        except ValueError:
            print("Error: Expected a real number")
            continue