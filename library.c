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

int mynfs_init()
{
    file_buf = (File_t *) calloc(BUF_LEN, sizeof(File_t));
    if(file_buf == NULL)
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
    
    fd = open(filename, flags);
    if(fd == 0)
    {
        return -1;
    }

    for(int i = 0; i < BUF_LEN; i++)
    {
        
        if(file_buf[i].fd == 0)
        {
            file = &file_buf[i];
            file->filename = filename;
            file->flags = flags;
            file->id = i;
            file->fd = fd;
            file->timestamp = time(NULL);
            fstat(fd, &stat_buf);
            file->size = stat_buf.st_size;
            return file->id;
        }
        else 
        {
            file = &file_buf[i];
            if(file->filename == filename && file->flags == flags)
            {
                return file->id;
            }
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
    int fd;
    char *message;
    //int last_modified, size;

    fd = mynfs_open(filename, flags);
    if(fd < 0)
    {
        return "File Not Created";
    }
    sprintf(message, "%d#%d#%f.", fd, file_buf[fd].timestamp, file_buf[fd].size);
    
    return message;
}

char *nfs_read(int fd, void *buf, size_t n, int offset)
{
    return mynfs_read(fd, buf, n, offset);
}

char *nfs_write(int fd, void *buf, size_t n, int offset)
{
    return mynfs_write(fd, buf, n, offset);
}

char *nfs_ftruncate(int fd, off_t size)
{
    return mynfs_ftruncate(fd, size);
}

char *nfs_close(int fd){
    return mynfs_close(fd);
}