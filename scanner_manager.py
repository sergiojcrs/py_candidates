import sys
import usb.core
import usb.util
import time
from element_converter import hid2ascii

class MyUsbScanner:
    
    def __init__ (self,idVendor,idProduct):
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.dev = usb.core.find(idVendor=0x9901, idProduct=0x0301)
        self.interface = 0
        self.endpoint = self.dev[0][(0,0)][0]

    
    def claim_device(self):
        if self.dev.is_kernel_driver_active(self.interface) is True:
            # tell the kernel to detach
            self.dev.detach_kernel_driver(self.interface)
            # claim the device
            usb.util.claim_interface(self.dev, self.interface)
    
    def release_device(self):
        try:
            # release the device
            usb.util.release_interface(self.dev, self.interface)
            # reattach the device to the OS kernel
            self.dev.attach_kernel_driver(self.interface)
        except Exception as e: 
            print(e)
    
    
    def read_element(self):
        ch = ''
        try:
            data = self.dev.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
            if data[2]:
                ch = hid2ascii(data)
            return ch
        except usb.core.USBError as e:
            if e.args[1] == ('Overflow'):
                self.dev.reset()
            return ''
    
    
    def read_buffer(self):
        full_scan = ''
        qr_scan = ''
        while True:
            try: 
                qr_scan = self.read_element()
                if qr_scan != '':
                    full_scan += qr_scan
                if qr_scan == '\n':
                    break
            except usb.core.USBError as e:
                if e.args[1] == ('Operation timed out'):
                    break
        return full_scan
    

