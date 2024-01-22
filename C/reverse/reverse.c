#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    // if commandlines is not 4 1.(name of project) 2.(/reverse)3.(input.wav)4.(output.wav)
    if (argv[3])
    {
        printf("Error, only acceptible input is (./reverse) (input.wav) (output.wav) \n");
        return 1;
    }
    // Open input file for reading
    // TODO #2
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Error, Not a valid input file");
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (check_format(header) != 0)
    {
        fclose(input);
        return 1;
    }
    // Open output file for writing
    // TODO #5
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Error, Not a valid output file");
        fclose(output);
        fclose(input);
        return 1;
    }
    // Write header to file
    // TODO #6
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    BYTE buffer[size];
    for (fseek(input, 0 - size, SEEK_END); ftell(input) > sizeof(header) - size; fseek(input, 0 - (size * 2), SEEK_CUR))
    {
        fread(&buffer, size, 1, input);
        fwrite(&buffer, size, 1, output);
    }
    fclose(input);
    fclose(output);
    return 0;
}

int check_format(WAVHEADER header)
{
    BYTE formatcheck[] = {'W', 'A', 'V', 'E'};
    for (int i = 0; i < 4; i++)
    {
        if (header.format[i] != formatcheck[i])
        {
            printf("Wrong file format!\n");
            return 1;
        }
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    int blocksize = header.numChannels * (header.bitsPerSample / 8);
    return blocksize;
}
