from DiffieHellman import DiffieHellman
import sys
import socket

class Client:

    def __init__(self):
        server = '127.0.0.1'
        port = 3000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(30)
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

    def informName(self, name, diffieHellman):
        print('Name == ' + name)
        encName = diffieHellman.encrypt(name)
        print('Encrypted name == ' + encName)
        self.s.send(encName.encode())
        try:
            buffer = self.s.recv(64)

            decodedBuffer = buffer.decode(encoding='utf-8')
            print('Encrypted buffer == ' + decodedBuffer)
            decBuffer = diffieHellman.decrypt(decodedBuffer)
            print('Decrypted buffer == ' + decBuffer)
            if decBuffer == 'This name already exists':
                print('This name already exists')
                exit()
            else:
                return decBuffer
        except:
            print('Connection timeout')
            exit()

    def diffieHellman(self, name):
        self.s.send('generate-key'.encode())
        diffieHellman = DiffieHellman()

        buffer = self.s.recv(1024).decode('utf-8')
        buffer = buffer.split('_')

        diffieHellman.prime = int(buffer[0])
        diffieHellman.alpha = int(buffer[1])

        print('Prime == ' + str(diffieHellman.prime))
        print('Alpha == ' + str(diffieHellman.alpha))

        diffieHellman.generatePrivateKey(diffieHellman.prime)
        diffieHellman.generatePublicKey(diffieHellman.prime, diffieHellman.alpha)

        print('Private == ' + str(diffieHellman.privateKey))
        print('Public == ' + str(diffieHellman.publicKey))

        serverPublicKey = int(self.s.recv(1024).decode('utf-8'))

        print('Server key == ' + str(serverPublicKey))

        self.s.send(str(diffieHellman.publicKey).encode())

        diffieHellman.sharedKey(serverPublicKey, diffieHellman.prime)

        print('Shared key == ' + str(diffieHellman.shared_key))

        self.generateKey(name, diffieHellman)

        exit()

    def generateKey(self, name, diffieHellman):

        # self.requestKey()
        publicKey = self.informName(name, diffieHellman)

        file = open('client_key.txt', 'w')
        # publicKey = self.s.recv(64)
        file.write('Public-key: ' + publicKey + '\n')
        encPrivateKey = self.s.recv(64).decode('utf-8')
        print('Encrypted Private-key: ' + encPrivateKey)
        privateKey = diffieHellman.decrypt(encPrivateKey)
        print('Decrypted Private-key: ' + privateKey)
        file.write('Private-key: ' + privateKey + '\n')
        file.close()
        self.s.close()


if sys.argv[1] == '--generate-key' and len(sys.argv) == 3:
    client = Client()
    client.diffieHellman(sys.argv[2])
    print('Key generated successfully')
