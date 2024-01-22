#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string fname = get_string("Whats your name? \n");
    printf("Hello, %s \n", fname);
}