

import select 
import socket 
import sys 
import thread
import time 
from threading import Thread
from SocketServer import ThreadingMixIn

global socktable
socktable={} #contains socket objects of active sockets
global clienttimers
clienttimers = {}  #contains order of execution for each client 
global exectime  #amount of time for which a client should be online 
exectime = 0 
global prevexectime
global clientid # ip address + port number 
global resendtable 
resendtable = {} #contains number of retrasnmissions occured for each client 
def calculatetimers():
    sleeptime = 5.0 
    startime = time.time()
    changetime = time.time() + 60
    global exectime
    global prevexxectime
    global resendtable 
    prevexectime = 0 
   
    print "Thread for fucntion started"
    while True:
        changeflag = 0 
        if changetime < time.time(): #For the first minute the timer value is frequently updated as we could expect many devices
            sleeptime = 15.0 #after a minute timer messages are exchanged every 15 seconds
        ind = 0
        n = len(clienttimers.keys())
        if n==0:
            continue 
        exectime = 1000/n # a device should not wait more than a sec for TDMA
        #assigning order of execution
        if prevexectime != exectime:
            resettime = time.time() + 7 #Time when all the devices have to start their new timers
            changeflag = 1
        for i in clienttimers.keys():
            clienttimers[i]=ind
            ind += 1
            sockt = socktable[i]
            timerinfo = "timer" + "-" + str(exectime) + "-" + str(clienttimers[i]) + "-" + str(resettime) + "-" + str(changeflag)
            print "sending timerinfo to", i
            while True:
                try:
                    sockt.send(timerinfo)
                except:
                    resendtable[i]+=1
                    if resendtable[i] >= 3:
                        clienttimers.pop(i, None) #more than three failed attempts indicates device is offline 
                        resendtable.pop(i,None)
                        break
                    time.sleep(1.0) #resend after one second
                    continue
                break
        time.sleep(sleeptime)
        prevexectime = exectime 

      
host = '' 
port = 10008
backlog = 5 
size = 1024 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
server.setblocking(0)
input = [server, sys.stdin] 
flag = 1 

i=1
try:
    thread.start_new_thread(calculatetimers, ())
except:
    print "Error: unable to start thread"

endtime = time.time() + 10
while flag:
    inputready,output,exceptions = select.select(input,[],[]) 
    
    for s in inputready: 
        #print i
        if s == server: 
            # handle the server socket 
            client, address = server.accept() 
            input.append(client)
            
        elif s == sys.stdin: 
            # handle standard input 
            junk = sys.stdin.readline() 
            running = 0 
            s.close() 
            input.remove(s)
            

        else: 
            # handle all other sockets 
            while True:
                try:
                    data = s.recv(size) #data can be initial hello message, or rfid data 
                    reply = ""
                    if data: 
                        if data == "hello":
                            clientid = str(address[0]) + "-" + str(address[1])
                            clienttimers[clientid] = 0
                            resendtable[clientid] = 0
                            socktable[clientid]=s
                            print clientid
                            reply = "ack"
                            s.send(reply)
                        elif data == "timer":
                            timerinfo = "timer-" + str(exectime) + "-" + str(clienttimers[clientid])
                            s.send(timerinfo) 
                        elif "rfid" in data:
                            print data 
                except:
                         resendtable[clientid]+=1
                         if resendtable[clientid] >= 3:
                             clienttimers.pop(clientid, None)
                             resendtable.pop(i,None)
                             break 
                         continue 
                break 
                                 
    
    for s in exceptions:
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in output:
            outputs.remove(s)
            #s.close()
           

        
  

           # Remove message queue
           #del message_queues[s]
server.close()