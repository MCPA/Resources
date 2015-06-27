/* Leander Metcalf
    2 Oct 2014
    Shellcode input must be in binary format ...
    
    gcc harness.c -o harness -fno-stack-protector
    ./harness <shellcode>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>

//If you are testing static shellcode
const char static_shellcode[] = "\xeb\xef";

int main (int argc, char **argv)
{
    struct stat sb;


    if (stat (argv[1], &shellcodebytes) == 0) {
        FILE *file = fopen(argv[1], "r");
        printf("Opening file %s\n", argv[1]);

    unsigned char *buffer = (unsigned char *) mmap (0, sb.st_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);

    fprintf(stderr, "mmap ptr: %p\n", buffer);

    fread(buffer, 1, sb.st_size, file);
    fclose(file);

    void (*foo)() = (void*)buffer;
    foo();
}
    return 0;
} 
