#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int get_size(void);
void print_grid(int size);

// runs program
int main(void)
{
    // get block size
    int height = get_size();
    // print block size
    print_grid(height);
}
// ask user for block size
int get_size(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    return height;
}
// prints mario blocks if input is 1-8
void print_grid(int height)
{
    char block[40] = "#";

    for (int x = 0; height > x; x++)
    {
        char space[40] = "";
        for (int j = (height - 1); x < j; j--)
        {
            strcat(space, " ");
        }
        printf("%s%s  %s", space, block, block);
        strcat(block, "#");
        printf("\n");
    }
}