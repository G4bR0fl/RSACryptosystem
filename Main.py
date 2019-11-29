import sympy
import numpy
import random

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mulinv(a, b):
    _, x, _ = xgcd(a, b)
    return (x + 100*b)% b # garante que nao vai ser negativo pq o operador % nao trata mod direito


def generateKey():

    p = sympy.randprime(10**0, 10**3)
    q = p

    while p == q:
        q = sympy.randprime(10**0, 10**3)
    n = p*q
    phi_n = (p-1)*(q-1)
    print("p =", p, "q =", q, "n =", n, "phi_n =", phi_n)
    e = random.randrange(1, phi_n)
    g, _, _ = xgcd(e, phi_n)
    while g != 1:
        e = random.randrange(1, phi_n)
        g, _, _ = xgcd(e, phi_n)
    d = mulinv(e, phi_n)
    print("p =", p, "q =", q, "n =", n, "phi_n =", phi_n, "e =", e, "d =", d)
    
    return (p, q, n, e, phi_n, d)


def encrypt(message, e, n):
    public_part1, public_part2 = e, n 
    cipher = [(ord(char) ** public_part1) % public_part2 for char in message]
    print(cipher)
    return cipher

def decrypt(cipher, d, n):
    private_part1, private_part2 = d, n
    plaintext = [chr((char ** private_part1) % private_part2) for char in cipher]
    return ''.join(plaintext)

key1 = generateKey()
print("First key generated")
key2 = generateKey()
print("Second key generated")
msg = input("Entra com a string:\n")
ascii_encoding = [ord(char) for char in msg]
print("Mensagem encriptada: ")
cifra1 = encrypt(msg, key1[3], key1[2])
print(''.join(map(str,cifra1)))
decrypted_msg = decrypt(cifra1, key1[5], key1[2])
print("Mensagem desencriptada: ", decrypted_msg)