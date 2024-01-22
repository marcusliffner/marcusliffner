#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string gradetext);
int count_words(string gradetext);
int count_sentences(string gradetext);

int main(void)
{
    string gradetext = get_string("Text: ");
    float letters = count_letters(gradetext);
    float words = count_words(gradetext);
    float sentences = count_sentences(gradetext);

    // L = avrage letters in 100 words
    // S = avrage sentencces in 100 words
    float L = 100 * letters / words;
    float S = 100 * sentences / words;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 15)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
    // printf("Letters: %i \n", letters);
    // printf("Words: %i \n", words);
    // printf("Sentences: %i \n", sentences);
}

int count_letters(string gradetext)
{
    float letters = 0;
    for (int i = 0, lenth = strlen(gradetext); i < lenth; i++)
    {
        // if upper or lower char letters + 1
        if (isupper(gradetext[i]) || islower(gradetext[i]))
        {
            letters++;
        }
    }
    return letters;
}
int count_words(string gradetext)
{
    float words = 0;
    int lenth = strlen(gradetext);

    if (lenth > 0)
    {
        words++;
    }
    for (int i = 0; i < lenth; i++)
    {
        // if upper or lower char letters + 1
        if (isspace(gradetext[i]))
        {
            words++;
        }
    }
    return words;
}
int count_sentences(string gradetext)
{
    float sentences = 0;

    for (int i = 0, lenth = strlen(gradetext); i < lenth; i++)
    {
        // if upper or lower char letters + 1
        if ((gradetext[i] == '.') || (gradetext[i] == '?') || (gradetext[i] == '!'))
        {
            sentences++;
        }
    }
    return sentences;
}
