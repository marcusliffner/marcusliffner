from cs50 import get_float


def main():
    changeowed = getchange()
    changenummber = calculatechange(changeowed)
    print(changenummber)


def getchange():
    while True:
        try:
            changeowed = get_float("Input change owed: ")
            if changeowed >= 0:
                break
            else:
                print("Enter a positive number")
        except ValueError:
            print("Enter a number")
    return changeowed


def calculatechange(changeowed):
    pennie = 0
    nickel = 0
    dime = 0
    quarter = 0
    while changeowed >= 0.24:
        quarter += 1
        changeowed -= 0.25

    while changeowed >= 0.09:
        dime += 1
        changeowed -= 0.10

    while changeowed >= 0.04:
        nickel += 1
        changeowed -= 0.05

    while changeowed >= 0.009:
        pennie += 1
        changeowed -= 0.01

    changenummber = quarter + dime + nickel + pennie
    return changenummber


if __name__ == "__main__":
    main()
