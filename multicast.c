#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#import <math.h>

#define EXAMPLE_PORT 5006
#define EXAMPLE_GROUP "224.1.1.1"
#define source_iface "192.168.2.4"
#define Ping_pong_port  5007
#define Ping_pong_port2 5008


pthread_mutex_t lock;
int servevies[3];
int num_servevies = 0;

int registe(int svcid){
   pthread_mutex_lock(&lock);
   while(num_servevies >= 3){}

   servevies[num_servevies] = svcid;
   num_servevies++;
   pthread_mutex_unlock(&lock);
   return 0;
}

int unregister(int svcid){
   for(int i = 0; i < num_servevies; i++){
      if(servevies[i] == svcid){
         servevies[i] = 0;
         num_servevies--;
         return 0;
      }
   }
}

int find_service(int svcid){
   for(int i = 0; i < num_servevies; i++){
      if(servevies[i] == svcid){
         return 1;
      }
   }
   return 0;
}

void multicast(){
   struct sockaddr_in addr,addr2;
   int addrlen,addr2len, sock, cnt;
   struct ip_mreq mreq;
   char message[50], message2[50]={0};

   /* set up socket */
   sock = socket(AF_INET, SOCK_DGRAM, 0);
   if (sock < 0) {
     perror("socket");
     exit(1);
   }
   bzero((char *)&addr, sizeof(addr));
   addr.sin_family = AF_INET;
   addr.sin_addr.s_addr = INADDR_ANY;
   addr.sin_port = htons(EXAMPLE_PORT);
   addrlen = sizeof(addr);

   bzero((char *)&addr2, sizeof(addr2));
   addr2.sin_family = AF_INET;
   addr2.sin_addr.s_addr = INADDR_ANY;
   addr2.sin_port = htons(5005);
   addr2len = sizeof(addr2);


   /* receive */
   if (bind(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0) {        
      perror("bind");
      exit(1);
   }   

   char *ptr = strtok(source_iface, ",");
   while (ptr) { 
   mreq.imr_multiaddr.s_addr = inet_addr(EXAMPLE_GROUP);         
      mreq.imr_interface.s_addr = inet_addr(ptr);        
      if (setsockopt(sock, IPPROTO_IP, IP_ADD_MEMBERSHIP,
            &mreq, sizeof(mreq)) < 0) {
            perror("setsockopt mreq");
            exit(1);
         }         
      ptr = strtok(NULL, ",");
   }
   while (1) {
      cnt = recvfrom(sock, message, sizeof(message), 0, 
      (struct sockaddr *) &addr, &addrlen);
      if (cnt < 0) {
         perror("recvfrom");
         exit(1);
      } else if (cnt == 0) {
         break;
      }
      printf("%s: message = \"%s\"\n", inet_ntoa(addr.sin_addr), message);
      if (find_service(atoi(message))) {
         strcpy(message2,"1_1_1");  
      }
      else {
         strcpy(message2,"1_1_0");
      }
      addr2.sin_addr.s_addr = inet_addr(inet_ntoa(addr.sin_addr));
      printf("sending: %s\n", message2);
      cnt = sendto(sock, message2, sizeof(message2), 0,
               (struct sockaddr *) &addr2, addr2len);
      if (cnt < 0) {
         perror("sendto");
         exit(1);
      }
      
      for (int i = 0; i < 50; i++) {
         message[i] = '\0';
      }
      sleep(5);
      printf("Send OK\n");
   }
   return 0;

}

void ping_pong(){

   struct sockaddr_in addr,addr2;
   int addrlen,addr2len, sock, cnt;
   struct ip_mreq mreq;
   char message[50], message2[50]={0};
   strcat(message2,"PONG");

   /* set up socket */
   sock = socket(AF_INET, SOCK_DGRAM, 0);
   if (sock < 0) {
     perror("socket");
     exit(1);
   }
   bzero((char *)&addr, sizeof(addr));
   addr.sin_family = AF_INET;
   addr.sin_addr.s_addr = INADDR_ANY;
   addr.sin_port = htons(Ping_pong_port);
   addrlen = sizeof(addr);

   bzero((char *)&addr2, sizeof(addr2));
   addr2.sin_family = AF_INET;
   addr2.sin_addr.s_addr = INADDR_ANY;
   addr2.sin_port = htons(Ping_pong_port2);
   addr2len = sizeof(addr2);


   /* receive */
   if (bind(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0) {        
      perror("bind");
      exit(1);
   }   

   char *ptr = strtok(source_iface, ",");
   while (ptr) { 
   mreq.imr_multiaddr.s_addr = inet_addr(EXAMPLE_GROUP);         
      mreq.imr_interface.s_addr = inet_addr(ptr);        
      if (setsockopt(sock, IPPROTO_IP, IP_ADD_MEMBERSHIP,
            &mreq, sizeof(mreq)) < 0) {
            perror("setsockopt mreq");
            exit(1);
         }         
      ptr = strtok(NULL, ",");
   }
   while (1) {
      cnt = recvfrom(sock, message, sizeof(message), 0, 
      (struct sockaddr *) &addr, &addrlen);
      if (cnt < 0) {
         perror("recvfrom");
         exit(1);
      } else if (cnt == 0) {
         break;
      }
      printf("%s: message = \"%s\"\n", inet_ntoa(addr.sin_addr), message);
      addr2.sin_addr.s_addr = inet_addr(inet_ntoa(addr.sin_addr));
      printf("sending: %s\n", message2);
      cnt = sendto(sock, message2, sizeof(message2), 0,
               (struct sockaddr *) &addr2, addr2len);
      if (cnt < 0) {
         perror("sendto");
         exit(1);
      }
      
      for (int i = 0; i < 50; i++) {
         message[i] = '\0';
      }
      sleep(5);
      printf("Send OK\n");
   }
}

int checksum(char str[], int lenth){
   int i,sum=0,x;
   for(i=0;i<lenth;i++){
      x = atoi(str[i]);
      sum+=floor(log2(x)/log2(2))+1;
   }
   return sum;
}
