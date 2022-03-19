/*
Team : 1
Names : Apostolopoulou Ioanna & Toloudis Panagiotis
AEM : 03121 & 02995
*/

#include "header.h"
#include <math.h>

Args_t *new_args(List_t *list, int fd) 
{
    Args_t *args;

    args = calloc(1, sizeof(*args));
    args->list = list;
    args->fd = fd;

    return args;
}

// Function that Prints Client's Info (host, port).
void print_client(Info_t *client) {
    printf("%s:%d\n", client->host, client->port);
}

// Function that Prints Client's Buffer Info.
char *print_client_buf(Info_t *client, char *buf) {
    sprintf(buf, "%s:%d", client->host, client->port);
    return buf;
}

// Function that Prints the List of Clients.
void print_list(List_t *list) 
{
    printf("---------------\n");
    printf("Clients are: \n");

    char name[BUF_LEN] = {0};
    Node_t *curr = NULL;
    for (curr = list->head; curr != NULL; curr = curr->next) {
        printf("%s -> ", print_client_buf(curr->client, name));
    }
}

// Function Creates the List and Initializes the Mutex and Conditions.
List_t *list_new(void) 
{
    List_t *list = calloc(1, sizeof(*list));

    pthread_cond_init(&list->t_lock, NULL);
    pthread_mutex_init(&list->mutex, NULL);

    return list;
}

// Function that Creates a new Node for the List.
Node_t *new_node(Info_t *client) 
{
    Node_t *node = calloc(1, sizeof(*node));
    node->client = client;
    return node;
}

// Function that Adds the new Node in the List.
void list_add_node(List_t *list, Node_t *node) 
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

// Function that inserts Node and Info (host, port) in the List.
void list_add(List_t *list, Info_t *client) 
{
    printf("Adding a client: "); 
    print_client(client);
    Node_t *new = new_node(client);
    list_add_node(list, new);
}

// Returns the node, or NULL if not found.
Node_t *list_find(List_t *list, Info_t *client) {
    assert(list != NULL);

    Node_t *found = NULL;
    Node_t *curr = NULL;

    for (curr = list->head; curr != NULL; curr = curr->next) 
    {
        found = curr;
    }
    return found;
}

// Function to Free Nodes Memory.
void node_destroy(Node_t *node) {
    free(node);
}

// Function to Remove a Client from Buffer.
void list_remove_client(List_t *list, Info_t *client) 
{
    printf("Removing a client: "); 
    print_client(client);

    Node_t *to_remove = list_find(list, client);
    list_remove(list, to_remove);
}

//Function that Clears the whole Buffer.
void list_remove(List_t *list, Node_t *to_remove) 
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

// Function Frees the Memory used by the Buffer and Destroys the Mutex and Conditions.
void list_destroy(List_t *list) 
{
    Node_t *curr = NULL;
    Node_t *tmp = NULL;

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

void file_create(Info_t *client)
{
    // Substitute the file_path string
    // with full path of CSV file
    FILE* fp = fopen("file_path", "a+");
 
    // char ip[50];
    // int port;
 
    if (!fp) {
        // Error in file opening
        printf("Can't open file\n");
        return;
    }
 
    // Saving data in file
    fprintf(fp, "%s, %d\n", client->host, client->port);
 
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



///////////////////////////

pthread_mutex_t lock;
int services[3];
int num_of_services = 0;

int register_Server(int svcid)
{
    pthread_mutex_lock(&lock);
    while(num_of_services >= 3){}

    services[num_of_services] = svcid;
    num_of_services++;
    pthread_mutex_unlock(&lock);

    return 0;
}



int unregister_Server(int svcid)
{
    int i;
    for(i = 0; i < num_of_services; i++)
    {
      if(services[i] == svcid)
      {
        services[i] = 0;
        num_of_services--;
        return 0;
      }
   }
   return 0;
}

int find_service(int svcid)
{
    int i;
    for(i = 0; i < num_of_services; i++)
    {
      if(services[i] == svcid)
      {
        return 1;
      }
    }
   return 0;
}

void *multicast()
{
   struct sockaddr_in addr,addr2;
   int addr2len, sock, cnt;
   unsigned int addrlen;
   char message[50], message2[50]={0};

   // Set up Socket. 
   sock = socket(AF_INET, SOCK_DGRAM, 0);
   if (sock < 0) 
   {
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


   // Receive.
    if (bind(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0) 
    {        
        perror("bind");
        exit(1);
    }   

    while (1) 
    {
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

void *ping_pong()
{

   struct sockaddr_in addr,addr2;
   int addr2len, sock, cnt;
   unsigned int addrlen;
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
   addr.sin_addr.s_addr = inet_addr(EXAMPLE_GROUP);
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
   return 0;
}

int checksum(char str[], int lenth){
   int i,sum=0,x;
   for(i=0;i<lenth;i++){
      x = atoi(str);
      sum+=floor(log2(x)/log2(2))+1;
   }
   return sum;
}

