#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int answer = 0;
    while (answer < 9)
    {
    printf("This program calculates your Lama groth\n");
    answer = get_int("How many Lamas do you have?\n");
    }

    for (;;)
    {

            printf("Start size: %i \n", answer);
            int lamas = answer;
            int newborns = lamas / 3;
            int deadlamas = lamas / 4;
            lamas = (lamas + newborns);
            lamas = (lamas - deadlamas);
            printf("You are estimated to have %d new born lamas during one year \n", newborns);
            printf("You are estimated to have %d dieing lams during one year \n", deadlamas);

            printf("Total amount of Lamas in one year will be %i \n", lamas);

            // TODO: Prompt for end size
            int goal = get_int("What is your population goal? \n");
            printf("End Size: %i \n", goal);

            int years = 0;

            if (goal == answer)
            {
                years = 0;
                printf("Years: %i  \n", years);
                break;
            }
           else if(goal > answer)
            {
                // TODO: Calculate number of years until we reach threshold

                    while (goal > answer)
                    {
                        int newborns1 = answer / 3;
                        int deadlamas1 = answer / 4;
                        answer = (answer + newborns1);
                        answer = (answer - deadlamas1);
                        years = (years + 1);
                    }
                // TODO: Print number of years
                printf("Years: %i  \n", years);
                break;
            }

        }
    }

