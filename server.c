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
#include "header.h"
#include <fcntl.h>
#include <sys/stat.h>
#include <signal.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
struct sockaddr_in sockaddr_server;
int received = 0;
int sent = 0;
int to_send = 0;
Info_t receive_buf[BUF_LEN];
Info_t send_buf[BUF_LEN];

void *receiver(void *arg)
{
    int sockfd = *(int *)arg;
    char buffer[1024];
    Info_t *info;
    socklen_t from_len;
    from_len = sizeof(sockaddr_server);


    printf("sag%s\n", buffer);
    while(recvfrom(sockfd, (void *)buffer, BUF_LEN, MSG_WAITALL, (struct sockaddr*)&sockaddr_server,  &from_len) > 0)
    {

        printf("Received\n");
        info = (Info_t *) malloc(sizeof(Info_t));
        if(info == NULL)
        {
            perror("malloc");
            exit(1);
        }
        pthread_mutex_lock(&mutex);
        memset(info->buffer, '\0', sizeof(info->buffer));
        strcpy(info->buffer, buffer);
        info->client_addr = sockaddr_server;
        info->client_addr_len = from_len;
        receive_buf[received % BUF_LEN] = *info;
        pthread_mutex_unlock(&mutex);
        received++;
        memset(buffer, '\0', sizeof(buffer));
        // printf("sag%s\n", buffer);
    }
    return NULL;
}


void *sender(void *arg){
    int sockfd = *(int *)arg;
    int n;
    Info_t *info;

    while(1){
        while(sent >= to_send );
        pthread_mutex_lock(&mutex);
        info = &send_buf[sent % BUF_LEN];
        printf("Sending %s\n", info->buffer);
        n = sendto(sockfd, info->buffer, strlen(info->buffer), MSG_WAITALL, (struct sockaddr*)&info->client_addr, info->client_addr_len);
        if(n < 0)
        {
            perror("sendto");
            exit(1);
        }
        pthread_mutex_unlock(&mutex);
        printf("Sent %d bytes\n", n);
        sent++;
    }
    return NULL;
}

void *execute_command(void *arg){

    chdir((char *) arg);

    int received_data = 0;
    char buffer[1024];
    Info_t *info;
    FILE *my_fd;
    int fd, seek, size;
    int magic_number, reboot_number, my_reboot;
    char message[1024];
    char command;
    char *token = NULL;
    char tmp[1024], temp[1024];
    char path[1024];
    int flag;
    int offset = 0, last_modified = 0;
    
    mynfs_init();

    my_fd = fopen("reboot.txt", "r+");
    if(my_fd == NULL)
    {
        perror("fopen");
        exit(1);
    }
    my_reboot = 0;

    fscanf(my_fd, "%d", &my_reboot);
    fseek(my_fd, 0, SEEK_SET);
    fprintf(my_fd, "%d", my_reboot + 1);
    fclose(my_fd);

    while(1){
        while(received_data >= received);
        info = &receive_buf[received_data % BUF_LEN];
        received_data++;
        memset(buffer,'\0', sizeof(buffer));
        strcpy(buffer, info->buffer);

        printf("Received %s\n", buffer);
        sscanf(buffer,"%d %c %d#", &magic_number, &command, &reboot_number);
        sprintf(temp,"%d %c %d#", magic_number, command, reboot_number);
        
        token = strtok(buffer, temp);
        memset(tmp, '\0', sizeof(tmp));
        while (token != NULL)
        {
            strcat (tmp, token);
            strcat (tmp, " ");
            token = strtok(NULL, " ");
        }
        

        switch (command)
        {
        case 'o':
            /* Open - Find file in Disk */
            memset(path,'\0', sizeof(path));
            sscanf(tmp, "%s %d", path , &flag);
            printf("Open %s\n", path);
            token = nfs_open(path, flag);
            sprintf(message, "%d#%d.%s", magic_number, my_reboot, token);
            break;
        case 'r':
            if (reboot_number != my_reboot)
            {
                sprintf(message, "%s", "Reboot");   
                break;
            }
            /* Read from Disk */
            sscanf(tmp, "%d %d %d", &fd, &seek, &size);
            token = nfs_read(fd, buffer, strlen(buffer), offset);
            sprintf(message, "%d#%d.%s", magic_number, my_reboot, token);
            break;
        case 'w':
            /* Write to Disk */
            if (reboot_number != my_reboot)
            {
                sprintf(message, "%s", "Reboot");   
                break;
            }
            sscanf(tmp, ".%d %d", &fd, &seek);
            sprintf(temp, ".%d %d ",fd, seek);
            printf("%d, %d\n", fd, seek);
            token = strtok(tmp,temp);
            if (!strcmp(token,"$#trun#$"))
            {
               token = nfs_ftruncate(fd, token,(off_t) seek); 
            }
            else
            {
                // printf("Write %s\n", token);
                printf(" tmp %d\n", seek);
                token = nfs_write(fd, token, strlen(token), seek);
            }
            sprintf(message, "%d#%d.%s", magic_number, my_reboot, token);
            break;

        case 'n':
            if (reboot_number != my_reboot)
            {
                sprintf(message, "%s", "Reboot");   
                break;
            }   
            token = nfs_mod(fd, last_modified);
            sprintf(message, "%d#%d.%s", magic_number, my_reboot, token);
            break;
        
        default:
            break;
        }
        pthread_mutex_lock(&mutex);
        int x = to_send % BUF_LEN;
        memset(info->buffer, '\0', sizeof(info->buffer));
        strcpy(info->buffer, message);
        send_buf[x] = *info;
        pthread_mutex_unlock(&mutex);
        to_send++;
    }
}


int main(int argc, char *argv[])
{

    //Configure Path for Files Server can Access
    if(argv[1] != NULL)
    {
        chdir(argv[1]);
    }
    else
    {
        perror("Specifiy a path to the files you want to access\n");
        exit(1);
    }


    // Create the server's socket.
    // First parameter indicates that the netwrork uses IPv4.
    // Second parameter means we use a UDP Socket.
    // Third parameter returns a file descriptor for our Socket.
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0){
        perror("ERROR opening socket");
        exit(1);
    }
    
    int err = -1;

    // Create the sockaddr that the server will use to send data to the client.
        
    // Set Socket Options
    int optval = 1;
    err = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
    if(err < 0){
        perror("ERROR setting socket options");
        exit(1);
    }

    sockaddr_server.sin_family = AF_INET;
    sockaddr_server.sin_addr.s_addr = htonl(INADDR_ANY);
    sockaddr_server.sin_port = htons(CLIENT_PORT);

    printf("Binding...\n");
    err = bind(sockfd, (struct sockaddr *) &sockaddr_server, sizeof(sockaddr_server));
    if (err < 0){
        perror("ERROR on binding");
        exit(1);
    }
    printf("Binding done.\n");

    // Create the threads.
    pthread_t recv_thread;
    pthread_t send_thread;
    pthread_t execute_command_thread;
    

    pthread_create(&recv_thread, NULL, receiver,(void *)&sockfd);
    pthread_create(&send_thread, NULL, sender,(void *)&sockfd);
    pthread_create(&execute_command_thread, NULL, execute_command, (void *)&argv[1]);

    char s[7];
    while (1) {
        scanf("%s", s);
        if (!strcmp(s, "reboot")) {
            break;
        }
    }

    // Close the sockets.
    close(sockfd);
    

    // Clean up the threads.
    
    pthread_kill(recv_thread, SIGKILL);
    pthread_kill(send_thread, SIGKILL);
    pthread_kill(execute_command_thread, SIGKILL);

    return 0;
}



// #TODO: Encoding and Decoding
// #TODO: Debugging
// #TODO: Error handling
// #TODO: Test Files
// #TODO: 