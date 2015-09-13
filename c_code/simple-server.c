#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define SERVER_PORT 25

int main(int argc, char **argv) {

   int sock;
   struct sockaddr_in my_addr, ca;
   int ca_len = sizeof(ca);


   memset(&my_addr, 0, sizeof(my_addr));
   //my_addr.sin_addr is 0.0.0.0 now
   my_addr.sin_family = AF_INET;
   my_addr.sin_port = htons(SERVER_PORT);

   sock = socket(AF_INET, SOCK_STREAM, 0);

   if (bind(sock, (struct sockaddr*)&my_addr, sizeof(my_addr))) exit(1);

   if (listen(sock, 10)) exit(1);

   while (1) {
      int client = accept(sock, (struct sockaddr*)&ca, &ca_len);
      if (client != -1) {
         char buf[256];
         //examine ca for client IP and port info
         char helo[] = "220 socket.demo.net ESMTP\r\n";
         send(client, helo, strlen(helo), 0);
         int len = recv(client, buf, 256, 0);
         if (len > 0) write(1, buf, len);
         char bye[] = "221 Bye\r\n";
         send(client, bye, strlen(bye), 0);
         close(client);
      }
   }
}
