import socket
from DiffieHellman import DiffieHellman
import time


class Server:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 3000))
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
                    break

    def generateKey(self, diffieHellman):

        name = self.connection.recv(1024).decode(encoding='utf-8')
        print('Encrypted name == ' + name)

        decName = diffieHellman.decrypt(name)
        print('Decrypted name == ' + decName)

        if self.checkUser(decName):
            # TODO: gera chave publica e privada rsa aqui
            # TODO: por enquanto sao place holders

            publicKey = 'a1b2c3d4'
            print('Public-key: ' + publicKey)
            privateKey = 'e5f6g7h8'
            print('Private-key: ' + privateKey)

            file = open('server_key.txt', 'a')
            file.write(decName + ' ' + publicKey + ' ' + privateKey + '\n')
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

server = Server()