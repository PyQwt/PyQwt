#!/usr/bin/env python

from math import sqrt

def isPrime(n):
    for i in range(2, 1+int(sqrt(n))):
        if not n % i:
            return 0
    return 1

for i in range(4, 16):
    k = j = 1 << i
    while not isPrime(k):
        k += 1
    print k
