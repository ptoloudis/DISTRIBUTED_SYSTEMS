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

#define SERVER_IP "127.0.0.1" ////?????????
#define SERVER_PORT 12000
#define UPDATE_INTERVAL 1
#define BufferLen 1024

// // Handlers for the sending and receiving threads.
// int receive_handler(void *info);
// int send_handler(void *info);


///////////////////////////////// MINE ///////////////////////////////////////////////////


typedef struct arguments Args_t;
typedef struct client_node Node_t;
typedef struct client_list List_t;
typedef struct client_info Info_t;

// Arguments struct (and creation function) to pass the required info
// into the thread handlers.
struct arguments {
    List_t list;
    int fd;
};

struct client_list {
    Node_t head, tail;
    pthread_cond_t t_lock;
    pthread_mutex_t mutex;
};

struct client_info {
    char host[INET_ADDRSTRLEN];
    int port;
};



Args_t new_args(List_t list, int fd) 
{
    Args_t args;

    args = calloc(1, sizeof(*args));
    args->list = list;
    args->fd = fd;

    return args;
}


////////////////////////////////////////////////////////////////////////
// Socket helper functions

// // Wrapper for the recv function, to avoid code duplication.
// int receive_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_from,
//         socklen_t *from_len, char *who);

// // Wrapper for the sendto function, to avoid code duplication.
// int send_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_to,
//         socklen_t *to_len, char *who);

// // Get a client_info struct based on the sockaddr we're communicating with.
// struct client_info get_client_info(struct sockaddr_in *sa);

// // Get the "name" (IP address) of who we're communicating with.
// char *get_name(struct sockaddr_in *sa, char *name);

// // Populate a sockaddr_in struct with the specified IP / port to connect to.
// void fill_sockaddr(struct sockaddr_in *sa, char *ip, int port);

// // A wrapper function for fgets, similar to Python's built-in 'input' function.
// void get_input(char *buf, char *msg);

// "Print" out a client, by copying its host/port into the specified buffer.
//char *print_client_buf(struct client_info client, char *buf);

///////////////
void print_client(Info_t client) {
    printf("%s:%d\n", client.host, client.port);
}

char *print_client_buf(Info_t client, char *buf) {
    sprintf(buf, "%s:%d", client.host, client.port);
    return buf;
}

void print_list(List list) 
{
    printf("---------------\n");
    printf("Clients are: \n");

    char name[BUF_LEN] = {0};
    Node_t curr = NULL;
    for (curr = list->head; curr != NULL; curr = curr->next) {
        printf("%s -> ", print_client_buf(curr->client, name));
    }

    printf("X\n");
    printf("---------------\n");

}

List_t list_new(void) 
{
    List_t list = calloc(1, sizeof(*list));

    pthread_cond_init(&list->t_lock);
    pthread_mutex_init(&list->mutex, NULL);

    return list;
}

Node_t new_node(Info_t client) 
{
    Node_t node = calloc(1, sizeof(*node));
    node->client = client;
    return node;
}

void list_add_node(List list, Node node) 
{
    assert(list != NULL);

    if (list->tail == NULL) 
    {
        assert(list->head == NULL);
        list->head = list->tail;
        list->tail = node;
    } 
    else 
    {
        assert(list->head != NULL);
        list->tail->next = node;
        node->prev = list->tail;
        list->tail = node;
    }
}

void list_add(List_t list, Info_t client) 
{
    printf("Adding a client: "); 
    print_client(client);
    Node_t new = new_node(client);
    list_add_node(list, new);
}

// Returns the node, or NULL if not found.
Node_t list_find(List_t list, Info_t client) {
    assert(list != NULL);

    Node_t found = NULL;
    Node_t curr = NULL;

    for (curr = list->head; curr != NULL; curr = curr->next) 
    {
        if (clients_equal(curr->client, client)) 
        found = curr;
    }
    return found;
}

void node_destroy(Node_t node) {
    free(node);
}

void list_remove_client(List_t list, Info_t client) 
{
    printf("Removing a client: "); 
    print_client(client);

    Node_t to_remove = list_find(list, client);
    list_remove(list, to_remove);
}

void list_remove(List list, Node to_remove) 
{
    if (to_remove == NULL) {
        fprintf(stderr, "Tried to remove a node that wasn't in the list!");
        return;
    }

    if (list->head == to_remove) {
        assert(to_remove->prev == NULL);
        list->head = to_remove->next;
    }

    if (list->tail == to_remove) {
        assert(to_remove->next == NULL);
        list->tail = to_remove->prev;
    }

    if (to_remove->next) to_remove->next = to_remove->next->next;
    if (to_remove->prev) to_remove->prev = to_remove->prev->prev;

    node_destroy(to_remove);

}

void list_destroy(List_t list) 
{
    Node_t curr = NULL;
    Node_t tmp = NULL;

    for (curr = list->head; curr != NULL;) 
    {
        tmp = curr;
        curr = curr->next;
        node_destroy(tmp);
    }

    pthread_mutex_destroy(&list->mutex);
    pthread_cond_destroy(&list->t_lock);

    free(list);
}

/////Socket

void get_input (char *buf, char *msg) {
    printf("%s", msg);
    fgets(buf, BUF_LEN, stdin);
    buf[strcspn(buf, "\n")] = '\0'; // Remove the newline
}

// Populate a `sockaddr_in` struct with the IP / port to connect to.
void fill_sockaddr(struct sockaddr_in *sa, char *ip, int port) {

    // Set all of the memory in the sockaddr to 0.
    memset(sa, 0, sizeof(struct sockaddr_in));

    // IPv4.
    sa->sin_family = AF_INET;
    sa->sin_port = htons(port);
    inet_pton(AF_INET, ip, &(sa->sin_addr));
}

// Populates a client_info struct from a `sockaddr_in`.
Info_t get_client_info(struct sockaddr_in *sa) {
    struct client_info info = {};
    info.port = ntohs(sa->sin_port);
    inet_ntop(sa->sin_family, &(sa->sin_addr), info.host, INET_ADDRSTRLEN);

    return info;
}

// Get the "name" (IP address) of who we're communicating with.
// Takes in an array to store the name in.
// Returns a pointer to that array for convenience.
char *get_name(struct sockaddr_in *sa, char *name) {
    inet_ntop(sa->sin_family, &(sa->sin_addr), name, BUF_LEN);
    return name;
}

// A wrapper for the recvfrom function.
// The `who` parameter will be "send" or "recv", to make the output
// clearer (so that you can see which thread called the function).
int recv_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_from,
        socklen_t *from_len, char *who) {

    char name[BUF_LEN] = {0};

    printf("[%s] Receiving...\n", who);
    int numbytes = recvfrom(fd, buf, BUF_LEN, 0,
        (struct sockaddr *) sockaddr_from, from_len);

    buf[numbytes] = '\0';
    buf[strcspn(buf, "\n")] = '\0';

    Info_t client = get_client_info(sockaddr_from);

    printf("[%s] Received %d bytes from %s: %s\n", who, numbytes,
            print_client_buf(client, name), buf);

    return numbytes;
}

// A wrapper for the sendto function.
// The `who` parameter will be "send" or "recv", to make the output
// clearer (so that you can see which thread called the function).
int send_wrapper(int fd, char *buf, struct sockaddr_in *sockaddr_to,
        socklen_t *to_len, char *who) {

    char name[BUF_LEN] = {0};

    int numbytes = sendto(fd, buf, strlen(buf), 0,
            (struct sockaddr *) sockaddr_to, *to_len);

    struct client_info client = get_client_info(sockaddr_to);

    printf("[%s] Sent %d bytes to %s: %s\n", who, numbytes,
            print_client_buf(client, name), buf);

    return numbytes;

}


int recv_handler(void *arguments) 
{
    Args_t args;
    List_t list;
    int server_fd;
    // Array that we'll use to store the data we're sending / receiving.
    char buf[BUF_LEN + 1] = {0};

    // Create the sockaddr that the server will use to receive data from
    // the client (and to then send data back).
    struct sockaddr_in sockaddr_from;

    // We need to create a variable to store the length of the sockaddr
    // we're using here, which the recvfrom function can update if it
    // stores a different amount of information in the sockaddr.
    socklen_t from_len = sizeof(sockaddr_from);


    args = (Args_t) arguments;
    list = args->list;
    server_fd = args->fd;

    while (1) {

        // The `recv_wrapper` function wraps the call to recv, to avoid
        // code duplication.
        recv_wrapper(server_fd, buf, &sockaddr_from, &from_len, "recv");

        // Create a struct with the information about the client
        // (host, port) -- similar to "clientAddress" in the Python.
        Info_t client = get_client_info(&sockaddr_from);

        // THe `with t_lock:` in the python code is equivalent to
        // `t_lock.acquire()` -- it calls the `acquire` function to
        // lock the underlying lock.
        //
        // In C, the condition variable and the mutex are two separate
        // things to create and keep track of.
        //
        // To acquire the lock in C, we call `mtx_lock` on the mutex.

        // Get the lock.
        printf("[recv] Waiting on the mutex...\n");
        pthread_mutex_lock(&(list->mutex));
        printf("[recv] Locked the mutex!\n");

        printf("[recv] Received request from %s listening at %d: %s at time %s",
                client.host, client.port, buf, get_time());

        if (!strcmp(buf, "Subscribe")) {
            list_add(list, client);
            strcpy(buf, "Subscription successful");

        } else if (!strcmp(buf, "Unsubscribe")) {
            if (list_contains(list, client)) {
                list_remove_client(list, client);
                strcpy(buf, "Subscription removed");
            } else {
                strcpy(buf, "You are not currently subscribed");
            }

        } else {
            strcpy(buf, "Unknown command, send Subscribe or Unsubscribe only");
        }

        // The `send_wrapper` function wraps the call to sendto, to
        // avoid code duplication.
        send_wrapper(server_fd, buf, &sockaddr_from, &from_len, "recv");

        // Now that we're finished, we want to notify the waiting thread
        // and release the lock.

        // Wake up one waiting thread.
        // This is the equivalent of `t_lock.notify()` in the Python code:
        printf("[recv] signalling...\n");
        pthread_cond_signal(&(list->t_lock));
        printf("[recv] signaled\n");

        // And unlock the mutex now that we're done.
        // This is the equivalent of the end of the `with t_lock:` block
        printf("[recv] unlocking the mutex...\n");
        pthread_mutex_unlock(&(list->mutex));
        printf("[recv] mutex unlocked!\n");
    }

    return EXIT_SUCCESS;
}

int send_handler(void *arguments) 
{
    Args_t args;
    List_t list;
    int client_fd;

    // Array that we'll use to store the data we're sending / receiving.
    char buf[BUF_LEN + 1] = {0};

    // Temporary array used to store the name of the client when printing.
    char name[BUF_LEN] = {0};

    args = (Args_t) arguments;
    list = args->list;
    client_fd = args->fd;

    while (1) {

        // Get the lock.
        printf("[send] Waiting on the mutex...\n");
        pthread_mutex_lock(&(list->mutex));
        printf("[send] Locked the mutex!\n");

        print_list(list);

        // For each client:
        for (Node curr = list->head; curr != NULL; curr = curr->next) {

            // Get the current time.
            char *curr_time = get_time();
            snprintf(buf, BUF_LEN, "Current time is %s", curr_time);

            printf("[send] Curr client is: %s\n",
                    print_client_buf(curr->client, name));


            // We create a sockaddr_in to store the details of the
            // client we're replying to, and fill it with the client's
            // host/port from the client_info struct.
            struct sockaddr_in sockaddr_to = {0};
            socklen_t to_len = sizeof(sockaddr_to);
            fill_sockaddr(&sockaddr_to, curr->client.host, curr->client.port);

            printf("[send] Sending time to %s listening at %d at time %s\n",
                    curr->client.host, curr->client.port, curr_time);

            send_wrapper(client_fd, buf, &sockaddr_to, &to_len, "send");
        }

        // Wake up one waiting thread.
        // This is the equivalent of `t_lock.notify()` in the Python code:
        printf("[send] signalling...\n");
        pthread_cond_signal(&(list->t_lock));
        printf("[send] signaled\n");

        // And unlock the mutex now that we're done.
        // This is the equivalent of the end of the `with t_lock:` block
        printf("[send] unlocking the mutex...\n");
        pthread_mutex_unlock(&(list->mutex));
        printf("[send] mutex unlocked!\n");

        // sleep for UPDATE_INTERVAL
        printf("[send] sleeping...\n");
        sleep(UPDATE_INTERVAL);

    }
    return EXIT_SUCCESS;
}


int main(int argc, char *argv[]) {

    // Create the server's socket.
    //
    // The first parameter indicates the address family; in particular,
    // `AF_INET` indicates that the underlying network is using IPv4.
    //
    // The second parameter indicates that the socket is of type
    // SOCK_DGRAM, which means it is a UDP socket (rather than a TCP
    // socket, where we use SOCK_STREAM).
    //
    // This returns a file descriptor, which we'll use with our sendto /
    // recvfrom functions later.
    int server_fd = socket(AF_INET, SOCK_DGRAM, 0);
    int client_fd = socket(AF_INET, SOCK_DGRAM, 0);

    // Create the sockaddr that the server will use to send data to the
    // client.
    struct sockaddr_in sockaddr_to;
    fill_sockaddr(&sockaddr_to, SERVER_IP, SERVER_PORT);

    // Let the server reuse the port if it was recently closed and is
    // now in TIME_WAIT mode.
    const int so_reuseaddr = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &so_reuseaddr, sizeof(int));

    printf("Binding...\n");
    bind(server_fd, (struct sockaddr *) &sockaddr_to, sizeof(sockaddr_to));

    // Create a new list, to keep track of the clients.
    // The list struct also contains a mutex and a condition variable
    // (equivalent to Python's threading.Condition()).
    List_t list = list_new();

    // Create an args struct for each thread. Both structs have a
    // pointer to the same list, but different sockets (different file
    // descriptors).
    Args_t server_info = new_args(list, server_fd);
    Args_t client_info = new_args(list, client_fd);

    // Create the threads.
    pthread_t recv_thread;
    pthread_t send_thread;

    pthread_create(&recv_thread, recv_handler, (void *) server_info);
    pthread_create(&send_thread, send_handler, (void *) client_info);

    while (1) {
        // Equivalent to `sleep(0.1)`
        usleep(100000);
    }


    // This code will never be reached, but assuming there was some way
    // to tell the server to shutdown, this code should happen at that
    // point.

    // Close the sockets
    close(server_fd);
    close(client_fd);

    // Clean up the threads.
    int retval;
    
    pthread_join(recv_thread, &retval);
    pthread_join(send_thread, &retval);

    // Free the memory for the linked list of clients.
    // This also frees the mutex and condition.
    list_destroy(list);

    return 0;
}
