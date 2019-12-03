import sympy
import numpy
import random
import time

class RSA:

    def __init__(self):
        pass

    def xgcd(self, a, b):
        """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            q, b, a = b // a, a, b % a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0


    def mulinv(self, a, b):
        _, x, _ = self.xgcd(a, b)
        return (x + 100 * b) % b  # garante que nao vai ser negativo pq o operador % nao trata mod direito


    def generateKey(self):
        p = sympy.randprime(10 ** 1, 10 ** 2)
        q = p

        while p == q:
            q = sympy.randprime(10 ** 1, 10 ** 2)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        # print("p =", p, "q =", q, "n =", n, "phi_n =", phi_n)
        e = random.randrange(1, phi_n)
        g, _, _ = self.xgcd(e, phi_n)
        while g != 1:
            e = random.randrange(1, phi_n)
            g, _, _ = self.xgcd(e, phi_n)
        d = self.mulinv(e, phi_n)
        # print("p =", p, "q =", q, "n =", n, "phi_n =", phi_n, "e =", e, "d =", d)
        self.privateKey = (n, d)
        self.publicKey = (n, e)
        return (p, q, n, e, phi_n, d)


    def encrypt(self, message, e, n):
        public_part1, public_part2 = e, n
        cipher = [(ord(char) ** public_part1) % public_part2 for char in message]
        return cipher


    def decrypt(self, cipher, d, n):
        private_part1, private_part2 = d, n
        plaintext = [chr((char ** private_part1) % private_part2) for char in cipher]
        return ''.join(plaintext)

    def run(self):
        print("Gerenating first key...")
        time.sleep(0.5)
        key1 = self.generateKey()
        print("First key generated")
        print("Gerenating second key...")
        time.sleep(0.5)
        key2 = self.generateKey()
        print("Second key generated")
        msg = input("Insira um texto para ser encriptado:\n")
        ascii_encoding = [ord(char) for char in msg]
        print("Mensagem encriptada:")
        cifra1 = self.encrypt(msg, key1[3], key1[2])
        print(''.join(map(str, cifra1)))
        decrypted_msg = self.decrypt(cifra1, key1[5], key1[2])
        print("Mensagem desencriptada:", decrypted_msg)


# publica (n= 625357, e= 521617)
# privada (n= 625357, d=220241)