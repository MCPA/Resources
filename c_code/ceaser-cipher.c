#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROTATION 9

#define caesar(x) rot(ROTATION, x)
#define decaesar(x) rot((26-ROTATION), x)

void rot(int c, char *str)
{
	int l = strlen(str);
	const char *alpha[2] = { "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"};

	int i;
	for (i = 0; i < l; i++)
	{
		if (!isalpha(str[i]))
			continue;

		str[i] = alpha[isupper(str[i])][((int)(tolower(str[i])-'a')+c)%26];
	}
}


int main(int argc, char **argv)
{
	char str[] = "This is a top secret text message!";

	printf("Original: %s\n", str);
	caesar(str);
	printf("Encrypted: %s\n", str);
	decaesar(str);
	printf("Decrypted: %s\n", str);


	return 0;
}
