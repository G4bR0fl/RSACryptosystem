import socket
from DiffieHellman import DiffieHellman
import time
from RSA import RSA

class Server:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 30000))
        self.s.listen(1)
        print('Alohomora')
        connections = []

        while True:
            self.connection, address = self.s.accept()
            connections.append(self.connection)
            print(address)
            while True:
                data = self.connection.recv(1024)
                print(data)
                if data.decode(encoding='utf-8') == 'generate-key':
                    self.diffieHellman()
                    self.connection.close()
                    print('-' * 70)
                    break
                if data.decode(encoding='utf-8') == 'user-key':
                    self.connection.send('Username?'.encode())
                    name = self.connection.recv(1024)
                    publicKey = self.findUser(name.decode(encoding='utf-8'))
                    self.connection.send(publicKey.encode())
                    self.connection.close()
                    break
                if data.decode(encoding='utf-8') == 'message':
                    self.connection.send('...'.encode())
                    message = self.connection.recv(5000)
                    print(len(message))
                    print(message[:7].decode('utf8'))
                    msg = []
                    for i in range(8, len(message[8:]), 4):
                        msg.append(int.from_bytes(message[i:i+3], byteorder='big'))
                        # print(int.from_bytes(message[i:i+3], byteorder='big'))
                    rsa = RSA()
                    a = rsa.decrypt(msg, 1633, 2231)
                    print(a)
                    # print(int.from_bytes(message[8:], byteorder='big', ))
                    break

                # message = data.decode(encoding='utf-8')
                # message = message.split('_')
                # if message[0] == 'boris':
                #     print(message[0])
                #     input()



    def generateKey(self, diffieHellman):

        name = self.connection.recv(1024).decode(encoding='utf-8')
        print('Encrypted name == ' + name)

        decName = diffieHellman.decrypt(name)
        print('Decrypted name == ' + decName)

        if self.checkUser(decName):

            rsa = RSA()
            rsa.generateKey()

            # TODO: gera chave publica e privada rsa aqui
            # TODO: por enquanto sao place holders

            publicKey = str(rsa.publicKey[0]) + '_' + str(rsa.publicKey[1])
            print('Public-key: ' + publicKey)
            privateKey = str(rsa.privateKey[0]) + '_' + str(rsa.privateKey[1])
            # privateKey = rsa.privateKey
            print('Private-key: ' + privateKey)

            file = open('server_key.txt', 'a')
            file.write(decName + ' ' + publicKey + '\n')
            file.close()

            publicKey = diffieHellman.encrypt(publicKey)
            print('Encrypted Public-Key: ' + publicKey)
            privateKey = diffieHellman.encrypt(privateKey)
            print('Encrypted Private-Key: ' + privateKey)
            self.connection.send(publicKey.encode())
            time.sleep(1)
            self.connection.send(privateKey.encode())



        else:
            error = diffieHellman.encrypt('This name already exists')
            self.connection.send(error.encode())
            return


    def diffieHellman(self):

        diffieHellman = DiffieHellman()
        diffieHellman.geratePrimeAndCoprime()

        print('Prime == ' + str(diffieHellman.prime))
        print('Alpha == ' + str(diffieHellman.alpha))

        primeAlpha = str(diffieHellman.prime) + '_' + str(diffieHellman.alpha)

        self.connection.send(primeAlpha.encode())

        diffieHellman.generatePrivateKey(diffieHellman.prime)
        diffieHellman.generatePublicKey(diffieHellman.prime, diffieHellman.alpha)
        print('Private == ' + str(diffieHellman.privateKey))
        print('Public == ' + str(diffieHellman.publicKey))

        self.connection.send(str(diffieHellman.publicKey).encode())

        clientPublicKey = int(self.connection.recv(1024).decode(encoding='utf-8'))
        print('Client key == ' + str(clientPublicKey))

        diffieHellman.sharedKey(clientPublicKey, diffieHellman.prime)
        print('Shared key == ' + str(diffieHellman.shared_key))

        self.generateKey(diffieHellman)


    def checkUser(self, name):
        file = open('server_key.txt', 'r')

        for i in file:
            name_entry = i.split(' ')
            if name == name_entry[0]:
                file.close()
                return False
        file.close()
        return True


    def findUser(self, name):
        file = open('server_key.txt', 'r')

        for i in file:
            name_entry = i.split(' ')
            if name == name_entry[0]:
                file.close()
                return name_entry[1]
        file.close()
        return 'User not found'


server = Server()