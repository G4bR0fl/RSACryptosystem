import sympy
import numpy
import random


def xgcd(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mulinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g == 1:
        return x % b


def generateKey():

    p = sympy.randprime(10**2, 10**3)   
    print("Prime 'p':", p)
    q = p

    while p == q:
        q = sympy.randprime(10**2, 100**3)
        print("Prime 'q':", q)

    n = p*q
    e = 65537
    lambda_n = numpy.lcm(p - 1, q - 1)
    d = mulinv(e, lambda_n)

    return (p, q, n, e, lambda_n, d)


def encrypt(message, e, n):
    public_part1, public_part2 = e, n 
    cipher = [(ord(char) ** public_part1) % public_part2 for char in message]
    print(cipher)
    return cipher


def decrypt(cipher, d, n):
    private_part1, private_part2 = d, n
    plaintext = [chr((char ** private_part1) % private_part2) for char in cipher]
    print(plaintext)
    return ''.join(plaintext)

key1 = generateKey()
key2 = generateKey()
msg = input("Entra com a string:\n")
ascii_encoding = [ord(char) for char in msg]
print("Mensagem encriptada: ")
print(''.join(map(str,ascii_encoding)))
cifra1 = encrypt(msg, key1[3], key1[2])
decrypted_msg = decrypt(cifra1, int(key1[5]), int(key1[2]))
