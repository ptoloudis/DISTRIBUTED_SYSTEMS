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
#include <ncurses.h>

#define SERVER_IP "127.0.0.1" ////?????????
#define SERVER_PORT 12000
#define UPDATE_INTERVAL 1
#define BUF_LEN 1024


#define EXAMPLE_PORT 5006
#define EXAMPLE_GROUP "224.1.1.1"
#define source_iface "192.168.2.4"
#define Ping_pong_port  5007
#define Ping_pong_port2 5008


typedef struct arguments Args_t;
typedef struct client_node Node_t;
typedef struct client_list List_t;
typedef struct client_info Info_t;

// Arguments struct (and creation function) to pass the required info
// into the thread handlers.

struct client_info 
{
    char host[INET_ADDRSTRLEN];
    int port;
};

struct client_node
{
    Info_t *client;
    Node_t *next, *prev;

};

struct client_list 
{
    Node_t *head, *tail;
    pthread_cond_t t_lock;
    pthread_mutex_t mutex;
};

struct arguments {
    List_t *list;
    int fd;
};






Args_t *new_args(List_t *list, int fd);



///////////////
void print_client(Info_t *client);

char *print_client_buf(Info_t *client, char *buf);

void print_list(List_t *list);

List_t *list_new(void);

Node_t *new_node(Info_t *client);

void list_add_node(List_t *list, Node_t *node);

void list_add(List_t *list, Info_t *client);
// Returns the node, or NULL if not found.
Node_t *list_find(List_t *list, Info_t *client);

void node_destroy(Node_t *node);

void list_remove_client(List_t *list, Info_t *client);

void list_remove(List_t *list, Node_t *to_remove);

void list_destroy(List_t *list);

void file_create(Info_t *client);

void file_out();

int size() ;


///////////////////////////




int registe(int svcid);

int unregister(int svcid);

int find_service(int svcid);

void *multicast();

void *ping_pong();

int checksum(char str[], int lenth);
