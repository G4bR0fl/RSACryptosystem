from DiffieHellman import DiffieHellman
import sys
import socket
import hashlib
from RSA import RSA

class Client:

    def __init__(self, server, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(30)
        try:
            self.s.connect((server, port))

        except ConnectionRefusedError:
            print('Connection refused')

    def fileMessage(self, fileName):
        file = open(fileName, 'r')
        text = file.read()
        file.close()
        return text

    def hashMessage(self, text):
        m = hashlib.sha256()
        m.update(text.encode())
        m.digest()
        return str(m.hexdigest())

    def encryptMessage(self, text, hexHash):
        file = open('client_key.txt', 'r')
        privateKey = file.readlines()
        privateKey = privateKey[1].split()[1:]
        rsa = RSA()
        return rsa.encrypt(hexHash + text, int(privateKey[1]), int(privateKey[0]))

    def encodeList(self, encMessage):
        byteArr = []
        for i in encMessage:
            byteArr.append((i).to_bytes(4, byteorder='big'))

        self.byteArr = byteArr

    def conCat(self, nameB):
        byteStr = b''
        for i in self.byteArr:
            byteStr += i
        byteStr = nameB + byteStr
        print(byteStr)
        self.byteStr = byteStr

    def sendMessage(self, fileName, name):
        self.s.send('message'.encode())
        self.s.recv(1024)
        text = self.fileMessage(fileName)
        hexHash = self.hashMessage(text)
        print(hexHash)
        encMessage = self.encryptMessage(text, hexHash)
        self.encodeList(encMessage)
        print(len(self.byteArr))
        nameB = (name + '_').encode()
        self.conCat(nameB)
        # encMessage = bytes(encMessage)

        # print(encMessage)
        # msg = name + '_' + encMessage
        self.s.send(self.byteStr)
        exit()

        # result = []
        # while True:
        #     print('Write your message: ', end='')
        #     msg = input()
        #     if len(msg) < 20:
        #         result.append(self.s.recv(1))
        #         while True:
        #             try:
        #                 print(result)
        #                 result.append(self.s.recv(1))
        #             except socket.timeout:
        #                 break
        #
        #     else:
        #         print('Message too long, write a message smaller than 20 characters')

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
        publicKey = publicKey.split('_')
        file.write('Public-key: ' + publicKey[0] + ' ' + publicKey[1] + '\n')
        encPrivateKey = self.s.recv(64).decode('utf-8')
        print('Encrypted Private-key: ' + encPrivateKey)
        privateKey = diffieHellman.decrypt(encPrivateKey)
        privateKey = privateKey.split('_')
        print('Decrypted Private-key: ' + privateKey[0] + ' ' + privateKey[1])
        file.write('Private-key: ' + privateKey[0] + ' ' + privateKey[1] + '\n')
        file.close()
        self.s.close()

    def findUser(self, username):
        self.s.send('user-key'.encode())
        if self.s.recv(1024).decode(encoding='utf-8') == 'Username?':
            self.s.send(username.encode())
            publicKey = self.s.recv(1024).decode(encoding='utf-8')
            print('User: ' + username)
            print('Public-key: ' + publicKey)
        else:
            print('Error')

# class ClientServer:
#
#     def __init__(self):


if sys.argv[1] == '--generate-key' and len(sys.argv) == 3:
    client = Client('127.0.0.1', 30000)
    client.diffieHellman(sys.argv[2])
    print('Key generated successfully')

if sys.argv[1] == '--send-message' and len(sys.argv) == 4:
    client = Client('127.0.0.1', 30000)
    client.sendMessage(sys.argv[2], sys.argv[3])

if sys.argv[1] == '--user-key' and len(sys.argv) == 3:
    client = Client('127.0.0.1', 30000)
    client.findUser(sys.argv[2])

# arg1 = --user-connect, arg2 == ip, arg3 == port
if sys.argv[1] == '--user-connect' and len(sys.argv) == 4:
    client = Client('127.0.0.1', 30000)
