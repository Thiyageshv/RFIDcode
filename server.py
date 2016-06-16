

import select 
import socket 
import sys 
import thread
import time 
from createtable import createitem,updateitem,displayitem,present,query 
from threading import Thread
from SocketServer import ThreadingMixIn

global socktable
socktable={} #contains socket objects of active sockets
global clienttimers
clienttimers = {}  #contains order of execution for each client 
global clienttimerslower
clienttimerslower = {}  #contains order of execution for each client in lowerring
global exectime  #amount of time for which a client should be online 
exectime = 0 
global prevexectime
global exectime2  #amount of time for which a client for lower ring should be online 
exectime2 = 0 
global prevexectime2
global clientid # ip address + port number 
global resendtable 
resendtable = {} #contains number of retrasnmissions occured for each client 
global inputq
inputq = {}
global outputq
outputq = {}
global tagstatus
tagstatus = {} # 1 or 0 corresponding to inside the tray or outside the tray 
global readyflag 
readyflag = 0
global readflaglower 
readyflaglower = 0
def calculatetimers():
    sleeptime = 5.0 
    startime = time.time()
    changetime = time.time() + 60
    global exectime
    global prevexxectime
    global resendtable 
    global readyflag
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
           
            while True:
                if readyflag == 0:
                    continue 
                try:
                    print "sending timerinfo to", i
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
        
def calculatetimerslower():
    sleeptime2 = 5.0 
    startime2 = time.time()
    changetime2 = time.time() + 60
    global exectime2
    global prevexxectime2
    global resendtable 
    global readyflaglower
    prevexectime2 = 0 
   
    print "Thread for fucntion started"
    while True:
        changeflag = 0 
        if changetime2 < time.time(): #For the first minute the timer value is frequently updated as we could expect many devices
            sleeptime2 = 15.0 #after a minute timer messages are exchanged every 15 seconds
        ind = 0
        n = len(clienttimerslower.keys())
        if n==0:
            continue 
        exectime2 = 1000/n # a device should not wait more than a sec for TDMA
        #assigning order of execution
        if prevexectime2 != exectime2:
            resettime = time.time() + 7 #Time when all the devices have to start their new timers
            changeflag = 1
        for i in clienttimerslower.keys():
            clienttimerslower[i]=ind
            ind += 1
            sockt = socktable[i]
            timerinfo = "timer" + "-" + str(exectime2) + "-" + str(clienttimerslower[i]) + "-" + str(resettime) + "-" + str(changeflag)
            print "sending timerinfo to", i
            while True:
                if readyflaglower==0:
                    continue 
                try:
                    sockt.send(timerinfo)
                except:
                    resendtable[i]+=1
                    if resendtable[i] >= 3:
                        clienttimerslower.pop(i, None) #more than three failed attempts indicates device is offline 
                        resendtable.pop(i,None)
                        break
                    time.sleep(1.0) #resend after one second
                    continue
                break
        time.sleep(sleeptime2)
        prevexectime2 = exectime2 

      
host = '' 
port = 10003
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
try:
    thread.start_new_thread(calculatetimerslower, ())
except:
    print "Error: unable to start thread"

endtime = time.time() + 10
while flag:
    #readyflag = 0
    #readyflaglower = 0
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
            # handle all other sockets 
            while True:
                try:
                    data = s.recv(size) #data can be initial hello message, or rfid data 
                    clientid = str(address[0]) + "-" + str(address[1])
                    reply = ""
                    if data: 
                        if data == "hello":
                            #clientid = str(address[0]) + "-" + str(address[1])
                            clienttimers[clientid] = 0
                            resendtable[clientid] = 0
                            socktable[clientid]=s
                            print "Upper Ring RFID", clientid
                            reply = "ack"
                            print "Sending ack"
                            readyflag = 1
                            s.send(reply)
                        elif data == "lower":
                             #clientid = str(address[0]) + "-" + str(address[1])
                             clienttimerslower[clientid] = 0
                             resendtable[clientid] = 0
                             socktable[clientid]=s
                             print "lower ring RFID", clientid
                             reply = "ack"
                             readyflaglower = 1 
                             s.send(reply)
                            
                        elif data == "timer":
                            timerinfo = "timer-" + str(exectime) + "-" + str(clienttimers[clientid])
                            s.send(timerinfo) 
                        elif "rfid" in data:
                            if clientid in clienttimers.keys():
                                print clientid, data
                            if clientid in clienttimerslower.keys():
                                print clientid,data
                            #handle collisions from RIFD's of same ring, find if tag is inside the basket and update cloud 
                            # if tagid is in inputq, it is inside the tray. If tagid is in output ONLY, it has left the tray 
                            content = data.split("-")
                            tagid = content[1]
                            #clientid = str(address[0]) + "-" + str(address[1])
                            if "upper" in data and (inputq.keys() is None or tagid not in inputq.keys()) and (outputq.keys() is None or tagid not in outputq.keys()):
                                print "tag has entered the tray"
                                tagstatus[tagid] = 0 #tag has just passed the upper ring, not sure if it is inside the tray yet
                                inputq[tagid] = 0
                                outputq[tagid] = 0 
                                #insert into table or do nothing if already present 
                                if not present(tagid):
                                    createitem(tagid)
                                    
                            
                            elif "upper" in data and (tagid in inputq.keys() and tagid in outputq.keys()):
                                print "tag has left the tray"
                                tagstatus[tagid]=0 #tag is outside the tray 
                                inputq.pop(tagid, None)
                                #update status to 0
                                updateitem(tagid, '0')
                            
                            elif "lower" in data and tagid in inputq.keys() and tagid in outputq.keys():
                                print "tag is now inside the tray"
                                tagstatus[tagid] = 1 # tag is inside the tray as it has passed the lower ring too
                                outputq.pop(tagid, None)
                                #update status to 1
                                updateitem(tagid, '1')
                            
                            elif "lower" in data and tagid in inputq.keys() and tagid not in outputq.keys():
                                print "tag is still inside the tray but might be in the process of leaving"
                                tagstatus[tagid] = 1 # tag that was inside the tray is now taken out 
                                outputq[tagid] = 0
                                #do nothing
                                
                            #update cloud now based on tagstatus 
                             
                except:
                         if clientid not in resendtable:
                             break 
                         resendtable[clientid]+=1
                         if resendtable[clientid] >= 10:
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