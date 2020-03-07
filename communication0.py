import socket
import time
import os
import serial


class Tcp():
	def __init__(self):
		self.host = "127.0.0.1"
		self.port = 5567
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
			# print("len",data)
			print("-------")
			return data  # .decode('utf-8')

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

	data1 = data1 * 256 + data2

	print(flag, function, data1)
