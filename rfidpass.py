import socket
import select 
import sys
import time 
from threading import Thread
from SocketServer import ThreadingMixIn

global dataqueue
dataqueue=[]
rfiddata="abc123"
#def passdata(rfiddata):
    #the rfid tag contents are passed to the fucntion from read.py in form a string. Function passes it to the client program which then forwards it to the centralized server 
dataqueue.append(rfiddata) #at any instance dataqueue contains list of rfid readings that are yet to be sent to the client.py. If client.py has to restart then readings that failed are successfully stored in the queue  
#server_address = ('localhost', 20000)
host = ''
port=20001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket for getting rfid data from rfidpass.py
server.bind((host,port))
server.setblocking(0)
server.listen(5) 
input = [server, sys.stdin] 
while True:
    inputready,output,exceptions = select.select(input,[],[]) 
    for s in inputready: 
        #print i
        if s == server: 
            # handle the server socket 
            client, address = server.accept() 
            print "client", address
            input.append(client)
            
        elif s == sys.stdin: 
            # handle standard input 
            junk = sys.stdin.readline() 
            running = 0 
            s.close() 
            input.remove(s)
        else:
            hellodata = s.recv(1024)
            print hellodata
            for i in dataqueue:
                sentflag=0 
                sendcount=0
                while sendcount < 3:
                    try:
                        #time.sleep(5.0)
                        print "sending data"
                        data = s.send(i)
                    except socket.error, exc:
                        print "Caught exception socket.error : %s" % exc
                        #print "error"
                        sendcount+=1
                        continue 
                    sentflag = 1
                    break 
        
            if sentflag==1: #if data has been sent remove it from the queue 
                print "Data sent"
                dataqueue.remove(i)
    
    for s in exceptions:
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        s.close()
        
#passdata("abc123")    