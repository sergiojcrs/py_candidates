import usb.core
import usb.util
import threading
import time
from element_converter import hid2ascii

# Find USB device (replace with your device's vendor and product ID)

VID = 0x9901  # Vendor ID
PID = 0x0301  # Product ID
device = usb.core.find(idVendor=VID, idProduct=PID)

if device is None:
    raise ValueError("Device not found")

# Set configuration if necessary
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)
device.set_configuration()

# Function to read data from the USB device
def read_usb_data(endpoint, timeout=1000):
    try:
        return device.read(endpoint, 64, timeout)
    except usb.core.USBError as e:
        if e.args == ('Operation timed out'):
            return None  # Timeout, no data
        #raise

# Function that continuously polls the device for data
def poll_device(endpoint):
    ch = ''
    while True:
        data = read_usb_data(endpoint)
        if data:
            print(f"Data received: {data}")
            if data[2]:
                ch = hid2ascii(data)
        time.sleep(0.1)  # Polling interval, adjust as needed

# Get the first endpoint (replace with your device's endpoint)
endpoint = device[0][(0,0)][0].bEndpointAddress

# Start polling the device in a separate thread
polling_thread = threading.Thread(target=poll_device, args=(endpoint,))
polling_thread.daemon = True
polling_thread.start()

# Main program loop
try:
    while True:
        time.sleep(1)  # Simulate doing other tasks
except KeyboardInterrupt:
    print("Exiting...")
