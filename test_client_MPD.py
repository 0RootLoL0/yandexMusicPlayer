import socket, json, sys, os
SERVER = "127.0.0.1"
PORT = 5598
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	client.connect((SERVER, PORT))
	if sys.argv[1] == "pause":
		client.sendall(bytes("pause",'UTF-8'))
	elif sys.argv[1] == "play":
		client.sendall(bytes("play",'UTF-8'))
	elif sys.argv[1] == "back":
		client.sendall(bytes("back",'UTF-8'))
	elif sys.argv[1] == "onward":
		client.sendall(bytes("onward",'UTF-8'))
	elif sys.argv[1] == "returnName":
		client.sendall(bytes("returnName",'UTF-8'))
	else:
		client.sendall(bytes("error",'UTF-8'))
	data = client.recv(1024)

	if sys.argv[1] == "returnName":
		ww = json.loads(data.decode())
		os.system("i3-nagbar -m 'Трек: " +ww["title"]+ " Артист: " +ww["artists"][0]["name"]+ "' -t warning")
	else:
		print(data.decode())
	client.close()
except ConnectionRefusedError:
	print("Connect error")