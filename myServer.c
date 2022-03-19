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
#include <math.h>
#include <errno.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "header.h"


int x;

void get_input (char *buf, char *msg) 
{
    printf("%s", msg);
    fgets(buf, BUF_LEN, stdin);
    // Remove the newline.
    buf[strcspn(buf, "\n")] = '\0'; 
}

// Populate a `sockaddr_in` struct with the IP / port to connect to.
void fill_sockaddr(struct sockaddr_in *sa, char *ip, int port) 
{
    // Set all of the memory in the sockaddr to 0.
    memset(sa, 0, sizeof(struct sockaddr_in));

    // IPv4.
    sa->sin_family = AF_INET;
    sa->sin_port = htons(port);
    inet_pton(AF_INET, ip, &(sa->sin_addr));
}

// Populates a client_info struct from a `sockaddr_in`.
Info_t get_client_info(struct sockaddr_in *sa) 
{
    Info_t info = {};
    info.port = ntohs(sa->sin_port);
    inet_ntop(sa->sin_family, &(sa->sin_addr), info.host, INET_ADDRSTRLEN);

    return info;
}

// A wrapper for the recvfrom function.
// The `who` parameter will be "send" or "recv", so that we can see which thread called the function.
int recv_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_from, socklen_t *from_len, char *who) 
{

    char name[BUF_LEN] = {0};

    printf("[%s] Receiving...\n", who);
    int numbytes = recvfrom(fd, buf, BUF_LEN, 0,
        (struct sockaddr *) sockaddr_from, from_len);

    buf[numbytes] = '\0';
    buf[strcspn(buf, "\n")] = '\0';

    Info_t client = get_client_info(sockaddr_from);

    printf("[%s] Received %d bytes from %s: %s\n", who, numbytes,
            print_client_buf(&client, name), buf);

    return numbytes;
}

// A wrapper for the sendto function.
// The `who` parameter will be "send" or "recv", so that we can see which thread called the function.
int send_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_to, socklen_t *to_len, char *who) 
{
    char name[BUF_LEN] = {0};

    int numbytes = sendto(fd, buf, strlen(buf), 0, (struct sockaddr *) sockaddr_to, *to_len);

    struct client_info client = get_client_info(sockaddr_to);

    printf("[%s] Sent %d bytes to %s: %s\n", who, numbytes, print_client_buf(&client, name), buf);

    return numbytes;

}


void *recv_handler(void *arguments) 
{
    Args_t *args;
    List_t *list;
    Node_t *node;
    int server_fd;

    // Array that we'll use to store the data we're sending / receiving.
    char buf[BUF_LEN + 1] = {0};

    // Create the sockaddr that the server will use to receive data from the client (and to then send data back).
    struct sockaddr_in sockaddr_from;

    // Stores the length of the sockaddr we're using here.
    socklen_t from_len = sizeof(sockaddr_from);

    args = (Args_t *) arguments;
    list = args->list;
    server_fd = args->fd;

    while (1) 
    {
        // The `recv_wrapper` function wraps the call to recv, to avoid code duplication.
        recv_wrapper(server_fd, buf, &sockaddr_from, &from_len, "recv");

        // Create a struct with the information about the client (host, port).
        Info_t client = get_client_info(&sockaddr_from);

        // Get the lock.
        printf("[recv] Waiting on the mutex...\n");
        pthread_mutex_lock(&(list->mutex));
        printf("[recv] Locked the mutex!\n");

        printf("[recv] Received request from %s listening at %d: %s\n", client.host, client.port, buf);

        if (!strcmp(buf, "Subscribe"))
        {
            list_add(list, &client);
            strcpy(buf, "Subscription successful");

        } 
        else if (!strcmp(buf, "Unsubscribe")) 
        {
            node = list_find(list, &client);
            if (node != NULL) 
            {
                list_remove_client(list, &client);
                strcpy(buf, "Subscription removed");
            } 
            else 
            {
                strcpy(buf, "You are not currently subscribed");
            }

        } 
        else 
        {
            strcpy(buf, "Unknown command, send Subscribe or Unsubscribe only");
        }

        // The `send_wrapper` function wraps the call to sendto, to avoid message duplication.
        send_wrapper(server_fd, buf, &sockaddr_from, &from_len, "recv");

        // Wake up one waiting thread.
        printf("[recv] signalling...\n");
        pthread_cond_signal(&(list->t_lock));
        printf("[recv] signaled\n");

        // Unlock the Mutex when finished.
        printf("[recv] unlocking the mutex...\n");
        pthread_mutex_unlock(&(list->mutex));
        printf("[recv] mutex unlocked!\n");
    }
}

void *send_handler(void *arguments) 
{
    Args_t *args;
    List_t *list;
    Node_t *curr;
    int client_fd;
    
    // Array that we'll use to store the data we're sending / receiving.
    char buf[BUF_LEN + 1] = {0};

    // Temporary array used to store the name of the client when printing.
    char name[BUF_LEN] = {0};

    args = (Args_t *) arguments;
    list = args->list;
    client_fd = args->fd;

    while (1) {

        // Get the lock.
        printf("[send] Waiting on the mutex...\n");
        pthread_mutex_lock(&(list->mutex));
        printf("[send] Locked the mutex!\n");

        print_list(list);

        // For each client:
        for (curr = list->head; curr != NULL; curr = curr->next) {
            printf("[send] Curr client is: %s\n", print_client_buf(curr->client, name));

            // We create a sockaddr_in to store the details of the
            // client we're replying to and fill it with the client's host/port info.
            struct sockaddr_in sockaddr_to = {0};
            socklen_t to_len = sizeof(sockaddr_to);
            fill_sockaddr(&sockaddr_to, curr->client->host, curr->client->port);

            printf("[send] Sending time to %s listening at %d\n", curr->client->host, curr->client->port);

            send_wrapper(client_fd, buf, &sockaddr_to, &to_len, "send");
        }

        // Wake up one waiting thread.
        printf("[send] signalling...\n");
        pthread_cond_signal(&(list->t_lock));
        printf("[send] signaled\n");

        // Unlock Mutex when finished.
        printf("[send] unlocking the mutex...\n");
        pthread_mutex_unlock(&(list->mutex));
        printf("[send] mutex unlocked!\n");

        printf("[send] sleeping...\n");
        sleep(1);

    }
}


void *prime()
{
    int *number, worker, i, flag;
    Args_t kati;

    worker = x + 1;
    kati.fd = worker;
    register_Server(worker);

    while (1)
    {                     
        number = (int*)recv_handler(&kati);
        flag =1;

        // Iterate from 2 to sqrt(n)
        for (i = 2; i <= sqrt(*number); i++)
        {
            // If the Number is Divisible by any Number between 2 and n/2, it is not Prime
            if (*number % i == 0)
            {
                flag = 0;
                break;
            }
        }

        if (*number <= 1)
        {
            flag = 0; 
        }

        // If the Number is Prime, send 1. 
        if (flag)
        {
            send_handler((void *)1);
        } 
        // If it is not Prime, send 0.    
        else
        {
            send_handler((void *)0);//send 0
        }         
    }
    unregister_Server(worker);
    printf("Seeeeeeee meee\n");  

    return 0;
}


int main(int argc, char *argv[])
{

    // Create the server's socket.
    // First parameter indicates that the netwrork uses IPv4.
    // Second parameter means we use a UDP Socket.
    // Third parameter returns a file descriptor for our Socket.
    int server_fd = socket(AF_INET, SOCK_DGRAM, 0);
    int client_fd = socket(AF_INET, SOCK_DGRAM, 0);

    x= 0;

    // Create the sockaddr that the server will use to send data to the client.
    struct sockaddr_in sockaddr_to;
    fill_sockaddr(&sockaddr_to, SERVER_IP, SERVER_PORT);

    // Let the server reuse the port if it was recently closed.
    const int so_reuseaddr = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &so_reuseaddr, sizeof(int));

    printf("Binding...\n");
    bind(server_fd, (struct sockaddr *) &sockaddr_to, sizeof(sockaddr_to));

    // Create a new list, to keep track of the clients.
    List_t *list;
    list = list_new();

    // Create an `Args_t` struct for each thread with different port number.
    Args_t *server_info = new_args(list, server_fd);
    Args_t *client_info = new_args(list, client_fd);

    // Create the threads.
    pthread_t recv_thread;
    pthread_t send_thread;
    pthread_t multi_thread;
    pthread_t pingpong_thread;
    pthread_t prime_thread;

    pthread_create(&multi_thread, NULL, multicast, NULL);
    pthread_create(&pingpong_thread, NULL, ping_pong, NULL);
    pthread_create(&recv_thread, NULL, recv_handler, &server_info);
    pthread_create(&send_thread, NULL, send_handler, &client_info);
    pthread_create(&prime_thread, NULL, prime, NULL);

    while (1) {
        sleep(1);
    }

    // Close the sockets.
    close(server_fd);
    close(client_fd);

    // Clean up the threads.
    void **retval;
    
    pthread_join(recv_thread, retval);
    pthread_join(send_thread, retval);

    // Free the memory for the linked list of clients, the mutex and condition.
    list_destroy(list);

    return 0;
}
