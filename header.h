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
#include <fcntl.h>


/********************** DEFINITIONS **********************/

#define SERVER_IP "192.168.68.190" 
#define SERVER_PORT 12000
#define CLIENT_PORT 12001
#define BUF_LEN 1024

/********************** STRUCTURES **********************/

typedef struct client_info
{
    char buffer[BUF_LEN];
    struct sockaddr *client_addr;
    socklen_t client_addr_len;
}Info_t;

typedef struct open_info
{
    char *filename;
    int flags;
    int id;
    int fd;
    double size;
    int timestamp;  
}File_t;

/********************** GLOBALS **********************/
File_t *file_buf;


/********************** FUNCTIONS **********************/
int mynfs_init();
int mynfs_open(char *filename, int flags);
int mynfs_read(int fd, void *buf, size_t n, int offset);
int mynfs_write(int fd, void *buf, size_t n, int offset);
int mynfs_seek(int fd, off_t pos, int whence);
int mynfs_ftruncate(int fd, off_t len);
int mynfs_close(int fd);


/********************** WRAPER FUNCTIONS **********************/
int nfs_init();
char *nfs_open(char *filename, int flags);
char *nfs_read(int fd, void *buf, size_t n, int offset);
char *nfs_write(int fd, void *buf, size_t n, int offset);
char *nfs_seek(int fd, off_t pos, int whence);
char *nfs_ftruncate(int fd, off_t len);
char *nfs_close(int fd);