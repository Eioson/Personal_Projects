bingus = input("Pick 1, 2, or 3: ")

match bingus:
    case "1":
        print("You are racist")
    case "2":
        print("You are even more racist")
    case "3":
        print("You are even even more racist")
    case _: # default can be anything
        print("You are not racist")