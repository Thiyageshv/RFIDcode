import socket
import sys
import time 
from threading import Thread
from SocketServer import ThreadingMixIn
global timer 
message = 'lower'
server_address = ('localhost', 10003)
rfid_address = ('localhost', 20000)
host =''
port=20000
threads = []

class timerthread(Thread):
    def __init__(self,socket):
        Thread.__init__(self)
        print "timer thread started"
        self.socket=socket
    def run(self):
        
        while True:
            #s.send(gettimer)
            try:
                data = self.socket.recv(1024)
                print data
                if "timer" in data:
                    timer=data.split("-")
                    changeflag = int(timer[4])
                    if changeflag==1:
                        resettime = float(timer[3])
                        offset = float(timer[1])*int(timer[2])
            except socket.timeout:
                print "timed out"
                continue 

        print "timer value is",timer


class datathread(Thread):
    def __init__(self,socket):
        Thread.__init__(self)
        print "data thread started"
        self.socket=socket 
    def run(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket for getting rfid data from rfidpass.py 
        try:
            s2.connect(rfid_address)
        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc
        s2.settimeout(30)
        while True:
            try:
                s2.send("hello")
            except:
                #print "error"
                continue 
            break 
        retrycount = 0    
        while retrycount <=3:
            try:
                rfiddata = s2.recv(1024)
            except:
                time.sleep(3.0)
                retrycount += 1 
                continue 
            print rfiddata
            rfiddata = "rfid lower" + "-" + rfiddata
            s.send(rfiddata) #rfiddata is now sent to centralized server
        s2.close()
        


        

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
# Connect the socket to the port where the server is listening
print >>sys.stderr, 'connecting to %s port %s' % server_address
s.connect(server_address)
s.settimeout(10)	

print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
while True:
    s.send(message)
    try:
        data = s.recv(1024)
    except socket.timeout:
        continue 
    break 
print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
'''if data != "ack":
    print >>sys.stderr, 'closing socket', s.getsockname()
    s.close() '''

print "get timer"
gettimer = "timer"

#data = s.recv024)

newthread = timerthread(s)
newthread.daemon = True
newthread2 = datathread(s)
newthread2.daemon = True

newthread.start()
newthread2.start()
threads.append(newthread)
threads.append(newthread2)

for t in threads:
    t.join(600)
    
#s2.close()
       