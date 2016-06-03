# RFIDcode

servery.py should be executed at the centralized server. 

client.py should be executed at all the client devices. 

server keeps track of the active clients and computes timer values. It then updates each of the devices on time when they have to make their rfid reader active. 
rfidpass.py contains a code snippet that must be intergrated with the read.py of MFRC522 library. rfidpass.py passes all the readings to client.py which then passes it to server.py

