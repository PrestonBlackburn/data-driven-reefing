
import network
import socket
import time
import utime

from machine import Pin



### Utility Functions:

def test():
    print("pico test")
    led = Pin("LED", Pin.OUT)

    # For demo purposes, we have an infinite loop here
    count=0
    while count < 3:
        led.high()
        time.sleep(0.5)
        led.low()
        time.sleep(0.5)
        count += 1



# ------------------ Pump Control ------------------

# Pins used to control pump:
# L298n - Pi Pico
# IN1   - GP12 (pin 16)
# IN2   - GP13 (pin 17)
# GND   - GND  (pin 18)

# based on multimeter testing the pin int correspnds to the GP number
IN1 = Pin(12, Pin.OUT)
IN2 = Pin(13, Pin.OUT)


def motor_forward():
    print("Motor Backward")

    IN1.value(1)
    IN2.value(0)


def motor_backwards():
    print("Motor Forward")

    IN1.value(1)
    IN2.value(0)


def motor_off():
    print("Motor off")

    IN1.value(0)
    IN2.value(0)




# ------------------  Networking -------------------

# Create its own network (access point inteface)
def create_access_point():
    """
        create the pico wifi access point    
    """

    ssid = 'pico_ap'
    password = 'password'

    ap = network.WLAN(network.AP_IF)
    ap.config(ssid=ssid, password=password, channel = 11)
    ap.active(True)

    # wait for wifi to go active:
    wait_counter = 0
    while ap.active() == False:
        print(f"waiting: {wait_counter}")
        time.sleep(0.5)
        pass

    print("wifi active")
    status = ap.ifconfig()
    pico_ip = status[0]
    print(status)

    return pico_ip



def open_socket():
    """ create the socket for testing  """

    #addr = (pico_ip, 80)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    print("addr:  ", addr)

    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print(f'listening on: {addr}')

    print("testing led: ")
    test()

    print("longer listen + opening:")


    # listen for connections:
    while True:
        try:     
            conn, socket_addr = s.accept()
            print(f"client connected from {socket_addr}")

            request = conn.recv(1024)
            print(f"client request {request}")

            if "off" in request:
                motor_off()

            if "forward" in request:
                motor_forward()

            if "backward" in request:
                motor_backwards()

            conn.send(request)
            
        except OSError as e:
            conn.close()
            print("connection closed")











test()
#connect_to_wifi()
pico_ip = create_access_point()
open_socket()
