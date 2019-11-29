import socket

class Server:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 30000))
        self.s.listen(1)

        connections = []

        while True:
            self.connection, address = self.s.accept()
            connections.append(self.connection)
            print(address)
            while True:
                data = self.connection.recv(1024)
                print(data)
                if data.decode(encoding='utf-8') == 'generate-key':
                    self.generateKey()

    def diffieHellman(self):
        self.connection.send('Okay, inform your name'.encode())
        data = self.connection.recv(1024)
        if self.checkUser(data.decode(encoding='utf-8')):
            print('abcdef')
            self.connection.send('abcdef'.encode())
        else:
            self.connection.send('This name already exists'.encode())
            return
        data = self.connection.recv(1024)
        print(data)
        if data.decode(encoding='utf-8') == 'private-key':
            print('123456')
            self.connection.send('123456'.encode())
        exit()

    def checkUser(self, name):
        file = open('server_key.txt', 'r')

        for i in file:
            name_entry = i.split(' ')
            if name == name_entry[0]:
                return False
        else:
            return True
