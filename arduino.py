import serial                                                              
import time                                                                  
ser = serial.Serial('/dev/ttyACM0',baudrate = 2400, timeout = 3)                                                                   
print(ser.readline())                             
print ("You have new message from Arduino")
while 1:         
    var = int(input())                                                       
    if (var == 1):                                                       
        ser.write("1".encode())                            
        print ("LED turned ON")         
        time.sleep(1)          
    if (var == 0):
        ser.write("0".encode())              
        print ("LED turned OFF")         
        time.sleep(1)
    if (var == 'fine and you'): 
        ser.write("0".encode())    
        print ("I'm fine too,Are you Ready to !!!")         
        print ("Type 1 to turn ON LED and 0 to turn OFF LED")         
        time.sleep(1)
