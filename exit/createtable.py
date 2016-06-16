import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
import time 
global pretext 
pretext = []
global extitem
extitem = []
global firsttimeflag 
firsttimeflag = 0 
conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='AKIAIEMNGBBNHEB7XYDQ',
        aws_secret_access_key='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')
        
def createitem():

    
    users = Table('items')
    # WARNING - This doens't save it yet!
    brush = Item(users, data={
     'rfid': '165',
     'pname': 'Toothpaste',
     'Price': '3$',
     'tray_status': '1',
     })

     # The data now gets persisted to the server.
    brush.save()
     
def updateitem():
    users = Table('items')

    curitem = users.get_item(rfid='165', pname='Toothpaste')
    curitem['tray_status'] = '0'
    #johndoe['whatever'] = "man, that's just like your opinion"
    del curitem['tray_Status']

    # Affects all fields, even the ones not changed locally.
    curitem.save()

def displayitem():
    users = Table('items')
    curitem = users.get_item(rfid='214', pname='Brush')
    return curitem['pname']

	

def query():
    global pretext
    context = {}
    textlist = []
    global extitem
    clearflag = 0
    global firsttimeflag
    users = Table('items')
    result = users.scan(
    tray_status__eq='1' )
    k=1
    total = 0 
    for user in result:
	text = ""
	label = 'pname' + str(k)
    	context[label]=user['pname']
   	text = text + user['pname'] + " : " 
	labelp = 'price' + str(k)
	context[labelp]=user['Price']
	p = user['Price']
	val = p.split("$")
	total = total + int(val[0])
 	text = text + user['Price'] + "\n"
	textlist.append(text)
        k+=1
    totaltext = "Total : " + str(total)
    textlist.append(totaltext)
    if textlist == pretext:
    	pretext = []
    else:
    	for t in textlist:
		if t not in pretext and 'Total' not in t:
			if "Diet Coke" in t:
				extitem = []	
				extitem.append(t)
			''' if clearflag == 0:
				extitem = []
				clearflag = 1 
			extitem.append(t)
			if "Diet Coke" in t:
                        	firsttimeflag = 1
			if firsttimeflag ==0:
				extitem = [] '''
    
    print firsttimeflag
    context['text'] = textlist
    context['time'] = time.time()
    context['pretext'] = extitem   
    pretext = textlist 
    return context 	    



#updateitem()
#createitem()

#while True:
#	query()
#	time.sleep(3.0)    
