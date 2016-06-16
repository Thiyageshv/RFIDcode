# RFIDcode

servery.py is the centralized server that habndles collisions and sycns with the cloud.

clients.py and clientslower.py act as intermediate stations that communicate with the RFID readers as well as the centralized server. 
rfidpass.py and rfidpass2.py are simulations to run for checking if you don't have any of the hardware required.

server keeps track of the active clients and computes timer values. It then updates each of the devices on time when they have to make their rfid reader active. 
rfidpass.py contains a code snippet that must be intergrated with the read.py of MFRC522 library. rfidpass.py passes all the readings to clients.py which then passes it to server.py

## How to run the simulation

Execute the codes in following order in separate terminal windows:
```
python server.py
python rfidpass.py, python rfidpass2.py
python manage.py runserver 0.0.0.0:8000
python clients.py
python clientslower.py 
```

Access the mobile webiste at http://ip address of server:8000/exit/ 
If you ahve the required hardware, follow the correct pin diagrams for the wifi shield and the RFC522 shield using information in  http://www.instructables.com/id/WiFi-RFID-Reader/ or https://www.addicore.com/v/vspfiles/downloadables/Product%20Downloadables/RFID_RC522/RFIDQuickStartGuide.pdf

For more information regarding the project setup follow 
1. https://www.youtube.com/watch?v=ADa_hrrYCs0 (Hardware explanation)
2. https://www.youtube.com/watch?v=6BJ7B6ySxgA (Software explanation)
3. https://www.youtube.com/watch?v=myyGI2jcHtA (Porject demonstation)


