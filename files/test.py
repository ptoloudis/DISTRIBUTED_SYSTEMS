import serial                                                             
import time                                                           #Required to use delay functions   
Arduino =serial.Serial('COM4', 9600)  
print (Arduino.readline() )      
while 1:         #Do this forever
    x = input("Enter a number: ")
    Arduino.write(x.encode())
    if x == "2":
        print("hi")
        #print (Arduino.readline() )                            #read the serial data and print it as line 
        print (Arduino.readline() )
    else:
        print ("Wait")    
    time.sleep(1) #delay for 0.5 seconds