from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
from createtable import query
import datetime
import time
import thread
from threading import Thread
from SocketServer import ThreadingMixIn



global context
context = {}
#context = query()
#n = len(context)/2
def update():
	global context 
	#context['current_time'] = time.time()
 	#context['num']=n 
	context= query()
    	#print context 
	time.sleep(5)    

from django.shortcuts import render_to_response
def index(request):
	global context
	try:
        	thread.start_new_thread(update, ())
	except:
    		print "Error: unable to start thread"
	#context['time'] = time.time()
	template = loader.get_template('index.html')
    	data = RequestContext(request, context)
    	return HttpResponse(template.render(data))





'''    return render_to_response("exit/home.html",
                               {"Testing" : "Contents of the Tray: ",
                               "HelloHello" : output})
'''

