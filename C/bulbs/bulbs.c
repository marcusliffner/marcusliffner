#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // asks for a message
    string word = get_string("Message: ");

    // changes word into ASCII numbers
    for (int i = 0, lenth = strlen(word); i < lenth; i++)
    {
        int decimal = word[i];

        // changes word into binary
        int bitarray[] = {
            0, 0, 0, 0, 0, 0, 0, 0,
        };
        int j = 0;
        while (decimal > 0)
        {
            bitarray[j] = decimal % 2;
            decimal = decimal / 2;
            j++;
        }
        // prints bulbs depending on the message
        for (int k = BITS_IN_BYTE - 1; k >= 0; k--)
        {
            print_bulb(bitarray[k]);
        }

        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
