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
#include <sys/stat.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "header.h"
#include <fcntl.h>

File_t *file_buf;
Id_t *id_buf;

int count_fd = 0;

int mynfs_init()
{
    file_buf = (File_t *) calloc(BUF_LEN/2, sizeof(File_t));
    if(file_buf == NULL)
    {
        perror("ERROR in Calloc");
        exit(1);
    }
    id_buf = (Id_t *) calloc(BUF_LEN * 2, sizeof(Id_t));
    if(id_buf == NULL)
    {
        perror("ERROR in Calloc");
        exit(1);
    }
    return 0;
}


int mynfs_open(char *filename, int flags)
{
    int fd;
    File_t *file;
    struct stat stat_buf;
    char *fi;

    printf("Opening file %s\n", filename);   

    for(int i = 0; i < BUF_LEN/2; i++)
    {
        
        if(file_buf[i].fd == 0)
        {
            fd = open(filename, flags);
            printf("fd = %d\n", fd);
            if(fd <= 0)
            {
                return -1;
            }
            file = &file_buf[i];
            strcat(file->filename, filename);
            file->flags = flags;
            file->id = i;
            file->fd = fd;
            file->timestamp = 0;
            fstat(fd, &stat_buf);
            file->size = stat_buf.st_size;
            id_buf[count_fd].id = i;
            id_buf[count_fd].open_id = count_fd;
            return count_fd++;
        }
        fi = file_buf[i].filename;
        if(strcmp(fi, filename) == 0)
        {
            printf("File already open\n");
            file = &file_buf[i];
            id_buf[count_fd].id = i;
            id_buf[count_fd].open_id = count_fd;
            return count_fd++;
        }
    }
    perror("ERROR in Open : Buffer is full");
    return -1;
}

int mynfs_read(int fd, void *buf, size_t n, int offset)
{
    lseek(fd,(off_t) offset, SEEK_SET);
    return read(fd, buf, n);
}

int mynfs_write(int fd, void *buf, size_t n, int offset)
{
    File_t *file = &file_buf[fd];

    lseek(fd,(off_t) offset, SEEK_SET);
    file->timestamp ++;
    return write(fd, buf, n);
}

int mynfs_ftruncate(int fd, off_t size)
{
    File_t *file = &file_buf[fd];

    file->timestamp ++;
    return ftruncate(fd, size);
}

int mynfs_close(int fd)
{
    return close(fd);
}


char *nfs_open(char *filename, int flags)
{
    int fd, tmp;
    char *message;
    

    fd = mynfs_open(filename, flags);
    if(fd < 0)
    {
        return "File Not Created";
    }
    tmp = id_buf[fd].id;
    sprintf(message, "%d#%d#%d", fd, file_buf[tmp].timestamp, (int)file_buf[tmp].size);
    
    return message;
}

char *nfs_read(int fd, void *buf, size_t n, int offset)
{
    char buffer[1024];
    char message[4098];
    int tmp;
    fd = id_buf[fd].id;
    fd = file_buf[fd].fd;
    printf("fd = %d\n", fd);
    tmp = mynfs_read(fd, buffer, sizeof(buffer), offset);
    if (tmp < 0)
    {
        return "File Not Read";
    }
    sprintf(message, "%d#%d#%s", fd, file_buf[fd].timestamp, buffer);
    buf = message;
    return buf;
}

char *nfs_write(int fd, void *buf, size_t n, int offset)
{
    char *message;
    fd = id_buf[fd].id;
    fd = file_buf[fd].fd;
    mynfs_write(fd, buf, n, offset);
    sprintf(message, "%s","OK");
    return message;
}

char *nfs_ftruncate(int fd, off_t size)
{
    fd = id_buf[fd].id;
    char *message;
    mynfs_ftruncate(fd, size);
    sprintf(message, "%s", "OK");
    return message;
}

char *nfs_mod(int fd, int last)
{
    char *message;
    fd = id_buf[fd].id;
    if (last == file_buf[fd].timestamp)
    {
        sprintf(message, "%s", "OK");
    }
    else
    {
        sprintf(message, "%s", "MOD");
    }
    return message;
}


char *nfs_close(int fd){
    return mynfs_close(fd);
}
