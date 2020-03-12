import socket
import time
import os
import serial
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
PWM_FREQ = 100
a = 0

pwm = []
pwm_data = []

for i in range(0, 45):
    pwm.append(0)
    pwm_data.append(0)

for i in range(a, 45):
    if (i == 42):
        continue
    GPIO.setup(i, GPIO.OUT)
    pwm[i] = GPIO.PWM(i, PWM_FREQ)
    pwm[i].start(0)

for i in range(a, 45):
    if (i == 42):
        continue
    pwm[i].ChangeDutyCycle(50)


class Tcp():
    def __init__(self):
        self.host = "192.168.2.1"
        self.port = 5555
        self.buffer_size = 1024
        self.start = time.time()

    def ping(self):
        state = os.system('ping {} {} > /dev/null'.format("-c 1", self.host)) == 0
        print(state)
        return state

    def setupConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((self.host, self.port))
                print("client connected")
                break
            except :
                print("connection refused")
                time.sleep(0.5)
                pass

    def getData(self):
        try:
            data = self.s.recv(self.buffer_size)
            print("len",len(data))
            return data #.decode('utf-8')

        except Exception as msg:
            print("Get data exception ", msg)

    def sendData(self, incoming):
        try:
            self.s.send(incoming)
        except Exception as msg:
            print("Send data exception", msg)
            pass


tcp = Tcp()
while True:
    if tcp.ping():
        print("ping is completed")
        break
    else:
        print("Ethernet unplugged")

tcp.setupConnection()
now = time.time()

while True:
    # Data coming from groundstation
    data = tcp.getData()
    if not data:
        tcp.setupConnection()
        
    if len(data) % 4 == 0:
        pass
    else:
        continue
    flag = data[0]
    function = data[1]
    data1 = data[2]
    data2 = data[3]
    
    data1 = data1*256 + data2
    
    print (flag, function, data1, data2)
    if flag == 255:
        if function == 5:
            if data1 == 10:
                device_data = 70
                device_id = 5
            elif data1 == 20:
                device_data = 70
                device_id = 6
            elif data1 == 30:
                device_data = 70
                device_id = 7
            elif data1 == 40:
                device_data = 70
                device_id = 8
        elif function == 4:
            if data1 == 10:
                device_data = 70
                device_id = 9
                pwm[5].ChangeDutyCycle(70)
            elif data1 == 20:
                device_data = 70
                device_id = 10





    pwm_data[device_id] = device_data
    pwm[device_id].ChangeDutyCycle(pwm_data[device_id])

    time.sleep(5.0 / PWM_FREQ)
