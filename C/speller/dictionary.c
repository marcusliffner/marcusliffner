// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table? is it not 26?
const unsigned int N = 26;

unsigned int words;
unsigned int hashvalue;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // done
    hashvalue = hash(word);
    node *cursor = table[hashvalue];

    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // done
    long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // done ( i think )
    FILE *file = fopen(dictionary, "r");
    // if file cant open
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    // makes new node
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new = malloc(sizeof(node));

        // return False if null
        if (new == NULL)
        {
            return false;
        }

        strcpy(new->word, word);
        hashvalue = hash(word);
        new->next = table[hashvalue];
        table[hashvalue] = new;
        words++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Done
    if (words > 0)
    {
        return words;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // done
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
