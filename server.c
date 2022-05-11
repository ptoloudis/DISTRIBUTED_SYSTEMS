/*
Team : 1
Names : Apostolopoulou Ioanna & Toloudis Panagiotis
AEM : 03121 & 02995
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
//#include "header.h"
#include <fcntl.h>


/********************** DEFINITIONS **********************/

#define SERVER_IP "192.168.68.197" 
#define SERVER_PORT 12000
#define CLIENT_PORT 12001
#define BUF_LEN 1024

typedef struct client_info
{
    char buffer[BUF_LEN];
    struct sockaddr *client_addr;
    socklen_t client_addr_len;
}Info_t;

/********************** GLOBALS **********************/
volatile int received = 0;
volatile int sent = 0;
Info_t *receive_buf[BUF_LEN];
Info_t *send_buf[BUF_LEN];


void *receiver(void *arg)
{
    int sockfd = *(int *)arg;
    int n;
    char buffer[1024];
    Info_t *info;
    struct sockaddr *sockaddr_from;
    socklen_t from_len;
    from_len = sizeof(sockaddr_from);
    
    while((n = recvfrom(sockfd, buffer, BUF_LEN, 0, sockaddr_from, &from_len) > 0))
    {// if buf=ack recv ack
        info = (Info_t *) malloc(sizeof(Info_t));
        if(info == NULL)
        {
            perror("malloc");
            exit(1);
        }
        strcpy(info->buffer, buffer);
        info->client_addr = sockaddr_from;
        info->client_addr_len = from_len;
        receive_buf[received % BUF_LEN] = info;
        received++;
        /// ACK? send ACK
        printf("Received %d bytes\n", n);
    }
    return NULL;
}


void *sender(void *arg){
    int sockfd = *(int *)arg;
    int n;
    char buffer[1024];
    Info_t *info;

    while(1){
        while(sent >= received);
        info = send_buf[sent % BUF_LEN];
        n = sendto(sockfd, info->buffer, strlen(info->buffer), 0, info->client_addr, info->client_addr_len);
        if(n < 0)
        {
            perror("sendto");
            exit(1);
        }
        /// ACK ? RECEIVE ACK
        free(info);
        sent++;
        printf("Sent %d bytes\n", n);
    }
    return NULL;
}

void *ping_pong(void *arg){
    int sockfd = *(int *)arg;
    int received_data = 0;
    int sent_data = 0;
    char buffer[1024];
    Info_t *info;
    int fd;
    int flags[5] = {0};
    int *ptr = flags;

    flags[0] = O_CREAT;
    flags[1] = O_WRONLY;
    flags[2] = O_EXCL;
    flags[3] = O_TRUNC;
    flags[4] = O_RDONLY;
    flags[5] = O_RDWR;

    while(1){
        while(received_data >= received);
        info = receive_buf[received_data % BUF_LEN];
        received_data++;
        strcat(buffer, info->buffer);

        int command;
        switch (command)
        {
        case 1:
            /* Write in Disk */
            write(fd, buffer, strlen(buffer));
            break;
        case 2:
            /* Read from Disk */
            read(fd, buffer, strlen(buffer));
            break;
        case 3:
            /* Truncate file in Disk */
            truncate(&fd, strlen(buffer));
            break;
        case 4:
            /* Open - Find file in Disk */
            
            for(int i = 0; i < 5; i++)
            {
                open(buffer, flags[i]);
            }
            break;
        
        default:
            break;
        }
        ///
        /*
        switch case 
        o (open)*/
        strcat(info->buffer, buffer);
        send_buf[sent_data % BUF_LEN];
    }
}



int main(int argc, char *argv[])
{
    // Create the server's socket.
    // First parameter indicates that the netwrork uses IPv4.
    // Second parameter means we use a UDP Socket.
    // Third parameter returns a file descriptor for our Socket.
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0){
        perror("ERROR opening socket");
        exit(1);
    }
    
    struct sockaddr_in sockaddr_server = {0};
    int err = -1;

    // Create the sockaddr that the server will use to send data to the client.
    struct sockaddr_in *sockaddr_to;
    //fill_sockaddr(&sockaddr_to, SERVER_IP, SERVER_PORT);

    memset(&sockaddr_server, 0, sizeof(sockaddr_server));
    sockaddr_server.sin_family = AF_INET;
    sockaddr_server.sin_addr.s_addr = htonl(INADDR_ANY);
    sockaddr_server.sin_port = htons(CLIENT_PORT);


    // Set Socket Options
    int optval = 1;
    err = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
    if(err < 0){
        perror("ERROR setting socket options");
        exit(1);
    }

    printf("Binding...\n");
    err = bind(sockfd, (struct sockaddr *) &sockaddr_to, sizeof(sockaddr_to));
    if (err < 0){
        perror("ERROR on binding");
        exit(1);
    }
    printf("Binding done.\n");

    // Create the threads.
    pthread_t recv_thread;
    pthread_t send_thread;
    

    //pthread_create(&pingpong_thread, NULL, ping_pong, NULL);
    pthread_create(&recv_thread, NULL, receiver, NULL);
    pthread_create(&send_thread, NULL, sender, NULL);

    while (1) {
        sleep(1);
    }

    // Close the sockets.
    close(sockfd);
    

    // Clean up the threads.
    void **retval;
    
    pthread_join(recv_thread, retval);
    pthread_join(send_thread, retval);


    return 0;
}
