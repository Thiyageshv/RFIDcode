import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table

conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='',
        aws_secret_access_key='')
        
def createitem(tagid):
    tagid = str(tagid)
    if tagid == "165":
        product = "Toothpaste"
        price = "3$"
    if tagid == "214":
        product = "Brush"
        price = "33$"
    if tagid == "100":
        product = "Diet Coke"
        price = "2$"
    users = Table('items')
    # WARNING - This doens't save it yet!
    brush = Item(users, data={
     'rfid': tagid,
     'pname': product,
     'Price': price,
     'tray_status': '0',
     })

     # The data now gets persisted to the server.
    brush.save()
     
def updateitem(tagid,status):
    print "updating tray status"
    tagid = str(tagid)
    users = Table('items')
    if tagid == "214":
        product = "Brush"
        price = "33$"
    if tagid == "165":
        product = "Toothpaste"
        price = "3$"
    if tagid == "100":
        product = "Diet Coke"
        price = "2$"
    curitem = users.get_item(rfid=tagid, pname=product)
    curitem['tray_status'] = status
    #johndoe['whatever'] = "man, that's just like your opinion"
    #del curitem['tray_Status']

    # Affects all fields, even the ones not changed locally.
    curitem.save()

def displayitem():
    users = Table('items')
    curitem = users.get_item(rfid='214', pname='Brush')
    return curitem['pname']

def present(tagid):
    users = Table('items')
    result = users.scan(
    tray_status__eq='1' )
    k=1
    total = 0 
    for user in result:
        if user['rfid']==tagid:
            return 1
    return 0 
    

def query():
    context = {}
    textlist = []
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
    context['text'] = textlist
    print context['text']
    return context 	    

#updateitem()
#createitem()
#query()    
