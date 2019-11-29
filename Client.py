from DiffieHellman import DiffieHellman
import sys
import socket

class Client:

    def __init__(self):
        server = '127.0.0.1'
        port = 30000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
        try:
            self.s.connect((server, port))

        except ConnectionRefusedError:
            print('Connection refused')

    def sendMessage(self):
        result = []
        while True:
            print('Write your message: ', end='')
            msg = input()
            if len(msg) < 20:
                self.s.send(msg.encode())
                result.append(self.s.recv(1))
                while True:
                    try:
                        print(result)
                        result.append(self.s.recv(1))
                    except socket.timeout:
                        break

            else:
                print('Message too long, write a message smaller than 20 characters')

    def requestKey(self):
        msg = 'generate-key'
        self.s.send(msg.encode())
        try:
            if self.s.recv(25).decode('utf-8') == 'Okay, inform your name':
                print('Okay, inform your name')
                return
        except:
            print('Connection timeout')
            exit()

    def informName(self, name):
        self.s.send(name.encode())
        try:
            buffer = self.s.recv(25)
            if buffer.decode('utf-8') == 'This name already exists':
                print('This name already exists')
                exit()
            else:
                return buffer
        except:
            print('Connection timeout')
            exit()

    def generateKey(self, name):
        self.requestKey()
        publicKey = self.informName(name)

        file = open('client_key.txt', 'w')
        # publicKey = self.s.recv(64)
        print(publicKey)
        file.write('Public-key: ' + publicKey.decode('utf-8') + '\n')
        msg = 'private-key'
        self.s.send(msg.encode())
        privateKey = self.s.recv(64)
        print(privateKey)
        file.write('Private-key: ' + privateKey.decode('utf-8') + '\n')
        file.close()
        self.s.close()


if sys.argv[1] == '--generate-key' and len(sys.argv) == 2:
    client = Client()
    client.generateKey(sys.argv[2])
    print('Key generated successfully')
