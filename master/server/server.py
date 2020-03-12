"""
TCP - IP Communication of vehicle
"""
import os
import socket
import time
from threading import Timer
import queue

def merge(flag,number,incoming_data):
    data = bytearray()
    data.append(flag)
    data.append(number)
    data1 = incoming_data // 256
    data2 = incoming_data % 256
    data.append(data1)
    data.append(data2)
    return data

def packing_joy(button):
    if button == -1:
        return merge(0,0,0)
    elif button == 2:
        return merge(255, 5, 10)
    elif button == 3:
        return merge(255, 5, 20)
    elif button == 5:
        return merge(255, 5, 30)
    elif button == 4:
        return merge(255, 5, 40)

def packing(key):
    # MICRO ROV FUNCTION
    if key == ord("W"):
        return merge(255, 1, 10)
    elif key == ord("S"):
        return merge(255, 1, 20)
    elif key == ord("A"):
        return merge(255, 1, 30)
    elif key == ord("D"):
        return merge(255, 1, 40)
    elif key == ord("Q"):
        return merge(255, 2, 50)
    elif key == ord("E"):
        return merge(255, 2, 60)

    # MASTER ROV FUNCTION
    elif key == ord("J"):  # KABLO SAR
        return merge(255,4, 10)
    elif key == ord("K"):  # KABLO SAL
        return merge(255,4, 20)

class Server():
    def __init__(self, port=5567):
        self.host = "192.168.2.1"
        self.port = port
        self.buffer_size = 1024
        self.axis_list = []
        self.i = 0
        self.new_conn = False
        self.connection = False
    def setupConnection(self):
        while True:
            try:
                self.connection = False
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind((self.host, self.port))
                self.s.listen()
                self.conn, self.address = self.s.accept()
                self.new_conn = True
                self.connection = True
                print("connection completed")
                return
            except Exception as msg:
                # print(msg)
                time.sleep(0.5)

    def datasend(self, button_list):
        try:
            self.conn.send(button_list)
        except BrokenPipeError as msg:
            print("broken pipe error ")
            self.setupConnection()


if __name__ == "__main__":
    s = Server()
    s.setupConnection()
    while True:
        s.datasend(["0"])
        time.sleep(0.5)