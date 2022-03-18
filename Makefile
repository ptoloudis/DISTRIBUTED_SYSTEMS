CC = gcc
CCFLAGS = -Wall -g 
OBJ = myServer.o library.o

myServer: $(OBJ)
	$(CC) $(OBJ) -o myServer -lpthread -lm

myServer.o: myServer.c header.h
	$(CC) $(CCFLAGS) -c $<

library.o: library.c header.h
	$(CC) $(CCFLAGS) -c $<

.PHONY: clean
clean:
	rm -f*.o 