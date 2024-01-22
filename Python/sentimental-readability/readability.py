from cs50 import get_string
from cs50 import get_float


def main():
    gradetext = get_string("Input text to be graded: ")
    letters = countletters(gradetext)
    words = countwords(gradetext)
    sentences = countsentences(gradetext)

    let = 100 * (letters / words)
    sen = 100 * (sentences / words)

    index = 0.0588 * let - 0.296 * sen - 15.8
    index = round(index)
    if index < 1:
        print("Before Grade 1")
    elif index > 15:
        print("Grade 16+")
    else:
        print("Grade " + str(index))


def countletters(gradetext):
    letters = 0
    for i in range(len(gradetext)):
        if gradetext[i].isupper() or gradetext[i].islower():
            letters += 1
    return letters


def countwords(gradetext):
    words = len(gradetext.split())
    return words


def countsentences(gradetext):
    sentences = 0
    for i in range(len(gradetext)):
        if gradetext[i] == "." or gradetext[i] == "?" or gradetext[i] == "!":
            sentences += 1
    return sentences


if __name__ == "__main__":
    main()
