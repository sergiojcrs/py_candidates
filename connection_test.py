import socketio
import os
import time
import webbrowser

import socketio.exceptions
import scanner_manager
import datetime
import atexit

idVendor=0x9901
idProduct=0x0301
my_scanner = scanner_manager.MyUsbScanner(idVendor,idProduct)
my_scanner.claim_device()
qr_scan = ''

def ExitingProgram():
    my_scanner.release_device()
   

sio = socketio.Client()


@sio.event
def connect():
    print("I'm connected!")
 

@sio.event
def connect_error(data):
    print("The connection failed!")

 
@sio.event
def disconnect():
    print("I'm disconnected!")

 
@sio.event
def message(data):
    print('I received a message!')

@sio.on('server')
def on_message(data):
    print('Server Data ', data)    

try:
    #sio.connect('wss://api-staging.calimaco.com', socketio_path='/api/retail_notifications', transports=['websocket'])
    sio.connect('HTTP://192.168.1.60:18104', transports=['websocket'])
    #print('my transport is', sio.transport)
    sio.emit('server', {"type":"terminal-login", "company":"CAL", "terminal":"1", "hash":"12121212121"})
except socketio.exceptions.ConnectionError:
    print("Unable to connect")

try:
    os.system('export DISPLAY=:0 && xdg-open && /usr/bin/google-chrome-stable --start-fullscreen https://staging-retail.calimaco.com/')
    with open("timestamp.log", "a") as fh:
        fh.write(str(datetime.datetime.now()) + " => " + "Launching Chrome Display=:0 \n") 
    """
    URL = "https://www.python.org"
    webbrowser.open(URL)
    """
except Exception as e:
    print("Orror opening browser" + str(e))

atexit.register(ExitingProgram)  
try: 
    while True:
    
        qr_scan= my_scanner.read_buffer()
        if qr_scan!= '':
            print(qr_scan)
            qr_scan = qr_scan.strip()
            msg2 = {"type":"credit", "company":"CAL", "terminal":"1", "token":f"{qr_scan}"}
            with open("timestamp.log", "a") as fh:
                fh.write(str(datetime.datetime.now()) + " => " + msg2["token"] + "\n")      
            try:
                sio.emit('server',msg2)
            except Exception as e:
                print(e)
finally:
    print("Scaner Free\n")
    my_scanner.release_device()
