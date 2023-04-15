import socket
import pickle
import threading

class Server:
	def __init__(self, address = str("192.168.1.3"), port = int(5555)):
		self.address = address
		self.port = port
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((f"{self.address}", self.port))
		self.client_sockets = []

	def run(self):
		self.server_socket.listen()
		print(f"Servidor iniciado en {self.address}:{self.port}")

		while True:
			client_socket, address = self.server_socket.accept()
			print(f'se ha conectado : {address}')
			self.client_sockets.append(client_socket)
			threading.Thread(target=self.handle_client, args=(client_socket,)).start()

	def handle_client(self, client_socket):
		while True:
			data = client_socket.recv(4096)
			if not data:
				break
			player_position =pickle.loads(data)
			# print(player_position)
			pos = pickle.dumps((player_position))

			for sock in self.client_sockets:
				if sock != client_socket: 
					sock.send(pos)