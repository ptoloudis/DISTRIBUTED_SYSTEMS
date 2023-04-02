CC = gcc
CCFLAGS = -Wall -g 
OBJ = server.o library.o

server: $(OBJ)
	$(CC) $(OBJ) -o server -lpthread 

server.o: server.c header.h
	$(CC) $(CCFLAGS) -c $<

library.o: library.c header.h
	$(CC) $(CCFLAGS) -c $<

.PHONY: clean
clean:
	rm -f*.o 