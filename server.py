import socket
import pickle
import threading


class Server:
    def __init__(self, address=str("192.168.1.3"), port=int(5555)):
        self.address = address
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((f"{self.address}", self.port))
        self.client_sockets = []

    def run(self):
        self.running = True
        self.server_socket.listen()
        print(f"Servidor iniciado en {self.address}:{self.port}")

        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f'se ha conectado : {address}')
                self.client_sockets.append(client_socket)
                threading.Thread(target=self.handle_client,
                                 args=(client_socket,)).start()
            except OSError as e:
                print(f"ShutDown Server")
                break

    def handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    client = client_socket.getpeername()
                    print(f"Se ha desconectado : {client}")
                    client_socket.close()
                    self.client_sockets.remove(client_socket)
                    break

                for sock in self.client_sockets:
                    if sock != client_socket:
                        sock.send(data)
            except ConnectionAbortedError:
                break

    def stop(self):
        self.running = False
        for client_socket in self.client_sockets:
            # print(client_socket)
            client_socket.close()
        self.server_socket.close()
