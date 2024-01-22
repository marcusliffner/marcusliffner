def main():
    height = getsize()
    printgrid(height)


def getsize():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
            else:
                print("Enter a number 1-8 to proceed")
        except ValueError:
            print("Enter a number 1-8 to proceed")
    return height


def printgrid(height):
    block = "#"
    for i in range(height):
        space = " " * (height - 1 - i)
        print(f"{space}{block}  {block}")
        block += "#"


if __name__ == "__main__":
    main()
