import sympy
import math
import random

class DiffieHellman:

    def __init__(self):
        pass

    def primRoots(self, prime):
        required_set = {num for num in range(1, prime) if math.gcd(num, prime)}
        return [g for g in range(1, prime) if required_set == {pow(g, powers, prime) for powers in range(1, prime)}]

    def geratePrimeAndCoprime(self):
        self.prime = sympy.randprime(10, 100)
        allPrimRoots = self.primRoots(self.prime)
        total_primRoots = len(allPrimRoots)
        primRootIndex = random.randint(0, total_primRoots - 1)
        self.alpha = allPrimRoots[primRootIndex]

    def generatePrivateKey(self, prime):
        self.privateKey = random.randint(0, prime)
        return self.privateKey

    def generatePublicKey(self, prime, alpha):
        self.publicKey = (alpha ** self.privateKey) % prime
        return self.publicKey

    def sharedKey(self, anotherPublicKey, prime):
        self.shared_key = (anotherPublicKey ** self.privateKey) % prime
        return self.shared_key

    def encrypt(self, message):
        charArray = list(message)
        intArray = []
        for i in charArray:
            intArray.append(ord(i) ^ self.shared_key)

        charArray = []
        for i in intArray:
            ascii_char = chr(i)
            # if len(number) == 1:
            #     number = '00' + number
            # elif len(number) == 2:
            #     number = '0' + number
            charArray.append(ascii_char)
        message = ''.join(charArray)
        # message = int(charArray)

        return message

    def decrypt(self, message):

        # message = str(message)

        # if len(message) % 3 == 1:
        #     message = '00' + message
        # elif len(message) % 3 == 2:
        #     message = '0' + message

        # message_decrypted = [(message[i:i+3]) for i in range(0, len(message), 3)]

        message = list(message)
        message_decrypted = []

        for i in message:
            message_decrypted.append(chr(ord(i) ^ self.shared_key))

        return ''.join(message_decrypted)

# d = DiffieHellman()
# d.geratePrimeAndCoprime()
# d.generatePrivateKey(d.prime)
# d.generatePublicKey(d.prime, d.alpha)
#
#
# e = DiffieHellman()
# e.generatePrivateKey(d.prime)
# e.generatePublicKey(d.prime, d.alpha)
#
# d.sharedKey(e.publicKey, d.prime)
# e.sharedKey(d.publicKey, d.prime)
#
# msg = 'alahu'
# # print(d.shared_key)
# print(msg)
# msg = d.encrypt(msg)
# print(msg)
# msg = d.decrypt(msg)
# print(msg)
# print(d.shared_key, e.shared_key)