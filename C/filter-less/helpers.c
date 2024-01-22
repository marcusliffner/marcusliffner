#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int total = image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen;
            int roundedtotal = (int)round(total / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = roundedtotal;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redcolor = (int)round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            int greencolor = (int)round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            int bluecolor = (int)round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            if (redcolor > 255)
            {
                redcolor = 255;
            }
            if (greencolor > 255)
            {
                greencolor = 255;
            }

            if (bluecolor > 255)
            {
                bluecolor = 255;
            }
            image[i][j].rgbtRed = redcolor;
            image[i][j].rgbtGreen = greencolor;
            image[i][j].rgbtBlue = bluecolor;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        RGBTRIPLE tempwidth[width];
        for (int j = 0; j < width; j++)
        {
            tempwidth[j] = image[i][width - 1 - j];
        }
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tempwidth[j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temparr[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float totalRed = 0.0;
            float totalGreen = 0.0;
            float totalBlue = 0.0;
            int count = 0;
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int ik = i + k;
                    int jl = j + l;
                    if (ik >= 0 && ik < height && jl >= 0 && jl < width)
                    {
                        totalRed += image[ik][jl].rgbtRed;
                        totalGreen += image[ik][jl].rgbtGreen;
                        totalBlue += image[ik][jl].rgbtBlue;
                        count++;
                    }
                }
            }
            temparr[i][j].rgbtRed = (int)round(totalRed / count);
            temparr[i][j].rgbtGreen = (int)round(totalGreen / count);
            temparr[i][j].rgbtBlue = (int)round(totalBlue / count);
        }
    }
    for (int ic = 0; ic < height; ic++)
    {
        for (int jc = 0; jc < width; jc++)
        {
            image[ic][jc] = temparr[ic][jc];
        }
    }

    return;
}
