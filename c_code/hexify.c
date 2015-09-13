/*
   hexify - binary to char* encoder
   Copyright (c) 2004, Chris Eagle
   
   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the Free
   Software Foundation; either version 2 of the License, or (at your option) 
   any later version.
   
   This program is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
   FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
   more details.
   
   You should have received a copy of the GNU General Public License along with 
   this program; if not, write to the Free Software Foundation, Inc., 59 Temple 
   Place, Suite 330, Boston, MA 02111-1307 USA
*/

#include <stdio.h>
#include <time.h>
#include <ctype.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

void usage() {
   fprintf(stderr, "usage: hexify [-a|-s] <input>\n");
   fprintf(stderr, "   -a output as array of char\n");
   fprintf(stderr, "   -j output as java byte array\n");
   fprintf(stderr, "   -c (default) output as C string\n");
   fprintf(stderr, "   -p output as perl string\n");
   fprintf(stderr, "   -y output as python string\n");
   fprintf(stderr, "   -r output as ruby string\n");
   exit(1);
}

typedef enum {ARRAY, JAVA, STRING, PERL, PYTHON, RUBY} type;

int doArray(int fd, char *name, int isJava) {
   int idx = 0, len, lines = 0;
   int total = 0;
   unsigned char ch;
   int lineLen = 8;
   printf(isJava ? "byte " : "char ");
   printf("%s[] = {", name);
   while (1) {
      len = read(fd, &ch, 1);
      if (len != 1) break;
      total++;
      if (idx == 0) {
         printf("\n   ");
      }
      printf("(%s)0x%02.2x, ", isJava ? "byte" : "char", ch);
      idx++;
      if (idx == lineLen) {
         idx = 0;
      }
   }
   printf("0\n}");
   return total;
}

int doString(int fd, char *name, int output) {
   int idx = 0, len, lines = 0;
   int total = 0;
   unsigned char ch;
   int lineLen = 16;
   switch (output) {
   case PERL:
      printf("my $%s = ", name);
      break;
   case PYTHON:
   case RUBY:
      printf("%s = ", name);
      break;
   default:
      printf("char %s[] = ", name);
      break;
   }
   while (1) {
      len = read(fd, &ch, 1);
      if (len != 1) break;
      total++;
      if (idx == 0) {
         if ((output == PERL) && lines > 0) {
            printf(" .");
         }
         else if ((output == RUBY) && lines > 0) {
            printf(" \\");
         }
         else if ((output == PYTHON) && lines > 0) {
            printf(" + \\");
         }
         printf("\n   \"");
         lines++;
      }
      printf("\\x%02.2x", ch);
      idx++;
      if (idx == lineLen) {
        printf("\"");
         idx = 0;
      }
   }
   if (idx) {
      printf("\"");
   }
   return total;
}

int main(int argc, char **argv) {
   int fd;
   int total = 0;
   int idx = 0, len;
   unsigned char ch;
   char *ptr;
   int asString = 1;
   int fileArg = 1;
   int lineLen = 16;
   int output = STRING;
   if (argc != 2 && argc != 3) {
      usage();
   }
   if (argc == 3) {
      if (strcmp(argv[1], "-c") == 0) {
      }
      else if (strcmp(argv[1], "-a") == 0) {
         asString = 0;
         output = ARRAY;
      }
      else if (strcmp(argv[1], "-j") == 0) {
         asString = 0;
         output = JAVA;
      }
      else if (strcmp(argv[1], "-p") == 0) {
         output = PERL;
      }
      else if (strcmp(argv[1], "-y") == 0) {
         output = PYTHON;
      }
      else if (strcmp(argv[1], "-r") == 0) {
         output = RUBY;
      }
      else {
         usage();
      }
      fileArg = 2;
      lineLen = 6;
   }
   fd = open(argv[fileArg], O_RDONLY);
   if (fd < 0) {
      fprintf(stderr, "open failed: %s\n", argv[1]);
      exit(1);
   }
   ptr = strchr(argv[fileArg], '.');
   if (ptr) *ptr = 0;
   ptr = strrchr(argv[fileArg], '/');
   ptr = ptr ? ptr + 1 : argv[fileArg];
   switch (output) {
   case STRING:
      total = doString(fd, ptr, output);
      break;
   case PERL:
      total = doString(fd, ptr, output);
      break;
   case ARRAY:
      total = doArray(fd, ptr, 0);
      break;
   case JAVA:
      total = doArray(fd, ptr, 1);
      break;
   case RUBY:
      total = doString(fd, ptr, output);
      break;
   case PYTHON:
      total = doString(fd, ptr, output);
      break;
   }
   if (output != PYTHON) {
      printf(";\n");
   }
   else {
      printf("\n");
   }

   switch (output) {
   case PERL: case RUBY: case PYTHON:
      printf("# total size: %d bytes\n", total);
      break;
   default:
      printf("// total size: %d bytes\n", total);
      break;
   }

   close(fd);     
}

