import scanner_manager
import datetime
import time
import sys

idVendor=0x9901
idProduct=0x0301
my_scanner = scanner_manager.MyUsbScanner(idVendor,idProduct)
my_scanner.claim_device()
qr_scan = ''

while True:
    try:
        qr_scan= my_scanner.read_buffer()
        if qr_scan!= '':
                print(qr_scan)
                qr_scan = qr_scan.strip()
                msg2 = {"type":"credit", "company":"CAL", "terminal":"1", "voucher":f"{qr_scan}"}
                with open("timestamp.log", "a") as fh:
                    fh.write(str(datetime.datetime.now()) + " => " + msg2["voucher"] + "\n")
    except Exception as e:
         print(e)
         my_scanner.release_device()
         break


            
