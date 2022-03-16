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
#define BufferLen 1024


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

struct client_node
{
    Info_t client;
    Node_t next, prev;

};

struct client_list 
{
    Node_t head, tail;
    pthread_cond_t t_lock;
    pthread_mutex_t mutex;
};

struct client_info 
{
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

void file_create(Info_t client)
{
    // Substitute the file_path string
    // with full path of CSV file
    FILE* fp = fopen("file_path", "a+");
 
    // char ip[50];
    // int port;
 
    if (!fp) {
        // Error in file opening
        printf("Can't open file\n");
        return 0;
    }
 
    // // Asking user input for the
    // // new record to be added
    // printf("\nEnter Account Holder Name\n");
    // scanf("%s", );
    // printf("\nEnter Account Number\n");
    // scanf("%d", &port);
    // printf("\nEnter Available Amount\n");
    // scanf("%d", &service_id);
 
    // Saving data in file
    fprintf(fp, "%s, %d\n", client.host, client.port);
 
    printf("\nNew Client added to record\n");
 
    fclose(fp);

    return;
}

void file_out()
{
     // Substitute the full file path
    // for the string file_path
    FILE* fp = fopen("file_path", "r+");
 
    if (!fp)
        printf("Can't open file\n");
 
    else {
        // Here we have taken size of
        // array 1024 you can modify it
        char buffer[1024];
 
        int row = 0;
        int column = 0;
 
        while (fgets(buffer, 1024, fp)) 
        {
            column = 0;
            row++;
 
            // To avoid printing of column
            // names in file can be changed
            // according to need
            if (row == 1)
                continue;
 
            // Splitting the data
            char* value = strtok(buffer, ", ");
 
            while (value) {
                // Column 1
                if (column == 0) 
                {
                    printf("IP :");
                }
 
                // Column 2
                if (column == 1) 
                {
                    printf("\tPORT :");
                }

                printf("%s", value);
                value = strtok(NULL, ", ");
                column++;
            }
 
            printf("\n");
        }
 
        // Close the file
        fclose(fp);
    }
}

int size() 
{
    FILE* fl = fopen("file_path", "r");
    int j,size;

    j = fseek(fl, 0L, SEEK_END);
    if (j == -1) 
    {
        ferror(fl);
        perror("no fseek the argument file\n");
        fclose(fl);
        return -1;
    }

    size = ftell(fl);
    if (size == -1) 
    {
        ferror(fl);
        perror("no ftell argument file\n");
        fclose(fl);
        return -1;
    }
    rewind(fl);
    //j = fseek(fl, 0L, SEEK_SET);
    if (j == -1) 
    {
        ferror(fl);
        perror("no fseek the argument file\n");
        fclose(fl);
        return -1;
    }

    if (size != 0) 
    {
        return size;
    }
    return 0;
}

