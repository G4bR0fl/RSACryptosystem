import sympy
import numpy


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
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
    q = p

    while p == q:
        q = sympy.randprime(10**2, 100**3)

    n = p*q
    e = 65537
    lambda_n = numpy.lcm(p - 1, q - 1)
    d = mulinv(e, lambda_n)

    return (p, q, n, e, lambda_n, d)


def encrypt(message, e, n):
    return (message ** e) % n


def decrypt(cipher, d, n):
    return (cipher ** d) % n


key1 = generateKey()
key2 = generateKey()

print(key1)
cifra1 = encrypt(166, key1[3], key1[2])
print(cifra1)
mensagem = decrypt(int(cifra1), int(key1[5]), int(key1[2]))
print(mensagem)
