import socket

s=socket.socket()
server_adr = ('',12345)
s.bind(server_adr)
s.listen(5)
print("Listening..")
while True:
	c, addr = s.accept()
	print("Connection from {}".format(addr))	
	data = (c.recv(64)).decode()
	print("{} -> Message = {}".format(addr,data))
	c.sendall(("Message Recieved! Message = {}".format(data)).encode())

